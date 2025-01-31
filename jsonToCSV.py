import pandas as pd
import argparse
import json

def json_to_csv(input_json, output_csv):
    """
    Reads a JSON file, flattens nested arrays efficiently, converts it into a Pandas DataFrame, and exports it as a CSV file.
    
    Args:
        input_json (str): Path to the input JSON file.
        output_csv (str): Path to the output CSV file.
        
    Usage:
        python3 jsonToCSV.py data/input.json data/output.csv
    """
    try:
        # Read JSON file
        with open(input_json, 'r') as f:
            data = json.load(f)
        
        # Convert JSON to DataFrame
        df = pd.json_normalize(data)
        
        # Flatten list-type columns into separate columns efficiently
        new_cols = []
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():  # Check if column has lists
                max_len = df[col].apply(lambda x: len(x) if isinstance(x, list) else 0).max()
                
                # Create new columns as a DataFrame and concatenate in one step
                expanded_cols = pd.DataFrame(df[col].tolist(), index=df.index)
                expanded_cols = expanded_cols.iloc[:, :max_len]  # Ensure correct column count
                expanded_cols.columns = [f"{col}_{i+1}" for i in range(expanded_cols.shape[1])]
                
                new_cols.append(expanded_cols)
                df.drop(columns=[col], inplace=True)  # Remove original array column
        
        # Concatenate all expanded columns at once (avoiding fragmentation)
        if new_cols:
            df = pd.concat([df] + new_cols, axis=1)
        
        # Export DataFrame to CSV
        df.to_csv(output_csv, index=False)

        print(f"CSV file '{output_csv}' has been successfully created and is ready for QuickSight!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Argument parser for command-line inputs
    parser = argparse.ArgumentParser(description="Convert a JSON file to CSV for QuickSight with efficient array flattening.")
    parser.add_argument("input_json", help="Path to the input JSON file")
    parser.add_argument("output_csv", help="Path to the output CSV file")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with user-provided file paths
    json_to_csv(args.input_json, args.output_csv)
