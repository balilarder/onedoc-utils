# give a folder path, with downloaded chunk data in it.
# filter each latest chunk data, also the chunk# and position to locate the file.

from pathlib import Path
import json
from urllib.parse import urlparse

def list_latest_chuck_version(path: Path) -> list[Path]:
    file_names = []
    latest_data = set()

    for file in path.glob("*.json"):
        name = file.stem
        splits = name.split('-')
        file_names.append(splits)

    chunks = set(map(lambda x:x[0], file_names))
    group_by_chunk = [[y for y in file_names if y[0] == x] for x in chunks]

    for group in group_by_chunk:
        # 先排序timestamp或先排序version結果都一樣
        sub_g1 = sorted(group, key=lambda x: (x[1], x[2]), reverse=True)
        latest_data.add(tuple(sub_g1[0]))

    return [Path(f"{file[0]}-{file[1]}-{file[2]}.json") for file in latest_data]


def get_target_file_set():
    return set([
        'gWiTpdHYIthQhwhFOyGZNknrMI4jviVwE0w.png',
        'gWiTpdHMJzRpQN56nc2zXVqkWfXE$sHPmmWA.jpg',
        'gWiTpdHV1uBhRA3aivIN8air9i5q$sIIt6zg.jpg',
        'gWiTpdwQEvBpUjroCiYNnZpwGDuAHGZffiA.jpg',
        'gWiTpdA4AuxhQWIE1zBxIaFpItUFwqP5DFA.jpg',
        'gWiTpdHUIyR1e8LeDwsfivZ0EdyRz0n1jcQ.jpg',
        'gWiTpdHVxyR8ldbpITTLbV3eu8OrcD8Z19w.jpg',
        'gWiTpdwBxvBVftIwvMEJH28j326WAWEdCkg.jpg'
    ])
    
        
if __name__ == '__main__':

    root = Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\0823-find-document-position-in-chunk\\downloaded-chunk-data\\ChunkData")
    
    filter_chuck = list_latest_chuck_version(root)
    target_file = get_target_file_set()
    
    cnt = 0
    for fc in filter_chuck:
        with open(root/fc, 'r') as file:
            data = json.load(file)
            items = data["items"]
            for item in items:
                item_id = item["itemId"]
                segments = item["staticData"]["uri"].split('/')
                id_name = segments[-1].split('?')[0]

                if id_name in target_file:
                    cnt += 1
                    target_file.remove(id_name)
                    chunk_num = fc.name.split('-')[0]

                    print(f"{id_name} = chunk:{chunk_num} item:{item_id}")