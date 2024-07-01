import json
import argparse
import re

def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)

def transform_name(name):
    sanitized = sanitize_name(name)
    words = sanitized.split('_')
    transformed = words[0] + ''.join(word.capitalize() for word in words[1:])
    return f"{transformed}_bool_exp"

def get_bool_exp_type(field_type, scalar_representations, object_types):
    base_type = field_type.rstrip('!')
    is_array = base_type.startswith('[') and base_type.endswith(']')
    if is_array:
        base_type = base_type[1:-1].rstrip('!')

    if base_type in scalar_representations:
        return transform_name(scalar_representations[base_type])
    elif base_type in object_types:
        return transform_name(base_type)
    else:
        return transform_name(base_type)

def update_model_filter_expression_types(subgraph, bool_exp_map):
    updated_count = 0
    for obj in subgraph['objects']:
        if obj.get('kind') == 'Model':
            object_type = obj['definition'].get('objectType')
            if object_type:
                new_filter_exp_type = bool_exp_map.get(object_type)
                if new_filter_exp_type:
                    obj['definition']['filterExpressionType'] = new_filter_exp_type
                    updated_count += 1
                    print(f"Updated filterExpressionType for Model with objectType: {object_type}")
    return updated_count

def process_file(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        data = json.load(file)
    
    total_removed = 0
    total_scalar_added = 0
    total_object_added = 0
    total_models_updated = 0
    
    for subgraph in data.get('subgraphs', []):
        original_length = len(subgraph.get('objects', []))
        
        subgraph['objects'] = [
            obj for obj in subgraph.get('objects', [])
            if obj.get('kind') != 'ObjectBooleanExpressionType'
        ]
        
        removed = original_length - len(subgraph['objects'])
        total_removed += removed

        object_types = {
            obj['definition']['name']: obj['definition']
            for obj in subgraph['objects']
            if obj.get('kind') == 'ObjectType'
        }

        scalar_representations = {}
        scalar_bool_exps = {}
        bool_exp_map = {}

        for obj in subgraph['objects']:
            if obj.get('kind') == 'DataConnectorLink':
                connector_name = obj['definition']['name']
                schema = obj['definition']['schema']['schema']
                scalar_types = schema.get('scalar_types', {})

                for rep_obj in subgraph['objects']:
                    if rep_obj.get('kind') == 'DataConnectorScalarRepresentation':
                        if rep_obj['definition']['dataConnectorName'] == connector_name:
                            scalar_type = rep_obj['definition']['dataConnectorScalarType']
                            scalar_representations[scalar_type] = rep_obj['definition']['representation']

                for scalar_type, properties in scalar_types.items():
                    if scalar_type in scalar_representations:
                        representation = scalar_representations[scalar_type]
                        bool_exp_name = transform_name(representation)
                        comparison_operators = [
                            {"name": op, "argumentType": f"{representation}!"}
                            for op in properties.get('comparison_operators', {}).keys()
                        ]
                        
                        # Add range operator for numeric types if it exists
                        if scalar_type in ['float', 'double', 'int', 'long'] and 'range' in properties.get('comparison_operators', {}):
                            comparison_operators.append({"name": "range", "argumentType": "range_input!"})
                        
                        new_bool_exp = {
                            "kind": "BooleanExpressionType",
                            "version": "v1",
                            "definition": {
                                "name": bool_exp_name,
                                "operand": {
                                    "scalar": {
                                        "type": representation,
                                        "comparisonOperators": comparison_operators,
                                        "dataConnectorOperatorMapping": [
                                            {
                                                "dataConnectorName": connector_name,
                                                "dataConnectorScalarType": scalar_type,
                                                "operatorMapping": {}
                                            }
                                        ]
                                    }
                                },
                                "logicalOperators": {"enable": True},
                                "isNull": {"enable": True},
                                "graphql": {
                                    "typeName": f"{sanitize_name(representation)}ComparisonExp"
                                }
                            }
                        }
                        subgraph['objects'].append(new_bool_exp)
                        scalar_bool_exps[scalar_type] = bool_exp_name
                        total_scalar_added += 1
                        print(f"Added BooleanExpressionType for scalar type: {scalar_type} with representation: {representation}")

        for obj_name, obj_def in object_types.items():
            comparable_fields = []
            for field in obj_def.get('fields', []):
                field_name = field['name']
                field_type = field['type']
                
                bool_exp_type = get_bool_exp_type(field_type, scalar_representations, object_types)
                
                comparable_fields.append({
                    "fieldName": field_name,
                    "booleanExpressionType": bool_exp_type
                })

            bool_exp_name = transform_name(obj_name)
            new_obj_bool_exp = {
                "kind": "BooleanExpressionType",
                "version": "v1",
                "definition": {
                    "name": bool_exp_name,
                    "operand": {
                        "object": {
                            "type": obj_name,
                            "comparableFields": comparable_fields,
                            "comparableRelationships": []
                        }
                    },
                    "logicalOperators": {"enable": True},
                    "isNull": {"enable": True},
                    "graphql": {"typeName": f"{sanitize_name(obj_name)}BoolExp"}
                }
            }
            subgraph['objects'].append(new_obj_bool_exp)
            bool_exp_map[obj_name] = bool_exp_name
            total_object_added += 1
            print(f"Added BooleanExpressionType for object type: {obj_name}")

        models_updated = update_model_filter_expression_types(subgraph, bool_exp_map)
        total_models_updated += models_updated

    with open(output_filename, 'w') as file:
        json.dump(data, file, indent=2)
    
    return total_removed, total_scalar_added, total_object_added, total_models_updated

def main():
    parser = argparse.ArgumentParser(description='Process JSON file: remove ObjectBooleanExpressionType, add BooleanExpressionTypes, and update Model filterExpressionTypes.')
    parser.add_argument('--input', default='metadata.json', help='Input JSON file (default: metadata.json)')
    parser.add_argument('--output', default='output.json', help='Output JSON file (default: output.json)')
    parser.add_argument('--structure', choices=['metadata', 'opendd'], default='metadata', help='Input file structure (default: metadata)')
    args = parser.parse_args()

    removed, scalar_added, object_added, models_updated = process_file(args.input, args.output)
    print(f"Removed {removed} ObjectBooleanExpressionType objects from {args.input}")
    print(f"Added {scalar_added} BooleanExpressionType objects for scalar representations")
    print(f"Added {object_added} BooleanExpressionType objects for object types")
    print(f"Updated filterExpressionType for {models_updated} Model objects")
    print(f"Modified JSON saved to {args.output}")

if __name__ == "__main__":
    main()