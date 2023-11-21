import json
import pandas as pd

def load_json_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def preprocess_data(json_data):

    if isinstance(json_data, list) and all(isinstance(item, list) for item in json_data):
        df = pd.json_normalize([item[0] for item in json_data])
    else:
        df = pd.json_normalize(json_data)

    if 'EPOCH' in df.columns:
        df['EPOCH'] = pd.to_datetime(df['EPOCH'])
        df['EPOCH'] = df['EPOCH'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df.fillna({'BSTAR': 0, 'MEAN_MOTION_DOT': 0, 'MEAN_MOTION_DDOT': 0}, inplace=True)

    df = df.astype({
        'OBJECT_ID': 'str',
        'EPHEMERIS_TYPE': 'category',
        'CLASSIFICATION_TYPE': 'category'
    })

    return df

def save_processed_data(df, output_file):
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    json_file_path = 'data/raw/orbital_data.json'
    output_csv_path = 'data/processed/cleaned_data.csv'

    json_data = load_json_data(json_file_path)

    processed_df = preprocess_data(json_data)

    save_processed_data(processed_df, output_csv_path)
