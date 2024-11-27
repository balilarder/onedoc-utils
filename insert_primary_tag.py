"""
Inplace modify the chunk data files, insert the Primary tag for the specific fields.
Input: chunk file path `root`
"""
from jsonpath_ng import parse
import json
from pathlib import Path


def insert_primary_tags(json_data):

    jsonpath_expr = parse('items[*].labelDatas[*].result.entities[*]')

    matches = jsonpath_expr.find(json_data)

    label_to_child_labels = {
        "Transactions": ['Date', 'Description', 'WithdrawalAmount', 'CheckNumber', 'DepositAmount', 'Type', 'BalanceAmount'],
        "Checks": ['Number', 'Date', 'Amount'],
        "Interests": ['Description', 'Amount']
    }

    for match in matches:
        entity = match.value
        label = entity.get('label')
        print(label)

        if label in label_to_child_labels:
            for child in entity["children"]:
                print(child)
                if child['label'] in label_to_child_labels[label]:
                    child.setdefault('tags', [])
                    child['tags'].append("Primary")

    return json_data


root = r"C:\Users\v-linluke\Desktop\OneDoc\1127-add-primary-tag-for-single-and-multiple-bank-statement\single-bank-statement\new-chunk-data"

for json_file in Path(root).glob('*.json'):
    
    with open(json_file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)
    
    insert_primary_tags(json_data)

    output_file = str(Path(root)/(json_file.name))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)
