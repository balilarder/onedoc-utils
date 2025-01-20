import requests
import json

# Define the URL for the API
url = "https://vdi-prebuilt-dte.azurewebsites.net/api/export_onedoc_label"
payload = [
    {
        "program_id": "5cd65bed-94de-49d0-b468-6d34cc718b50",
        "payload": {
            "batchName": "6e6175b6-956b-425e-ae79-df22a15f2367-fields",
            "targetContainerUri": "https://vdiprebuiltdte.blob.core.windows.net/dev?{SAS_TOKEN}",
            "directoryPath": "onedoc_export_test/20250120-Batch-ID-SEA/",
            "converterName": "Default",
            "pathType": "WithoutBatchDirectory"
        }
    }
]

# Set headers (optional, if required by the API)
headers = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer <your_token>"  # Uncomment and replace with token if needed
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Print the response from the API
print(response.status_code)  # HTTP status code
print(response.json())       # Response body as JSON
