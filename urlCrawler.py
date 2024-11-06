import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'https://www.codewars.com'

response = requests.get(url, timeout = 10)
response.raise_for_status()  # Raises an error for non-200 status codes
soup = BeautifulSoup(response.text, 'html.parser')

unvisited_links = []
visited_links = []
snd_ctch = []

links = soup.find_all('a', href = True)

print(f'Status: {response.status_code}')
for link in links:
    href = link.get('href')
    if (href and ('https://' in href or 'http://' in href) and href not in unvisited_links):
        unvisited_links.append(link.get('href'))
    
print(len(unvisited_links))
print('\n'.join(unvisited_links))

while len(unvisited_links) > 0:
    link_2 = unvisited_links[0]
    response_2 = requests.get(link_2, timeout = 10)
    soup_2 = BeautifulSoup(response_2.text, 'html.parser')
    links_2 = soup_2.find_all('a', href = True)

    for link_1 in links_2:
        href = link_1.get('href')
        if (href and ('https://' in href or 'http://' in href) and href not in unvisited_links or visited_links):
            snd_ctch.append(link_1.get('href'))
    
    visited_links.append(link_2)
    unvisited_links.remove(link_2)

