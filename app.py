# app.py

import streamlit as st
import json
from azure_upload import upload_to_blob
from test_model import analyze_document

st.set_page_config(page_title="Document Intelligence Analyzer", layout="wide")

st.title("📄 Custom Document Intelligence Analyzer")

uploaded_file = st.file_uploader("Upload a PDF or image", type=["pdf", "jpg", "jpeg", "png"])

schema = None
if st.checkbox("Use schema.json for custom output formatting"):
    try:
        with open("schema.json") as f:
            schema = json.load(f)
        st.success("Loaded schema.json")
    except Exception as e:
        st.error(f"Could not load schema.json: {e}")

if uploaded_file and st.button("Analyze Document"):
    with st.spinner("Uploading to Azure Blob Storage..."):
        blob_url = upload_to_blob(uploaded_file, uploaded_file.name)

    st.info(f"Uploaded to: {blob_url}")

    with st.spinner("Running Document Intelligence model..."):
        result = analyze_document(blob_url, schema)

    st.subheader("📊 Analysis Result")
    st.json(result)