# 把一包primary field和item都有Label的資料拆成兩部分
from pathlib import Path
import json
import copy

folder = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\\exported\\en_us_other_field_item")
split_primary_field_path = Path("split/primary_field")
split_item_path = Path("split/item")

cnt = 0

Path(split_primary_field_path).mkdir(exist_ok=True, parents=True)
Path(split_item_path).mkdir(exist_ok=True, parents=True)

for jfile in folder.glob("*.json"):
    if jfile.stem.startswith('OneDoc'):
        continue
    
    # check each one has item:
    with jfile.open('r', encoding='utf-8') as f:
        jdata = json.load(f)
    print(type(jdata))

    cnt += 1
    print(jfile.name)
    primary_field_json = copy.deepcopy(jdata)
    new_labels = []
    for label in primary_field_json["labelDatas"][0]["result"]["entities"]:
        if label["label"] != 'Items':
            new_labels.append(label)
    primary_field_json["labelDatas"][0]["result"]["entities"] = new_labels


    items_json = copy.deepcopy(jdata)
    new_labels = []
    for label in items_json["labelDatas"][0]["result"]["entities"]:
        if label["label"] == 'Items':
            new_labels.append(label)
    items_json["labelDatas"][0]["result"]["entities"] = new_labels

    # write new jsons
    with (split_primary_field_path / Path(jfile.name)).open('w', encoding='utf-8') as newf:
        json.dump(primary_field_json, newf, indent=4, ensure_ascii=False)

    with (split_item_path / Path(jfile.name)).open('w', encoding='utf-8') as newf:
        json.dump(items_json, newf, indent=4, ensure_ascii=False)