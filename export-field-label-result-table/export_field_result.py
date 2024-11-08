from pathlib import Path
import pandas as pd
import json
from jsonpath_rw import parse
import re

document_url_mapping = {}
PROGRAM_ID = "5cd65bed-94de-49d0-b468-6d34cc718b50"
PROJECT_ID = "e9285499-204e-4335-9266-326532f29e02"


# first, remain the last chunk
# ...
chunk_path = Path("C:\\Users\\v-linluke\\Desktop\\VDI\\VDI-onedoc-API-data\\20241108-export-field-result-table\\reference-data\\ChunkData").glob('*.json')

for chunk in chunk_path:
    with open(chunk, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    chunkid = data['chunkId']
    
    for item in data['items']:
        url = item['staticData']['uri']
        itemid = item['itemId']
        
        match = re.search(r'/document/([a-f0-9]+)\.[a-zA-Z0-9]+', url)
        document_id = match.group(1) if match else None

        document_url_mapping[document_id] = f"https://onedoclabeling.azurewebsites.net/projects/{PROJECT_ID}/chunks/{chunkid}?programId={PROGRAM_ID}&itemId={itemid}"


export_result_root = Path("C:\\Users\\v-linluke\\Desktop\\VDI\\VDI-onedoc-API-data\\20241108-export-field-result-table\\export-result\\20241108-56f9185c-9eb0-4ba7-adb1-5a5dbbaa0f52-field-1713414362-merged-1714152689")
output_path = "C:\\Users\\v-linluke\\Desktop\\VDI\\VDI-onedoc-API-data\\20241108-export-field-result-table\\output\\output.xlsx"

# Helper function to process a single entity and add it to the data list
def process_entity(entity, filename, link):
    return {
        'documentid': filename,
        'fieldname': entity.get('label', ""),
        'tag': ", ".join(entity.get('tags', [])),
        'state': entity.get('state', ""),
        'text': entity.get('text', ""),
        'value': entity.get('value', ""),
        'link': link
    }

data = []
for export_result in export_result_root.glob('*.json'):
    if export_result.name.startswith('OneDoc'):
        continue
    
    # Load the JSON data
    with open(export_result, 'r', encoding='utf-8') as file:
        label = json.load(file)

    filename = Path(export_result).name
    link = document_url_mapping[Path(export_result).name.split('.')[0]]

    # Determine the JSONPath expression based on the structure of `label`
    attr_jpath = "items.[*].labelDatas.[0].result" if "items" in label else "labelDatas.[0].result"

    # Extract data using JSONPath
    attribute_container = {}
    for result in parse(attr_jpath).find(label):
        attribute_container.update(result.value)

    # Collect data for DataFrame
    
    for result in attribute_container.get('entities', []):
        # Process main entity
        data.append(process_entity(result, filename, link))
        
        # Process children if they exist
        for child in result.get('children', []):
            data.append(process_entity(child, filename, link))

# Create DataFrame
df = pd.DataFrame(data)
df.to_excel(output_path)