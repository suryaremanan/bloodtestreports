from fastapi import FastAPI, UploadFile, File, HTTPException
import pytesseract
from pdf2image import convert_from_path
from ollama_api import generate_health_recommendations
from pathlib import Path  # Import Path from pathlib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Directories
UPLOAD_DIR = Path("uploaded_pdfs")
REPORTS_DIR = Path("reports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Function to extract text from PDF using OCR
def extract_text_from_pdf(pdf_file: UploadFile):
    temp_file_path = UPLOAD_DIR / pdf_file.filename
    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(pdf_file.file.read())
        
        images = convert_from_path(temp_file_path)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)

    except Exception as e:
        logging.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    finally:
        if temp_file_path.exists():
            os.remove(temp_file_path)
    
    return text

@app.post("/upload/")
async def upload_pdf(pdf_file: UploadFile = File(...)):
    try:
        logging.info("Received file for processing")
        extracted_text = extract_text_from_pdf(pdf_file)
        logging.info(f"Extracted text: {extracted_text[:100]}")  # Log the first 100 characters
        recommendations = generate_health_recommendations("Patient", extracted_text)
        logging.info("Generated recommendations")
        return {"recommendations": recommendations}
    except Exception as e:
        logging.error(f"Failed to process PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Welcome to Health Insights AI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)




