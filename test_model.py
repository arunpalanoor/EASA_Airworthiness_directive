# test_model.py

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from dotenv import load_dotenv
import os
from typing import Optional, Dict, Any


def analyze_document(file_url: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Analyze a document using Azure Document Intelligence and return structured JSON.
    """

    load_dotenv()
    endpoint = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
    key = os.getenv("DOC_INTELLIGENCE_KEY")
    model_id = os.getenv("MODEL_ID")

    client = DocumentAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    poller = client.begin_analyze_document_from_url(model_id, file_url)
    result = poller.result()

    output = {"documents": []}

    for document in result.documents:
        doc_obj = {
            "doc_type": document.doc_type,
            "confidence": document.confidence,
            "fields": {}
        }

        for name, field in document.fields.items():
            value = field.value if field.value else field.content

            doc_obj["fields"][name] = {
                "value": value,
                "confidence": field.confidence
            }

        output["documents"].append(doc_obj)

    # Optional schema transformation
    if schema:
        output = apply_schema(output, schema)

    return output


def apply_schema(result: dict, schema: dict) -> dict:
    """
    Transform the raw result into a custom JSON structure based on a schema.
    """

    transformed = {"documents": []}

    for doc in result["documents"]:
        new_doc = {
            "doc_type": doc["doc_type"],
            "confidence": doc["confidence"] if schema.get("include_confidence", True) else None,
            "fields": {}
        }

        for field_name, field_data in doc["fields"].items():
            new_name = schema.get("rename_fields", {}).get(field_name, field_name)

            if schema.get("include_confidence", True):
                new_doc["fields"][new_name] = field_data
            else:
                new_doc["fields"][new_name] = field_data["value"]

        transformed["documents"].append(new_doc)

    return transformed