import bs4
import requests
from PIL import Image
import mimetypes
from io import BytesIO
from datetime import datetime
import os

session = requests.Session()

startTime = datetime.now()

#range
start = 70000
stop = 135397

dirname = "pj_img"
try:
    os.mkdir(dirname)
except OSError as error:
    print(error)


base_url = 'http://pixeljoint.com'
generated_urls = [f"{base_url}/pixelart/{pnum}.htm" for pnum in range(start, stop)]

for num, url in enumerate(generated_urls, start=start):
        try:
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            image = soup.find(id="mainimg")
            if image:
                response = requests.get((base_url+image['src']))

                try:
                    img = Image.open(BytesIO(response.content))
                except:
                    print("Error with Image.open, continuing.")
                    continue
                #get actual type, not filename
                response = session.head(base_url+image['src'])
                contentType = response.headers['content-type']
                #save with proper extension
                img.save(dirname + "/" + str(num) + mimetypes.guess_extension(contentType))
                print(num)
        except:
            print("error with " + str(num))
            continue

print("done: " + str(stop - start) + " items, " + str(start) + " - " + str(stop))

print("Start time: " + str(startTime))
print("Finish time: " + str(datetime.now()))
print("Total time: " + str(datetime.now() - startTime))
print("Average time per item: " + str((datetime.now() - startTime)/(stop - start)))