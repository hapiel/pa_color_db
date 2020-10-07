import bs4
import requests

base_url = 'http://pixeljoint.com/pixelart/'
generated_urls = [f"{base_url}{pnum}.htm" for pnum in range(1000, 1005)]

for url in generated_urls:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    image = soup.find(id="mainimg")
    if image:
        print(image['src'])
    