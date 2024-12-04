import requests
import re
import time

for i in range(1, 25054):
    time.sleep(1)
    print(f"Ripping file {i}: {(i/25053) * 100:.3f}%")
    abc = requests.get(f"https://thesession.org/tunes/{i}/abc")
    if abc.status_code != 200:
        print(f"Tune {i} not found on site! Error code: {abc.status_code}")
        continue
    tune_title = re.search(r"T: (.*)", abc.text).group(1).strip()
    with open(f"data/session/{i}-{tune_title}.abc", "w") as f:
        f.write(abc.text)
