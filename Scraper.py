import bs4
import requests

base_url = 'http://pixeljoint.com'
generated_urls = [f"{base_url}/pixelart/{pnum}.htm" for pnum in range(1000, 1005)]

for url in generated_urls:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    image = soup.find(id="mainimg")
    if image:
        print('title '+image['alt'])
        print('width '+image['width'])
        print('height '+image['height'])
        print('src '+image['src'])
    