import os
import json
from fpdf import FPDF

# Function to extract blood test details from JSON
def extract_blood_tests(patient_data):
    blood_tests = []
    for entry in patient_data.get('entry', []):
        resource = entry.get('resource', {})
        if resource.get('resourceType') == 'Observation':
            category = resource.get('category', [{}])[0].get('coding', [{}])[0].get('code')
            if category == 'laboratory':  # Adjust this to match the specific category for lab tests
                test_name = resource.get('code', {}).get('coding', [{}])[0].get('display')
                value = resource.get('valueQuantity', {}).get('value')
                unit = resource.get('valueQuantity', {}).get('unit')
                blood_tests.append({
                    'test_name': test_name,
                    'value': value,
                    'unit': unit
                })
    return blood_tests

# Function to create a PDF report
def create_pdf_report(blood_tests, patient_id, output_dir, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add a title
    pdf.cell(200, 10, txt="Blood Test Report", ln=True, align='C')
    pdf.ln(10)

    # Add patient ID
    pdf.cell(200, 10, txt=f"Patient ID: {patient_id}", ln=True)
    pdf.ln(10)

    # Add each blood test result
    for test in blood_tests:
        pdf.cell(200, 10, txt=f"{test['test_name']}: {test['value']} {test['unit']}", ln=True)

    # Save the PDF
    output_path = os.path.join(output_dir, file_name)
    pdf.output(output_path)
    print(f"PDF report generated: {output_path}")

# Main function to process all JSON files in the input directory
def process_reports(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each JSON file
    for json_file in os.listdir(input_dir):
        if json_file.endswith('.json'):
            with open(os.path.join(input_dir, json_file)) as f:
                patient_data = json.load(f)
            
            # Extract patient ID
            patient_id = patient_data.get('id', os.path.splitext(json_file)[0])

            # Extract blood test data
            blood_tests = extract_blood_tests(patient_data)

            # Create PDF report
            pdf_file_name = f"{patient_id}_blood_test_report.pdf"
            create_pdf_report(blood_tests, patient_id, output_dir, pdf_file_name)

# Specify input and output directories
input_directory = '/home/surya/Documents/synthea/output/fhir'
output_directory = '/home/surya/Documents/synthea/output/pdf'

# Run the script
process_reports(input_directory, output_directory)
