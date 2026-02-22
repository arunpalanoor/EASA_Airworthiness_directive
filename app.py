# app.py

import streamlit as st
import json
from azure_upload import upload_to_blob
from test_model import analyze_document
import pandas as pd

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

    doc = result["documents"][0]

    # --- Key fields ---
    st.markdown("### 📌 Key Fields")
    key_fields = ["PurchaseOrderNumber", "VendorName", "Total"]
    cols = st.columns(len(key_fields))

    for idx, key in enumerate(key_fields):
        if key in doc["fields"]:
            cols[idx].metric(
                label=key,
                value=doc["fields"][key]["value"],
                delta=f"Conf: {doc['fields'][key]['confidence']:.2f}"
            )

    # --- Table of all fields ---
    st.markdown("### 📋 All Extracted Fields")
    rows = []
    for field_name, field_data in doc["fields"].items():
        rows.append({
            "Field": field_name,
            "Value": field_data["value"],
            "Confidence": round(field_data["confidence"], 3)
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    # --- Raw JSON (optional) ---
    with st.expander("🔧 Raw JSON Output"):
        st.json(result)