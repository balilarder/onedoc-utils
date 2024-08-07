# input a idlist, read all the exported data, find the Locale and sort the idlist with Locale
# and write a new idlist file (As the payload of the create-onedoc-task `idList` input)

from pathlib import Path
import pandas as pd
import json

id_mapping_locale = {}

id_list_file = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\idlists-0726\\temp1.txt")
with open(id_list_file, 'r') as file:
    lines = file.readlines()

    
    for line in lines:
        line = line.strip()

        
        for json_file in Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\utils\\output\\batch_data-0806\\merge\\en_non_test_field").glob('*.json'):
            if json_file.stem.startswith(line):
                with open(json_file, 'r', encoding='utf-8') as file:
                    
                    jdata = json.load(file)
                    # Process jdata as needed
                    # print(f"Loaded data from {json_file}")
                    id_mapping_locale[json_file.name] = jdata['labelDatas'][0]['result']['Locale']
                    
                break  # Stop after finding the first matching file
        # else:
        #     print(f"No matching file found for {line}")

print(id_mapping_locale)

sorted_items = sorted(id_mapping_locale.items(), key=lambda item: item[1])
print(sorted_items)

# Path to the new text file
output_file_path = "sorted_keys3.txt"

# Write the sorted keys to the new text file
with open(output_file_path, 'w') as file:
    # for key, value in sorted_items:
    #     file.write(f"{key}\n")
    file.write(str([i[0] for i in sorted_items]))