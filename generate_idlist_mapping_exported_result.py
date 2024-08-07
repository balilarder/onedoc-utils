"""
input1: folder with idlists
input2: List[folder], a list of exported label result
output: csv table, to indict the each ldlist in the input1 in the input2 or not
"""

import pandas as pd
from pathlib import Path

idlists = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\\idlists-0726").glob("*.txt")
exported_root = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0726-Receipt-EN-thermal-field-task\\task-prelabel-currency-adjust\\exported")

folders = [f.name for f in exported_root.iterdir() if f.is_dir()]

file_name_sets = [set () for _ in folders]
# the collection of the exported file name


for i, v in enumerate(folders):
    exported_folder = exported_root/folders[i]
    for label in exported_folder.iterdir():
        if len(label.stem.split('.')) == 2:
            file_name_sets[i].add(label.stem.split('.')[0])
    print(len(file_name_sets[i]))
###


rows = []

for idlist in idlists:
    text_file_name = idlist.stem  # Get the text file name without extension
    with open(idlist, 'r') as file:
        for line in file:
            f = line.strip().split('.')[0]  # Remove whitespace characters
            in_folders = ['V' if f in folder_set else '' for folder_set in file_name_sets]
            total_count = sum(f in folder_set for folder_set in file_name_sets)
            
            file_info = {
                'TextFileName': text_file_name,
                'FileName': f,
            }
            
            for i, folder in enumerate(folders):
                file_info[folder] = in_folders[i]
            file_info['Count'] = total_count
            rows.append(file_info)

df = pd.DataFrame(rows)
df.to_csv("exported_task_count_idlist.csv")