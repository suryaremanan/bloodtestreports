import streamlit as st
import requests

st.title("Health Insights AI")

# Upload a blood test PDF
st.header("Upload Blood Test Report")
uploaded_pdf = st.file_uploader("Upload a blood test PDF", type=["pdf"])

if uploaded_pdf and st.button("Analyze PDF and Generate Recommendations"):
    files = {"pdf_file": (uploaded_pdf.name, uploaded_pdf.read(), "application/pdf")}
    try:
        response = requests.post("http://fastapi:8000/upload/", files=files)
        response.raise_for_status()
        recommendations = response.json().get("recommendations", "No recommendations available.")
        st.success("Recommendations generated successfully!")
        st.write(recommendations)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to process PDF: {str(e)}")
