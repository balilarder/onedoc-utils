"""
Merge MRZ1,2,3 to a combined new field `MachineReadableZone`
* inputs: origin chunk data folder path
* outputs: new chunks with added MachineReadableZone and remove MRZ1,2,3
Note that the timestemp would be hard coded, or make it generated by program itself.
"""

from pathlib import Path
import shutil
import json
import time
import uuid

def generate_MRZ_template(state, text, bboxs):
    return {
        "label": "MachineReadableZone",
        "state": state,
        "text": text,
        "value": text.replace("\\n", " "),
        "boundingBoxes": bboxs,
        "entityId": str(uuid.uuid4()),
        "tags": [
            "Primary"
        ],
        "pages": [
            1
        ],
        "children": []
    }


sources = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1104-Merge-passport-MRZ-field\\origin-chunk-data\\ChunkData").glob('*.json')
destination = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1104-Merge-passport-MRZ-field\\processed")

for file in sources:
    parts = file.name.split('-')
    new_file_name = f"{parts[0]}-1730706730-{parts[2]}"

    with open(file, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
        data_write = data.copy()

    for index, value in enumerate(data_write['items']):
        item = data_write['items'][index]

        result = item['labelDatas'][0]['result']['entities']

        for label in result:
            if label['label'] == "MRZ1":
                mrz1 = label
            elif label['label'] == "MRZ2":
                mrz2 = label
            elif label['label'] == "MRZ3":
                mrz3 = label
        
            # Rename some fields
            if label['label'] == "CountryCode":
                label['label'] = "CountryRegion"
            if label['label'] == "PassportType":
                label['label'] = "DocumentType"
            if label['label'] == "OtherNames":
                label['label'] = "Aliases"
        
        # parse the state
        if mrz1['state'] == 'notFound' and mrz2['state'] == 'notFound' and mrz3['state'] == 'notFound':
            state = "notFound"
        elif mrz1['state'] == 'skip' or mrz2['state'] == 'skip' or mrz3['state'] == 'skip':
            state = "skip"
        else:
            state = "Ok"

        merge_MRZ = '\\n'.join([mrz1['text'], mrz2['text'], mrz3['text']]).strip('\\n')
        print(data_write['chunkId'], item['itemId'], merge_MRZ, state)

        bboxs = mrz1['boundingBoxes'] + mrz2['boundingBoxes'] + mrz3['boundingBoxes']
        result.append(generate_MRZ_template(state, merge_MRZ, bboxs))

        # Remove MRZ1, MRZ2, MRZ3 from result
        result = [label for label in result if label['label'] not in ["MRZ1", "MRZ2", "MRZ3"]]
        item['labelDatas'][0]['result']['entities'] = result


    # Write the modified data to a new JSON file
    with open(destination/new_file_name, 'w', encoding='utf-8') as new_fp:
        json.dump(data_write, new_fp, ensure_ascii=False, indent=4)