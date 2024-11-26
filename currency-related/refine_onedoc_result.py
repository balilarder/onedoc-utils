"""
Refine the onedoc result to fix the defect from smart-label transform result.
Input: source_root (the collection data of `onedoc format document data`)
"""
import json
import os
from pathlib import Path
from jsonpath_ng import parse
import uuid
import re

# source_root is the collection data of `onedoc format document data`
source_root = Path(r"C:\Users\v-linluke\Desktop\OneDoc\1101-prelabel-create-task-invoice\1126-follow-up-backup\onedoc-pdf-prediction-use-re")
destination = r"C:\Users\v-linluke\Desktop\OneDoc\1101-prelabel-create-task-invoice\1126-follow-up-backup\onedoc-pdf-prediction-use-re-transform"

# Ensure destination directory exists
os.makedirs(destination, exist_ok=True)


def generate_child(field: dict) -> list:
    # field should be Items.Tax and Items.UnitPrice
    result = []
    field_names = ["currencySymbol", "currencyCode", "amount"]
    parent_entityid = field["entityId"]
    state = field.get("state")
    text = field.get('text')
    
    if state == 'notFound':
        for child in field_names:
            template  = {
                "label": child,
                "state": "notFound",
                "text": None,
                "value": None,
                "boundingBoxes": [],
                "entityId": str(uuid.uuid4()),
                "tags": [],
                "pages": [],
                "children": [],
                "parentId": parent_entityid
            }

            result.append(template)
    
    elif state == 'Ok':
        parsed_value = json.loads(field.get("value").replace("'", '"'))
        bbox = field.get("boundingBoxes")
        for child in field_names:
            if child in parsed_value:
                template  = {
                    "label": child,
                    "state": "Ok",
                    "text": text if child != 'currencyCode' else "", # `text` should come from parent's text. But currencyCode is choiceType, so don't have text
                    "value": str(parsed_value[child]), # `value` should come from prediction reuslts
                    "boundingBoxes": bbox,
                    "entityId": str(uuid.uuid4()),
                    "tags": [],
                    "pages": [
                        1
                    ],
                    "children": [],
                    "parentId": parent_entityid
                }
            else:
                template  = {
                    "label": child,
                    "state": "notFound",
                    "text": None,
                    "value": None,
                    "boundingBoxes": [],
                    "entityId": str(uuid.uuid4()),
                    "tags": [],
                    "pages": [],
                    "children": [],
                    "parentId": parent_entityid
                }
            result.append(template)
    
    return result


def load_json(file_path):
    """Load a JSON file and return its content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process(json_data):
    """Process the loaded JSON data."""
    jsonpath_expr = parse("$.labelDatas[*].result.entities[*]")
    matches = jsonpath_expr.find(json_data)


    for match in matches:
        entity = match.value
        label = entity.get("label")
        state = entity.get("state")

        if label == "Items.Amount":
            if state == 'notFound':
                continue
            
            # Use `value` to check preidiction result, if it only numeric data means it doesn't has currencySymbol, so currencySymbol is `notFound`
            if re.match(r"^-?\d+(\.\d+)?$", entity.get('value').replace(",", "")):
                for i, child in enumerate(entity['children']):
                    if child['label'] == 'currencySymbol':
                        entity['children'][i] = {
                            "label": "currencySymbol",
                            "state": "notFound",
                            "text": None,
                            "value": None,
                            "boundingBoxes": [],
                            "entityId": str(uuid.uuid4()),
                            "tags": [],
                            "pages": [],
                            "children": [],
                            "parentId": entity['entityId']
                        }
         
            entity.pop('value')
        
        if label == "Items.Tax":
            entity["children"].extend(generate_child(entity))
            entity.pop('value')

        if label == "Items.UnitPrice":
            entity["children"].extend(generate_child(entity))
            entity.pop('value')

        if label == "Items.TaxRate":
            if state != 'notFound':
                entity.pop('value')
        
    return json_data

def write_json(data, output_path):
    """Write JSON data to a file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Main loop
for file in source_root.glob('*.json'):

    json_data = load_json(file)
    # Process the JSON data
    print(file)
    processed_data = process(json_data)

    # Write the processed data to the destination
    output_file = Path(destination) / Path(file).name
    write_json(processed_data, output_file)

    print(f"Processed and saved: {output_file}")

