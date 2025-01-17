import requests
import json

# Define the parameters

# Define the URL for the API
url = "https://syndaction.azurewebsites.net/api/start-syndact?code={API_KEY}"

# Prepare the payload
payload = {
    "config": "https://vdiprebuiltdte.blob.core.windows.net/prebuilt-lab-data/121cbfd6-d724-4963-b235-a9d3cebe0532/translationSyndactionConfig.json"
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
