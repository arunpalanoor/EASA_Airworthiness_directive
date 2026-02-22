# EASA_Airworthiness_directive
EASA Airworthiness Directive database using Azure Document Intelligence

# 📄 Custom Document Intelligence Analyzer (Streamlit App)

A modular Streamlit application that allows users to upload PDF or image documents, store them in Azure Blob Storage, and analyze them using a **Custom Azure Document Intelligence model**.  
The results are displayed in a clean, user‑friendly interface with tables, metrics, and optional schema‑based formatting.

---

## 🚀 Features

### ✅ Upload & Store Documents
- Users upload a PDF/JPG/PNG file.
- File is automatically uploaded to Azure Blob Storage under the `raw/` folder.
- A public blob URL is generated for model analysis.

### ✅ Custom Document Intelligence Model Integration
- Uses Azure Document Intelligence (Form Recognizer) with your **custom trained model**.
- Accepts the blob URL as input.
- Returns structured JSON output.

### ✅ Configurable Output Formatting
- Optional `schema.json` allows:
  - Renaming fields  
  - Hiding confidence values  
  - Custom output structure  

### ✅ Clean, Modular Architecture
```your-app/ │ ├── app.py                # Streamlit UI ├── azure_upload.py       # Uploads files to Azure Blob Storage ├── test_model.py         # Runs the custom Document Intelligence model ├── schema.json           # Optional output formatting rules └── .streamlit/ └── secrets.toml      # Secure secrets for deployment
```


---

## 🧩 Module Overview

### **1. `azure_upload.py`**
Handles uploading files to Azure Blob Storage using:
- `AZURE_STORAGE_CONNECTION_STRING`
- `AZURE_CONTAINER_NAME`

Returns a public blob URL.

### **2. `test_model.py`**
A clean, function‑based wrapper around Azure Document Intelligence:
- `analyze_document(file_url, schema=None)`
- Returns structured JSON
- Optional schema transformation

### **3. `app.py`**
Streamlit UI:
- File uploader
- Upload to Blob Storage
- Run model
- Display results as:
  - Metrics
  - Table
  - Expandable JSON

---

## 🔐 Secrets & Environment Variables

### Local Development
Create a `.env` file:
{
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_CONTAINER_NAME=your-container-name
DOC_INTELLIGENCE_ENDPOINT=your-endpoint
DOC_INTELLIGENCE_KEY=your-key MODEL_ID=your-model-id
}


### Streamlit Cloud Deployment
Streamlit Cloud does **not** use `.env`.

Instead:

1. Create `.streamlit/secrets.toml`:
   ```toml
   AZURE_STORAGE_CONNECTION_STRING = "your-connection-string"
   AZURE_CONTAINER_NAME = "your-container-name"

   DOC_INTELLIGENCE_ENDPOINT = "your-endpoint"
   DOC_INTELLIGENCE_KEY = "your-key"
   MODEL_ID = "your-model-id"
2. Add the same values in
Streamlit Cloud → App Settings → Secrets


