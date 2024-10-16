# Append new items in a existed task, using offset to make sure each chunk has 60 items

"""
Input:
* dummy chunks data after inserting translation image, locale, otherelse..
* The last chunk data from the existed task, say, the chunk `A` and want to append starting from id `B`
It will offset the new data from chunkA.itemidB and generate a set of new chunks to upload to the blob.
"""

from pathlib import Path
import json

# Collect all chunks file to generate all items list
all_items = []

cnt = 0
chunks = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1015-filter-attribute-result-append-to-existed-primary-and-item\\dummy-item-chunk\\modified").glob('*.json')

for chunk in chunks:
    with open(chunk, 'r', encoding='utf-8') as jfile:
        data = json.load(jfile)  # Load JSON content

    items = data["items"]

    for item in items:
        item["itemId"] = cnt
        cnt += 1
        all_items.append(item)


# From the last existed chunk insert new item, and create a new chunk if exceed 60 items
current_chunk = 27
current_id = 45
chunk_folder = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1015-filter-attribute-result-append-to-existed-primary-and-item\\origin-item-chunk-data\\modified")
chunk_file = "27-1727148814-v2.0.json"

def generate_chunk_template(chunkid):
    template = {
        "chunkId": chunkid,
        "updatedAt": 0,
        "updatedBy": "System",
        "updatedByEmail": "System",
        "items": []
    }
    return template


for item in all_items:
    chunk_file = chunk_folder / chunk_file
    
    if not chunk_file.exists():
        # Create a new chunk file
        with open(chunk_file, 'w', encoding='utf-8') as jfile:
            json.dump(generate_chunk_template(current_chunk), jfile, ensure_ascii=False, indent=4)

    with open(chunk_file, 'r', encoding='utf-8') as jfile:
        data = json.load(jfile)  # Load JSON content

    items = data["items"]  # origin chunks

    # Add a new item with a unique itemId
    item["itemId"] = current_id
    current_id += 1
    items.append(item)

    with open(chunk_file, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)

    if len(items) == 60:
        current_chunk += 1
        current_id = 0
        chunk_file = f"{current_chunk}-0-v2.0.json"
