import json
import uuid
from pathlib import Path

from jsonpath_rw_ext import parse
from tqdm import tqdm
import re


special_case = set()

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


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_normalize_amount_text(s: str):

    def extract_numbers(s):
        match = re.search(r'-?\d[\d,]*(?:\.\d+)?', s)
                        
        if match:
            return match.group()
        return None
    
    # def is_number(s):
    #     try:
    #         float(s)
    #         return True
    #     except ValueError:
    #         return False
    
    if s:
        striped_text = s.strip()
        if not is_number(striped_text):
            
            number = extract_numbers(striped_text)
            if number:
                return number
    return s

def get_field_bbox(field):
    bboxs = field.get("boundingBoxes", [])
    return bboxs

def parser_currency_object(parent: dict, currency_map_by_locale: dict, locale: str, id):
    child = list()
    # amount = parent.copy() # 改成不是直接copy了?? 好像還是可以先抄，只是怕有兩個bbox應該只要拿一個就好
    # amount['entityId'] = str(uuid.uuid4())
    # amount['parentId'] = parent.get('entityId')
    # amount['label'] = "Amount"
    # amount['tags'] = []
    # child.append(amount)

    if parent.get("state") == "notFound":

        amount = {
            "entityId": str(uuid.uuid4()),
            "label": "Amount",
            "state": "notFound",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "text": "",
            "value": "",
            "parentId": parent.get('entityId')
        }
        child.append(amount)
        
        currency_code = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencyCode",
            "state": "notFound",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "value": "",
            "parentId": parent.get('entityId')
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
            "parentId": parent.get('entityId')
        }
        child.append(currency_symbol)
    else:
        
        bboxs = get_field_bbox(parent)
        if len(bboxs) > 2:
            special_case.add(id)

        origin_text = parent.get('text')
        normalize_amount_text = get_normalize_amount_text(origin_text)

        # try to extract the currency symbol
        if origin_text == normalize_amount_text:
            currency_symbol_state = "notFound"
            currency_symbol_bbox = []
            currency_symbol_text = ""

        else:
            currency_symbol_state = parent.get('state')
            
            # currency_symbol_bbox = parent.get('boundingBoxes') if len(bboxs) == 1 else [bbox for bbox in bboxs if not is_number(bbox['customData']['text'])]
            if len(bboxs) == 1:
                currency_symbol_bbox = parent.get('boundingBoxes')
            else:
                currency_symbol_bbox = []
                for bbox in bboxs:
                    if bbox['customData'].get('text', '') and not is_number(bbox['customData'].get('text', '')):
                        currency_symbol_bbox.append(bbox)
                    elif not bbox['customData'].get('text', ''):
                        special_case.add(id)

            currency_symbol_text = origin_text.replace(normalize_amount_text, "", 1).strip()
                
        # parse amount bbox
        if len(bboxs) == 1:
            amount_bbox = parent.get('boundingBoxes')
        else:
            amount_bbox = []
            for bbox in bboxs:
                if not bbox['customData'].get('text', ''):
                    special_case.add(id)
                    amount_bbox.append(bbox)
                elif is_number(bbox['customData'].get('text', '')):
                    amount_bbox.append(bbox)

        
        amount = {
            "entityId": str(uuid.uuid4()),
            "label": "Amount",
            "state": parent.get('state'),
            # "boundingBoxes": [],  #??
            # "boundingBoxes":parent.get('boundingBoxes') if len(bboxs) == 1 else [bbox for bbox in bboxs if is_number(bbox['customData']['text'])],  #??
            "boundingBoxes": amount_bbox,
            "pages": parent.get('pages'),
            "children": [],
            "tags": [],
            # "text": "",  # ??
            "text": normalize_amount_text,  # ??
            "value": parent.get('value'),
            "parentId": parent.get('entityId')
        }
        child.append(amount)
        

        # child[0]['text'] = get_normalize_amount_text(child[0]['text'])  ###
        
        currency_code = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencyCode",
            "state": "Ok",
            "boundingBoxes": [],
            "pages": [],
            "children": [],
            "tags": [],
            "value": currency_map_by_locale.get(locale) if currency_map_by_locale.get(locale) is not None else None,
            "parentId": parent.get('entityId')
        }
        child.append(currency_code)
        
        # currency symbol要改
        currency_symbol = {
            "entityId": str(uuid.uuid4()),
            "label": "CurrencySymbol",
            # "state": "notFound",  # ????
            "state": currency_symbol_state,
            # "boundingBoxes": [],   # ???
            "boundingBoxes": currency_symbol_bbox,   # ???
            "pages": [],
            "children": [],
            "tags": [],
            "value": "",
            # "text": "",    # ??
            "text": currency_symbol_text,    # ??
            "parentId": parent.get('entityId')
        }
        child.append(currency_symbol)


    parent['children'] = child

date = "0807"
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

        # # 測試新規則
        # if fpath.stem.split('.')[0] not in ['ReceiptEN_006_976', 'ReceiptEN_000_000','ReceiptEN_000_036','ReceiptEN_000_001', 'ReceiptEN_006_430','ReceiptEN_006_863']:
        #     continue

        # if fpath.stem.split('.')[0] not in need_id:
        #     continue

        with fpath.open('r', encoding='utf-8') as file:
            jdata = json.load(file)
        
        # jdata = json.loads(fpath.read_text())
        id = fpath.stem
        # locale = locale_map.get(id)  # 從attribute 整理出locale對應id的dict
        locale = jdata['labelDatas'][0]['result']['Locale'].replace('en-', '')
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

                        parser_currency_object(field, currency_map_by_locale, locale, id)


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
                                parser_currency_object(children, currency_map_by_locale, locale, id)

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



print("Special id")
for sid in special_case:
    print(sid)
