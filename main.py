import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict
import socket
import re

url = "http://ransomxifxwc5eteopdobynonjctkxxvap77yqifu2emfbecgbqdw6qd.onion/"
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Cookie': '_token=3831097059; _uuid=948a7594-d795-4323-8495-b28242782252',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}

response = requests.get(url, proxies=proxies, headers=headers)
if response.status_code == 200:
    with open('page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("Страница сохранена в файл 'page.html'")
else:
    print(f"Ошибка запроса. Статус код: {response.status_code}")

with open('page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

victim_sites = soup.find_all('div', class_='col-12 col-md-6 col-lg-4')

country_count = defaultdict(int)
continent_count = defaultdict(int)

for site in victim_sites:
    title = site.find('div', class_='card-title')
    if title:
        try:
            site_name = title.get_text(strip=True)
            site_name = re.sub(r"[<\(].*?[>\)]", "", site_name)
            site_name = site_name.strip()

        except Exception:
            continue

        try:
            site_ip = socket.gethostbyname(site_name)
        except socket.gaierror:
            continue
        api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey=2a9f15951e1c45799e1c4f504b0675b1&ip={site_ip}'
        response_api = requests.get(api_url)
        if response_api.status_code == 200:
            data = response_api.json()
            country = data.get('country_name', 'Неизвестно')
            continent = data.get('continent_name', 'Неизвестно')
            country_count[country] += 1
            continent_count[continent] += 1
        else:
            print(f"Ошибка при запросе для сайта {site_name}")


with open('country_count.json', 'w', encoding='utf-8') as json_file:
    json.dump(country_count, json_file, ensure_ascii=False, indent=4)
with open('continent_count.json', 'w', encoding='utf-8') as json_file:
    json.dump(continent_count, json_file, ensure_ascii=False, indent=4)
