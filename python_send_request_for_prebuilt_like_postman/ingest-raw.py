import requests
import json

# Define the parameters
projectId = "121cbfd6-d724-4963-b235-a9d3cebe0532"
projectName = "hotelReceipt-unit4"
rawPath = "https://vdiprebuiltdte.blob.core.windows.net/dev/receipt/gpt-classifier-hotel-receipt-by-zayn-gpt/"
toRunOCR = True

# Define the URL for the API
url = "https://vdi-prebuilt-dte.azurewebsites.net/api/orchestrators/ingest-raw"

# Prepare the payload
payload = {
    "projectId": projectId,
    "projectName": projectName,
    "rawPath": rawPath,
    "toRunOCR": toRunOCR
}

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
