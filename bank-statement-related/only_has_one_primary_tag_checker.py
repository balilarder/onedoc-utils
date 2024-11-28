"""
A primary tag checker, use dfs to parse all the label results, get label tags, 
make sure all of tags list have only one `Primary` 

* input: the source root including all onedoc chunk data
"""

import json
from pathlib import Path

def check_primary_node_tag(data, tag="tags"):

    def recursive_search(node):
        if isinstance(node, dict):
            target = node.get(tag)
            if isinstance(target, list):


                # print(f"tag: {target}")
                if len(target) > 1:
                    print(f"nonono: {target}")

                    seen = set()
                    node[tag] = [x for x in target if not (x == "Primary" and x in seen or seen.add(x))]
                    print(f"new taget: {node[tag]}")

            
            for key, value in node.items():
                if isinstance(value, (dict, list)):
                    recursive_search(value)
        
        elif isinstance(node, list):
            for item in node:
                recursive_search(item)

    recursive_search(data)



source_root = Path(r"C:\Users\v-linluke\Desktop\OneDoc\1127-add-primary-tag-for-single-and-multiple-bank-statement\muitiple-bank-statement\origin-chunk-data2")
dest_root = Path(r"C:\Users\v-linluke\Desktop\OneDoc\1127-add-primary-tag-for-single-and-multiple-bank-statement\muitiple-bank-statement\new-chunk-data2")

for json_file in source_root.glob('*.json'):

    with open(json_file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    for item in json_data["items"]:
        print(f"itemid: {item['itemId']}")
        labelDatas = item['labelDatas'][0]
        entities = labelDatas['result']['entities']
        
        check_primary_node_tag(entities)

    output_file = str(Path(dest_root)/(json_file.name))
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

