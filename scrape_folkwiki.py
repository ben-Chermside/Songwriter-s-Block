import os
import requests
from bs4 import BeautifulSoup

def scrape_lattyper_links(url):
    filtered_links = []

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        elements = soup.find_all(class_="wikilink")

        # print(elements)
        filtered_links = [element.get('href') for element in elements if element.get('href') and 'Musik' in element.get('href')]
    else:
        print(f"Failed to fetch page {response.status_code}")
    # print(filtered_links)
    return filtered_links


def fetch_abc_links(latyper_links, output_file):
    with open(output_file, 'w') as f_out:
        for link in latyper_links:
            response = requests.get(link)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                abclinks = soup.find_all('a', href=lambda href: href and href.endswith('.abc'))
                for abclink in abclinks:
                    full_abc_url = abclink['href']
                    f_out.write(full_abc_url + '\n')

            else:
                print(f"Failed to fetch {link} {response.status_code}")


def download_abc_files(abc_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    with open(abc_file, 'r') as f:
        links = [line.strip() for line in f.readlines()]
        
        for link in links:
            response = requests.get(link)

            if response.status_code == 200:
                filename = os.path.basename(link)
                file_path = os.path.join(output_folder, filename)
                with open(file_path, "wb") as file:
                    file.write(response.content)

            else:
                print(f"Failed to download {link} {response.status_code}")


if __name__ == "__main__":

    base_urls = []

    with open('song_type_links.txt', 'r') as song_type_links:
        base_urls = song_type_links.readlines()


    for base_url in base_urls:
        base_url = base_url.strip()
        lattyp_name = base_url.split("/")[-1]
        print(f"Processing Låttyp: {lattyp_name}")

        latyper_links_file = f"{lattyp_name}_links.txt"
        abc_links_file = f"{lattyp_name}_abc_links.txt"
        output_folder = os.path.join("abc_files", lattyp_name)

        latyper_links = scrape_lattyper_links(base_url)

        fetch_abc_links(latyper_links, abc_links_file)

        download_abc_files(abc_links_file, output_folder)
