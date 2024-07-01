import json
import argparse
from typing import Dict, List, Any

def load_json(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data: Dict[str, Any], file_path: str):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_scalar_types(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    result = {}
    for subgraph in data.get('subgraphs', []):
        for obj in subgraph.get('objects', []):
            if obj.get('kind') == 'DataConnectorLink':
                schema = obj.get('definition', {}).get('schema', {}).get('schema', {})
                scalar_types = schema.get('scalar_types', {})
                for scalar_type, properties in scalar_types.items():
                    if 'comparison_operators' in properties:
                        result[scalar_type] = {
                            'operators': list(properties['comparison_operators'].keys()),
                            'connector_name': obj.get('definition', {}).get('name', '')
                        }
    return result

def find_object_types(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    result = []
    for subgraph in data.get('subgraphs', []):
        for obj in subgraph.get('objects', []):
            if obj.get('kind') == 'ObjectType':
                result.append(obj)
    return result

def generate_scalar_boolean_expression_type(scalar_type: str, info: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "kind": "BooleanExpressionType",
        "version": "v1",
        "definition": {
            "name": f"{scalar_type}_bool_exp",
            "operand": {
                "scalar": {
                    "type": scalar_type,
                    "comparisonOperators": [
                        {"name": op, "argumentType": f"{scalar_type}!"} for op in info['operators']
                    ],
                    "dataConnectorOperatorMapping": [
                        {
                            "dataConnectorName": info['connector_name'],
                            "dataConnectorScalarType": scalar_type,
                            "operatorMapping": {}
                        }
                    ]
                }
            },
            "logicalOperators": {"enable": True},
            "isNull": {"enable": True},
            "graphql": {
                "typeName": f"{scalar_type}_Comparison_Exp"
            }
        }
    }

def generate_object_boolean_expression_type(obj_type: Dict[str, Any], scalar_types: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    name = obj_type['definition']['name']
    comparable_fields = []
    
    for field in obj_type.get('definition', {}).get('fields', []):
        field_name = field.get('name')
        field_type = field.get('type').rstrip('!')  # Remove '!' if present
        if field_type in scalar_types:
            comparable_fields.append({
                "fieldName": field_name,
                "booleanExpressionType": f"{field_type}_bool_exp"
            })
    
    return {
        "kind": "BooleanExpressionType",
        "version": "v1",
        "definition": {
            "name": f"{name}_bool_exp",
            "operand": {
                "object": {
                    "type": name,
                    "comparableFields": comparable_fields,
                    "comparableRelationships": []
                }
            },
            "logicalOperators": {"enable": True},
            "isNull": {"enable": True},
            "graphql": {"typeName": f"{name}BoolExp"}
        }
    }

def add_boolean_expression_types(data: Dict[str, Any], scalar_types: Dict[str, Dict[str, Any]], object_types: List[Dict[str, Any]]) -> int:
    count = 0
    for subgraph in data.get('subgraphs', []):
        for scalar_type, info in scalar_types.items():
            new_obj = generate_scalar_boolean_expression_type(scalar_type, info)
            subgraph['objects'].append(new_obj)
            count += 1
        
        for obj_type in object_types:
            new_obj = generate_object_boolean_expression_type(obj_type, scalar_types)
            subgraph['objects'].append(new_obj)
            count += 1
    
    return count

def remove_object_boolean_expression_types(data: Dict[str, Any]) -> int:
    removed_count = 0
    for subgraph in data.get('subgraphs', []):
        objects = subgraph.get('objects', [])
        original_length = len(objects)
        objects[:] = [obj for obj in objects if obj.get('kind') != 'ObjectBooleanExpressionType']
        removed_count += original_length - len(objects)
    return removed_count

def main():
    parser = argparse.ArgumentParser(description='Process JSON file, add BooleanExpressionType objects for scalars and object types, and remove ObjectBooleanExpressionType objects.')
    parser.add_argument('--input', default='metadata.json', help='Input JSON file (default: metadata.json)')
    parser.add_argument('--output', default='output.json', help='Output JSON file (default: output.json)')
    args = parser.parse_args()

    # Load the JSON file
    data = load_json(args.input)
    
    # Find scalar types with comparison operators
    scalar_types = find_scalar_types(data)
    
    print(f"Found {len(scalar_types)} scalar types with comparison operators:")
    for scalar_type, info in scalar_types.items():
        print(f"  {scalar_type}: {', '.join(info['operators'])}")
    
    # Find object types
    object_types = find_object_types(data)
    print(f"\nFound {len(object_types)} object types")
    
    # Remove ObjectBooleanExpressionType objects
    removed_count = remove_object_boolean_expression_types(data)
    print(f"\nRemoved {removed_count} ObjectBooleanExpressionType objects")

    # Add BooleanExpressionType objects for each scalar type and object type
    added_count = add_boolean_expression_types(data, scalar_types, object_types)
    
    # Save the modified JSON
    save_json(data, args.output)
    
    print(f"Added {added_count} BooleanExpressionType objects")
    print(f"Modified JSON saved to {args.output}")

if __name__ == "__main__":
    main()