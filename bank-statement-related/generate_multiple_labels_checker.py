"""
Generate a result indicating whether a subfield contains multiple labels. 
Ideally, support single and multiple bank statements. (Now, for the `multiple bank statement`)
* inputs: chunk data root folder
* outputs: pandas table
"""
import pandas as pd
from jsonpath_rw_ext import parse
import json
from pathlib import Path

result_data = {
    'chunk': [],
    'item': [],
    'field': [],
    'parent_text': [],
    'parent_id': []
}


label_to_child_labels = {
    "Transactions": ['Date', 'Description', 'WithdrawalAmount', 'CheckNumber', 'DepositAmount', 'Type', 'BalanceAmount'],
    "Checks": ['Number', 'Date', 'Amount'],
    "Interests": ['Description', 'Amount']
}

def process_json_file(json_file, result_data):

    with open(json_file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    chunkid = json_data["chunkId"]

    for items in json_data["items"]:
        itemid = items['itemId']

        jsonpath_expr1 = parse("labelDatas[*].result.entities[?(@.label == 'Accounts')]")

        matches = jsonpath_expr1.find(items)
        for match in matches:
            entity = match.value
            
            for child in entity['children']:
                if child['label'] in label_to_child_labels.keys():
                    print(f"child: {child['label']}")
                    subfield_set = set()
                    for subfield in child['children']:
                        if subfield['label'] in label_to_child_labels[child['label']]:
                            print(f"  {subfield['label']}")
                            if subfield['label'] not in subfield_set:
                                subfield_set.add(subfield['label'])
                            else:
                                print(f"Add a row: {subfield['label']}")
                                result_data['chunk'].append(chunkid)
                                result_data['item'].append(itemid)
                                result_data['field'].append(f"{child['label']}.{subfield['label']}")
                                result_data['parent_text'].append(child.get('text', ''))
                                result_data['parent_id'].append(child.get('parentId', ''))

    
for json_file in Path(r"C:\Users\v-linluke\Desktop\OneDoc\1127-add-primary-tag-for-single-and-multiple-bank-statement\muitiple-bank-statement\new-chunk-data").glob('*.json'):
    process_json_file(json_file, result_data)

df = pd.DataFrame(result_data)

output_csv = Path("output.csv")
df.to_csv(output_csv, index=False, encoding='utf-8')

