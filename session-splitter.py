import os
from tqdm import tqdm

path = "abc_files/session"
new_path = "data/session_split"

for (root, dirs, files) in os.walk(path):
    dirname = os.path.basename(root)
    new_filepath = os.path.join(new_path, dirname)
    # Create subfolders if they don't already exist
    if root == path:
        for direc in dirs:
            os.makedirs(os.path.join(new_path, direc), exist_ok=True)
        continue
    # Walk through all files recursively
    for file in tqdm(files):
        # Open old file for reading
        filepath = os.path.join(root, file)
        with open(filepath, 'r') as file_p:
            lines = file_p.readlines()
            # Open first new file for writing, truncating if exists
            split_index = 1
            new_file_path = os.path.join(new_filepath, str(split_index) + '-' + file)
            new_file_p = open(new_file_path, 'w')
            tqdm.write("Writing to: " + new_file_path)
            for line in lines:
                # If encounter blank line, close file pointer, increment split index, open new file pointer
                if line == '\n':
                    new_file_p.close()
                    split_index += 1
                    new_file_path = os.path.join(new_filepath, str(split_index) + '-' + file)
                    new_file_p = open(new_file_path, 'w')
                    tqdm.write("Writing to: " + new_file_path)
                    continue
                new_file_p.write(line)
            new_file_p.close()