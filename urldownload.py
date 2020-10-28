import bs4
import requests
from pymongo import MongoClient
from datetime import datetime
from os import path

session = requests.Session()

startTime = datetime.now()

#range
start = 5050
stop = 140000

folder = "pj_img/"

#db settings
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.pixeldb
collection = db.pixeldb

base_url = 'http://pixeljoint.com'
generated_urls = [f"{base_url}/pixelart/{pnum}.htm" for pnum in range(start, stop)]

for i in range (start, stop):
    try:
        if path.exists(folder + str(i) + ".gif") or path.exists(folder + str(i) + ".png") :
            response = requests.get(f"{base_url}/pixelart/{i}.htm")
            soup = bs4.BeautifulSoup(response.text, "html.parser")
            image = soup.find(id="mainimg")
            if image:
                url = base_url+image['src']
                print(
                    str(
                        collection.update_one({"pjId": i}, { "$set": {"url": url} })
                    ) + " " + str(i)
                )
                

    except:
        print("error with " + str(i))
        continue


print("done: " + str(stop - start) + " items, " + str(start) + " - " + str(stop))

print("Start time: " + str(startTime))
print("Finish time: " + str(datetime.now()))
print("Total time: " + str(datetime.now() - startTime))
print("Average time per item: " + str((datetime.now() - startTime)/(stop - start)))