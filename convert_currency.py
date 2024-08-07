import json
import uuid
from pathlib import Path

from jsonpath_rw_ext import parse
from tqdm import tqdm
import re

def generate_idlist_set(idlist_txts) -> set:
    """
    給一組idlist, 轉成set, 通常開task會有給定的idlist，處理轉換prelabel時用這些即可
    """
    result = set()
    for idlist_txt in idlist_txts:
        with idlist_txt.open('r') as file:
            
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                result.add(line.split('.')[0])
    return result

def normalize_amount_text(s: str):

    def extract_numbers(s):
        match = re.search(r'-?\d[\d,]*(?:\.\d+)?', s)
                        
        if match:
            return match.group()
        return None
    
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    if s:
        striped_text = s.strip()
        if not is_number(striped_text):
            
            number = extract_numbers(striped_text)
            if number:
                return number
    return s

def parser_currency_object(children: dict, currency_map_by_locale: dict, locale: str):
    child = list()
    amount = children.copy()
    amount['entityId'] = str(uuid.uuid4())
    amount['parentId'] = children.get('entityId')
    amount['label'] = "Amount"
    amount['tags'] = []
    child.append(amount)

    if children.get("state") == "notFound":

        currency_code = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencyCode",
            "state": "notFound",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "value": "",
            "parentId": children.get('entityId')
        }
        child.append(currency_code)

        currency_symbol = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencySymbol",
            "state": "notFound",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "value": "",
            "text": "",
            "parentId": children.get('entityId')
        }
        child.append(currency_symbol)
    else:
        # modify the Amount.text
        child[0]['text'] = normalize_amount_text(child[0]['text'])
        
        currency_code = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencyCode",
            "state": "Ok",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "value": currency_map_by_locale.get(locale) if currency_map_by_locale.get(locale) is not None else None,
            "parentId": children.get('entityId')
        }
        child.append(currency_code)
        
        # currency symbol要是not found
        currency_symbol = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencySymbol",
            "state": "notFound",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "value": "",
            "text": "",
            "parentId": children.get('entityId')
        }
        child.append(currency_symbol)


    children['children'] = child

date = "0806"
folder = "en_us_clean_field"
path = Path(f"C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\\exported\\{folder}")
idlist_txts = [
    Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\\idlists-0726\\en_others_train_id_list.txt"),
    Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\\idlists-0726\\en_others_val.txt")
]
need_id = generate_idlist_set(idlist_txts)


currency_map_by_locale = json.loads(Path('./locale_to_currency.json').read_text())
for task in [
    "primary_field",
    # "item"
]:
    # for fpath in tqdm(path.glob('ReceiptEN_007_980.jpeg.json')):
    # for fpath in tqdm(Path(f'./export/{task}/').glob('**/*.json')):
    for fpath in tqdm(Path(path).glob('**/*.json')):
        print(fpath.stem)
        
        if fpath.stem.startswith("OneDoc_"):
            continue
        
        # # # 看情況社的條件: 只需要某幾個檔案時
        # if fpath.stem.split('.')[0] not in ['Receipt_008_421', 'Receipt_005_473', 'ReceiptEN_000_782', 'ReceiptEN_011_706']:
        #     continue
        if fpath.stem.split('.')[0] not in ['Receipt_008_421','Receipt_005_473','ReceiptEN_000_782','ReceiptEN_011_706','Receipt_006_528']:
            continue
        # if fpath.stem.split('.')[0] not in need_id:
        #     continue

        with fpath.open('r', encoding='utf-8') as file:
            jdata = json.load(file)
        
        # jdata = json.loads(fpath.read_text())
        id = fpath.stem
        # locale = locale_map.get(id)  # 從attribute 整理出locale對應id的dict
        locale = jdata['labelDatas'][0]['result']['Locale']
        # currency_code = currency_map_by_locale[locale.replace('en-', '')]
        print(id, locale)
        
        
        if task == "primary_field":
            # Primary field
            for parser in parse("labelDatas.[*].result.entities").find(jdata):
                entities = parser.value
                for field in entities:
                    if field.get('label') in [
                        # "Total",
                        # "TransactionTotal",
                        # "Transaction Total",
                        "Total Tax",
                        # "Payment Total",
                        # "Subtotal",
                        # "Tip",
                        # "Grand Total",
                    ]:

                        parser_currency_object(field, currency_map_by_locale, locale.replace('en-', ''))


                    elif field.get('label') in [
                        "Tax Detail"
                    ]:
                        # 如果是not found就不用再label 
                        if field.get("state") == "notFound":
                            tax_rate = {
                                "entityId": str(uuid.uuid4()),
                                "label": "Tax Rate",
                                "state": "notFound",
                                "text": "",
                                "value": "",
                                "boundingBoxes": [],
                                "children": [],
                                "pages": [],
                                "parentId": field.get('entityId')
                            }
                            net_amount = {
                                "entityId": str(uuid.uuid4()),
                                "label": "Net Amount",
                                "state": "notFound",
                                "boundingBoxes": [],
                                "children": [],
                                "pages": [],
                                "parentId": field.get('entityId')
                            }
                            field.get("children").append(tax_rate)
                            field.get("children").append(net_amount)
                        
                        children_list = field.get('children')
                        for children in children_list:
                            if children.get('label') == "Tax Amount" or children.get('label') == "Net Amount":
                                # parser_currency_object(field, currency_map_by_locale, locale)
                                parser_currency_object(children, currency_map_by_locale, locale.replace('en-', ''))

            jdata['labelDatas'][0]['result']['Locale'] = locale

        # # elif task == "item":
        # #     # item
        # #     for parser in parse("labelDatas.[*].result.entities").find(jdata):
        # #         entities = parser.value
        # #         for field in entities:
        # #             if field.get('label') in [
        # #                 "Items",
        # #                 "Item",
        # #             ]:
        # #                 children_list = field.get('children')
        # #                 for children in children_list:
        # #                     if children.get('label') in [
        # #                         "Total Price",
        # #                         "Price",
        # #                     ]:
        # #                         parser_currency_object(field, currency_map_by_locale, locale)
        # #                     elif children.get('label') in [
        # #                         "Subitems",
        # #                     ]:
        # #                         subitems_children_list = children.get('children')
        # #                         for subitems_children in subitems_children_list:
        # #                             if subitems_children.get('label') in [
        # #                                 "Total Price",
        # #                             ]:
        # #                                 parser_currency_object(field, currency_map_by_locale, locale)    

        # #     jdata['labelDatas'][0]['result']['Locale'] = locale

        file_name = Path(fpath).name
        new_name = file_name.split('.', 1)[0] + ".json"

        dst_path = f"output/batch_data-{date}/{folder}/{task}/{file_name}"
        Path(dst_path).parent.mkdir(exist_ok=True, parents=True)
        json.dump(jdata, open(dst_path, 'w', encoding='utf-8'), indent=4, ensure_ascii=False)
