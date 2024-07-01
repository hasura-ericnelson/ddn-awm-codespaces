import argparse
import json

def find_scalar_types_with_aggregates(data):
    scalar_types_with_aggregates = {}
    for subgraph in data['subgraphs']:
        subgraph_name = subgraph['name']
        for obj in subgraph['objects']:
            if obj['kind'] == 'DataConnectorLink':
                data_connector_name = obj['definition']['name']
                for scalar_type, info in obj['definition']['schema']['schema']['scalar_types'].items():
                    if info.get('aggregate_functions'):
                        if scalar_types_with_aggregates.get(subgraph_name) is None:
                            scalar_types_with_aggregates[subgraph_name] = {}
                        if scalar_types_with_aggregates[subgraph_name].get(data_connector_name) is None:
                            scalar_types_with_aggregates[subgraph_name][data_connector_name] = {}
                        scalar_types_with_aggregates[subgraph_name][data_connector_name][scalar_type] = info
    return scalar_types_with_aggregates

def find_existing_scalar_representations(data):
    existing_representations = {}
    for subgraph in data['subgraphs']:
        subgraph_name = subgraph['name']
        for obj in subgraph['objects']:
            if obj['kind'] == 'DataConnectorScalarRepresentation':
                data_connector_name = obj['definition']['dataConnectorName']
                scalar_type = obj['definition']['dataConnectorScalarType']
                if existing_representations.get(subgraph_name) is None:
                    existing_representations[subgraph_name] = {}
                if existing_representations[subgraph_name].get(data_connector_name) is None:
                    existing_representations[subgraph_name][data_connector_name] = {}
                existing_representations[subgraph_name][data_connector_name][scalar_type] = obj['definition']['representation']
    return existing_representations

def create_scalar_representation(subgraph_name, data_connector_name, scalar_type):
    return {
        "kind": "DataConnectorScalarRepresentation",
        "version": "v1",
        "definition": {
            "dataConnectorName": data_connector_name,
            "dataConnectorScalarType": scalar_type,
            "representation": scalar_type.capitalize(),
            "graphql": {
                "comparisonExpressionTypeName": f"{subgraph_name.capitalize()}_{scalar_type.capitalize()}ComparisonExp"
            }
        }
    }

def create_aggregate_expression(subgraph_name, data_connector_name, scalar_type, info, representation):
    agg_functions = []
    function_mapping = {}
    for func_name, func_info in info['aggregate_functions'].items():
        agg_functions.append({
            "name": f"_{func_name}",
            "description": f"{func_name.capitalize()} {scalar_type}",
            "returnType": representation
        })
        function_mapping[f"_{func_name}"] = {"name": func_name}

    return {
        "kind": "AggregateExpression",
        "version": "v1",
        "definition": {
            "name": f"{representation}_aggregate_exp",
            "operand": {
                "scalar": {
                    "aggregatedType": representation,
                    "aggregationFunctions": agg_functions,
                    "dataConnectorAggregationFunctionMapping": [
                        {
                            "dataConnectorName": data_connector_name,
                            "dataConnectorScalarType": scalar_type,
                            "functionMapping": function_mapping
                        }
                    ]
                }
            },
            "count": {
                "enable": True,
                "description": f"Count of all non-null {representation}s"
            },
            "countDistinct": {
                "enable": True,
                "description": f"Count of all distinct non-null {representation}s"
            },
            "description": f"Aggregate expression for the {representation} type",
            "graphql": {
                "selectTypeName": f"{representation}_aggregate_exp"
            }
        }
    }

def process_file(data, output_file):
    scalar_types_with_aggregates = find_scalar_types_with_aggregates(data)
    existing_representations = find_existing_scalar_representations(data)
    
    new_scalar_representations = []
    new_aggregate_expressions = []
    
    for subgraph_name, data_connectors in scalar_types_with_aggregates.items():
        for data_connector_name, scalar_types in data_connectors.items():
            for scalar_type, info in scalar_types.items():
                if (subgraph_name not in existing_representations or
                    data_connector_name not in existing_representations[subgraph_name] or
                    scalar_type not in existing_representations[subgraph_name][data_connector_name]):
                    new_scalar_rep = create_scalar_representation(subgraph_name, data_connector_name, scalar_type)
                    new_scalar_representations.append(new_scalar_rep)
                    representation = new_scalar_rep['definition']['representation']
                else:
                    representation = existing_representations[subgraph_name][data_connector_name][scalar_type]
                
                new_aggregate_expressions.append(create_aggregate_expression(subgraph_name, data_connector_name, scalar_type, info, representation))
    
    # Add new scalar representations and aggregate expressions to the data
    for subgraph in data['subgraphs']:
        subgraph['objects'].extend(new_scalar_representations)
        subgraph['objects'].extend(new_aggregate_expressions)
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_scalar_representations)} new DataConnectorScalarRepresentations.")
    print(f"Added {len(new_aggregate_expressions)} new AggregateExpressions.")

def main():
    parser = argparse.ArgumentParser(description="Process metadata or opendd files.")
    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument("--output", required=True, help="Path to the output file")
    parser.add_argument("--structure", required=True, choices=["metadata", "opendd"], help="Type of file structure")
    
    args = parser.parse_args()
    
    with open(args.input, 'r') as file:
        data = json.load(file)
    
    process_file(data, args.output)

if __name__ == "__main__":
    main()