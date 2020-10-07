#ISSUES: doesn't log transparent colors, now they are black?

from PIL import Image
from pymongo import MongoClient
import glob 
#glob is for easy importing filenames?

#db settings
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.pixeldb
collection = db.col001

#image settings
folder = "images"

images = glob.glob( folder + "/*")

for image in images:
  img = Image.open(image)

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
    #filename minus path
    "filename": image[len(folder) + 1:],
    "width": img.width,
    "height": img.height,
    "colors": colors
  }
  #enter into database
  collection.insert_one(imageEntry)
  print(imageEntry)



