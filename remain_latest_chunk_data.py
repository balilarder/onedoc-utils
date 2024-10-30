# Given a path containing downloaded label chunk data
# The filename should be ['0-0-v2.0.json', '0-1726458566-v2.0.json', '0-1726651480-v2.0.json', '1-0-v2.0.json']
# This program would filter out the outdated chunk file, and only remains the latest chunk for each chunk id

from pathlib import Path

chunk_files = list(Path("C:\\Users\\v-linluke\\Desktop\\OneDoc\\1030-rename-attribute-name\\download-chunks\\d2d693b9-f82c-48a1-a2f3-fb5b351a5646-attribute\\ChunkData").glob('*.json'))

# Dictionary to keep the latest file for each id
latest_files = {}

for file_path in chunk_files:
    # Split the filename by "-" to extract id and timestamp
    parts = file_path.stem.split('-')
    chunk_id, timestamp = parts[0], int(parts[1])
    
    # If the id is not in the dictionary, or if the timestamp is more recent, update the dictionary
    if chunk_id not in latest_files or timestamp > latest_files[chunk_id][1]:
        latest_files[chunk_id] = (file_path, timestamp)

# Extract the Path objects of the latest files only
filtered_files = [file_info[0] for file_info in latest_files.values()]

for ff in filtered_files:
    print(ff)
print(len(filtered_files))

# delete rest files:
for file_path in chunk_files:
    print(f"file_path: {file_path}")
    if file_path not in [f for f in filtered_files]:
        file_path.unlink()