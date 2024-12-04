import requests
import re
import time
import argparse
from tqdm import trange

parser = argparse.ArgumentParser()
parser.add_argument("num", type=int, default=1)

args = parser.parse_args()

ran = trange(args.num, 25054)
for i in ran:
    time.sleep(1)
    abc = requests.get(f"https://thesession.org/tunes/{i}/abc")
    if abc.status_code != 200:
        ran.write(f"Tune {i} not found on site! Error code: {abc.status_code}")
        continue
    tune_title = re.search(r"T: (.*)", abc.text)
    if tune_title is None:
        ran.write(f"Tune {i} title not parseable!")
        continue
    tune_title = tune_title.group(1).strip()
    try:
        with open(f"data/session/{i}-{tune_title}.abc", "w") as f:
            f.write(abc.text)
    except FileNotFoundError as e:
        ran.write(f"Failed to rip {i}: {e}")
