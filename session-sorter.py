import os
from tqdm import tqdm

for file in tqdm(os.scandir("data/session")):
    if not file.is_file():
        continue
    with open(file.path, 'r') as f:
        for i, line in enumerate(f):
            if i != 4:
                continue
            type = line.split()[1]
            break
    if not os.path.exists(f"data/session/{type}"):
        os.makedirs(f"data/session/{type}")
    os.replace(file.path, f"data/session/{type}/{file.name}")
