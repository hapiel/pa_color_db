#ISSUES: doesn't log transparent colors, now they are black?

from os import path
from PIL import Image
from pymongo import MongoClient
#glob is for easy importing filenames?
from datetime import datetime
import colorsys


#which items to grab
startNumber = 1000
endNumber = 135423

#how long does the script take
startTime = datetime.now()

#db settings
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.pixeldb
collection = db.pjData

#image settings
folder = "pj_img/"

def dbBrightness(r,g,b):
    return min(255,(r*r*0.0676 + g*g*0.3025 + b*b*0.0361)**0.5 * 1.5690256395005606)


for i in range (startNumber, endNumber):

    if path.exists(folder + str(i) + ".gif"):
        img = Image.open(folder + str(i) + ".gif")
    elif path.exists(folder + str(i) + ".png"):
        img = Image.open(folder + str(i) + ".png")
    else:
        continue

    print(i)

    size = img.width * img.height
    sizeMinTrans = size

    if img.mode != "RGBA":
        img = img.convert(mode="RGBA")

    imgColors = img.getcolors(maxcolors=1999)
    if imgColors == None:
        #too many colors. Still needs to be logged in the DB!
        cCount = 2000
        #still enter in db but without color or trans data
        imageEntry = {
            "width": img.width,
            "height": img.height,
            "colorCount" : cCount,
        }
        print(
            collection.update_one({"pjId": i}, { "$set": imageEntry })
        )
        continue
    
    #transparent, defining var
    trans = False
    for color in imgColors:
        #if the alpha index is 0
        if color[1][3] == 0:
            trans = True
            sizeMinTrans = size - color[0]
            #remvoe trans from list of colors
            imgColors.remove(color)
            break
    
    cCount = len(imgColors)
    
    colors = []
    #Image.getcolors() outputs [(amount of pixels, (r,g,b,a)),...]
    for color in imgColors:
        #drop alpha value:
        rgb = (color[1][0], color[1][1], color[1][2])
        # takes value between 0.0-1.0 and outputs in same range.
        hsv = colorsys.rgb_to_hsv(rgb[0]/255, rgb[1]/255, rgb[2]/255)

        colorDict = {
            "rgb": rgb,
            #String formatting to convert the values to hex:
            "hex": '#%02x%02x%02x' % rgb,
            "percent": color[0] / sizeMinTrans * 100,
            # * sign unpacks tuple and makes it 3 single arguments
            "dbBrightness": dbBrightness(*rgb),
            "hsv": (hsv[0]*360, hsv[1]*100, hsv[2]*100)
            }
        colors.append(colorDict)
    
    colors = sorted(colors, key = lambda i: i["percent"], reverse = True)
    #trim to first 100 items
    colors = colors[:100]

    imageEntry = {
        "width": img.width,
        "height": img.height,
        "trans" : trans,
        "sizeMinTrans": sizeMinTrans,
        "colorCount" : cCount,
        "colors": colors
        
    }
    print(
        collection.update_one({"pjId": i}, { "$set": imageEntry })
    )


print("Start time: " + str(startTime))
print("Finish time: " + str(datetime.now()))
print("Total time: " + str(datetime.now() - startTime))
print("Average time per item: " + str((datetime.now() - startTime)/ (endNumber - startNumber)))
