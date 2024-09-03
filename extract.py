import os
import json
import pandas as pd

def extract_data_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract specific blood test data, assuming these fields exist
    patient_id = data.get('id', 'Unknown')
    blood_tests = []

    for entry in data.get('entry', []):
        resource = entry.get('resource', {})
        if resource.get('resourceType') == 'Observation':
            category = resource.get('category', [{}])[0].get('coding', [{}])[0].get('code')
            if category == 'laboratory':  # Assuming this is the category for blood tests
                test_name = resource.get('code', {}).get('coding', [{}])[0].get('display')
                value = resource.get('valueQuantity', {}).get('value')
                unit = resource.get('valueQuantity', {}).get('unit')
                blood_tests.append({
                    'patient_id': patient_id,
                    'test_name': test_name,
                    'value': value,
                    'unit': unit
                })
    
    return blood_tests

def process_all_json_files(input_dir):
    all_data = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(input_dir, filename)
            blood_tests = extract_data_from_json(json_path)
            all_data.extend(blood_tests)

    return all_data

# Example usage
input_directory = '/home/surya/Documents/synthea/output/fhir/'
all_blood_test_data = process_all_json_files(input_directory)

# Convert to DataFrame for easy handling and analysis
df = pd.DataFrame(all_blood_test_data)
print(df.head())

# Save the extracted data to a CSV file
df.to_csv('extracted_blood_test_data.csv', index=False)
