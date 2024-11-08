import requests
from bs4 import BeautifulSoup

user_url = input('Enter url: ')

def verify_url(_input):
    http_head = 'https://'
    www_head = 'www.'
    
    if www_head and http_head not in _input:
        if www_head not in _input:
            _input = www_head + _input
        if http_head not in _input:
            _input = http_head + _input
            
    if www_head not in _input:
        parts = _input.split('://')
        parts[0] += '://'
        parts.insert(1, 'www.')
        _input = ''.join(parts)
        
    return _input

url = verify_url(user_url)
response = requests.get(url, timeout = 10)
response.raise_for_status()  # Raises an error for non-200 status codes
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href = True)
print(f'Status: {response.status_code}')

unvisited_links = []
visited_links = []

for link in links:
    href = link.get('href')
    if len(href) > 1 and 'mailto:' not in href:
        if 'http' not in href:
            if href[0] != '/':
                unvisited_links.append(f'{url}/{href}')
            else:
                unvisited_links.append(f'{url}{href}')
        elif 'http' in href:
            unvisited_links.append(href)
                                       
print('\n'.join(unvisited_links))
