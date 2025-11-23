import logging
import azure.functions as func
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from datetime import datetime
import base64

def main(inputBlob: func.InputStream, outputDocument: func.Out[dict]):

    logging.info(f"Triggered for blob: {inputBlob.name} ({inputBlob.length} bytes)")

    # 1. Read the uploaded image
    image_bytes = inputBlob.read()

    # 2. Connect to Vision Service
    endpoint = "https://ComputervisionForDamage.cognitiveservices.azure.com/"
    key = "CWRqHsjk92lhxTdh8RyeSXvwwhbY5Kzk7wfjmOHSmDmbrLx5UB35JQQJ99BKACGhslBXJ3w3AAAFACOGc5Tv"

    client = ImageAnalysisClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # 3. Run Image Classification
    result = client.analyze(
        image_data=image_bytes,
        visual_features=["Caption", "Tags"]
    )

    caption = result.caption.text if result.caption else "No caption detected"
    tags = [t.name for t in result.tags] if result.tags else []

    logging.info(f"Caption: {caption}")
    logging.info(f"Tags: {tags}")

    # 4. Save result to CosmosDB
    document = {
        "id": inputBlob.name.replace("/", "_"),
        "filename": inputBlob.name,
        "caption": caption,
        "tags": tags,
        "timestamp": datetime.utcnow().isoformat(),
        "image_preview": base64.b64encode(image_bytes).decode()
    }

    outputDocument.set(document)
    logging.info("Document inserted into Cosmos DB successfully")
