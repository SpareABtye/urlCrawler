import time
import requests
from bs4 import BeautifulSoup

url = input('Enter url: ')
user_wait = input('How long between requests?\n(Choose an option)\n1 : 0s Let the site block me\n2 : 1s Play it safe\n3 : 1s-3s rando\n4 : 3s Play it safe\n')

# Function used to check format and properly use http is necessary.
def verify_url(url):
    if '://' not in url:
        url = 'https://' + url
        
    if not url.startswith('www.'):
        url = url.replace('://', '://www.', 1)
        
    return url

#Establishing time wait choice
timer = 0
time_wait= int(user_wait)
if time_wait == 2:
    timer = 1
elif time_wait == 3:
    timer = random.randint(0, 3)
elif time_wait == 4:
    timer = 3

url_f = verify_url(url) #Calling the url format function.
unvisited_links = []
visited_links = []
href_catch = [] # Needed a catch for the raw href
unvisited_links.append(url_f)
            
while len(unvisited_links) > 0:
    navi = unvisited_links[0]
    try:
        crawl_res = requests.get(navi, timeout = 10) #Allows up to 10s for the ack.
        crawl_res.raise_for_status()  # Raises an error for non-200 status codes
        crawl_soup = BeautifulSoup(crawl_res.text, 'html.parser')
        scraped = crawl_soup.find_all('a', href = True) #Pulling all href links in the current url.
        
        for scrap in scraped: #Loop to start the crawl
            href = scrap.get('href')
            if len(href) > 1 and 'mailto:' not in href and href not in href_catch: #Was running into problems pulling emails as a url, this was a way around.
                href_catch.append(href)
                if 'http' not in href:
                    if href[0] != '/' and f'{url_f}/{href}' not in unvisited_links and f'{url_f}/{href}' not in visited_links:
                        unvisited_links.append(f'{url_f}/{href}')
                    elif 'f{url_f}{href}' not in unvisited_links and  'f{url_f}{href}' not in visited_links:
                        unvisited_links.append(f'{url_f}{href}')
                        
        print(f'{navi} - {crawl_res.status_code}')
        visited_links.append(navi)
        unvisited_links.remove(navi)
        time.sleep(timer)
    except requests.exceptions.RequestException as e: #If the page cannot be reached or the crawl created a false url, this will return it but continue crawling.
        print(f'Error: Unable to reach the website: {navi}')
        print(e)
        visited_links.append(navi)
        unvisited_links.remove(navi)
    
    
                                       
print('Finished')
