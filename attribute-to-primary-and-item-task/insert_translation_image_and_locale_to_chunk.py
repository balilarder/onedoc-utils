# Insert translation image and locale to dummy task
import json
from pathlib import Path

"""
Input
* dummy chunk of primary or item task generated for test.
* exported data by api, with finished attribute task result.
Output:
* Modified chunks with translation image and locale inserted.
"""

chunks = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1015-filter-attribute-result-append-to-existed-primary-and-item\\dummy-item-chunk\\modified").glob('*.json')

cnt = 0
for chunk in chunks:
    with open(chunk, 'r', encoding='utf-8') as jfile:
        data = json.load(jfile)  # Load JSON content


    items = data["items"]
    for item in items:
        fn = item["staticData"]["uri"].split('/')[-1]
        print(fn)
        result_file = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1015-filter-attribute-result-append-to-existed-primary-and-item\\export-result\\remain-new-id-list-result") / Path(str(fn)+".json")

        with open(result_file, encoding='utf-8') as result_json:
            result = json.load(result_json)

        translation_image = result["staticData"]["customData"]["referenceImageUri"]
        locale = result["labelDatas"][0]["result"]["Locale"]

        item["staticData"]["customData"]["referenceImageUri"] = translation_image
        item["labelDatas"][0]["result"]["Locale"] = locale
        
        cnt += 1
    
    # dump data to json
    with open(chunk, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    