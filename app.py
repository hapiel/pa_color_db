#ISSUES: doesn't log transparent colors, now they are black?

from PIL import Image
from pymongo import MongoClient
import glob 
#glob is for easy importing filenames?
import bs4
import requests
from io import BytesIO
from datetime import datetime

#how long does the script take
startTime = datetime.now()

#pixeljoint
base_url = 'http://pixeljoint.com'

#db settings
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.pixeldb
collection = db.col003

#image settings
folder = "images"

images = glob.glob( folder + "/*")


generated_urls = [f"{base_url}/pixelart/{pnum}.htm" for pnum in range(1000, 1100)]

for url in generated_urls:
  response = requests.get(url)
  soup = bs4.BeautifulSoup(response.text, "html.parser")
  image = soup.find(id="mainimg")
  if image:
    response = requests.get((base_url+image['src']))
    img = Image.open(BytesIO(response.content))
    print(image['alt'])
    # print('width '+image['width'])
    # print('height '+image['height'])
    # print('src '+image['src'])

    if img.mode != "RGB":
      img = img.convert(mode="RGB")

    size = img.width * img.height
    
    colors = []

    #Image.getcolors() outputs [(amount of pixels, (r,g,b)),...]
    for color in img.getcolors():
      colorDict = {
        "rgb": color[1],
        #I don't know why this works but it does:
        "hex": '#%02x%02x%02x' % color[1],
        "percent": color[0] / size * 100
        }
      colors.append(colorDict)
    
    colors = sorted(colors, key = lambda i: i["percent"], reverse = True)
    
    imageEntry = {
      #full url
      "filename": base_url+image['src'],
      "title": image['alt'],
      "width": img.width,
      "height": img.height,
      "colors": colors
    }
    #enter into database
    collection.insert_one(imageEntry)

    #print(imageEntry)

print(datetime.now() - startTime)
