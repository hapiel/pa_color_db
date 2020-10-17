import bs4
import requests
from pymongo import MongoClient
from datetime import datetime
import re

#range
start = 122915
stop = 135397

#how long does the script take
startTime = datetime.now()

#db settings
uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client.pixeldb
collection = db.pjData

def cleanHtml(raw_html):
    str_html = str(raw_html)[1:-1]
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str_html)
    return cleantext

base_url = 'http://pixeljoint.com'
generated_urls = [f"{base_url}/pixelart/{pnum}.htm" for pnum in range(start, stop)]

for num, url in enumerate(generated_urls, start=start):
    try:
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        image = soup.find(id="mainimg")
        if image:

            title = cleanHtml(soup.select("td:nth-of-type(2) > table > tr:nth-of-type(1) > td:nth-of-type(2)"))
            
            author = cleanHtml(soup.select("table a[target='_top']"))
            
            dateStr = soup.select("tr:nth-of-type(3) > td:nth-of-type(2)")
            dateStr = cleanHtml(dateStr)
            #remove time from date
            dateStr = dateStr.split(" ")
            datetimeObject = datetime.strptime(dateStr[0], '%m/%d/%Y')
            
            faves = cleanHtml(soup.select(".clean > a:nth-of-type(1)"))
            faves = int(faves.split()[0])

            desc = cleanHtml(soup.select("tr:nth-of-type(6) > td"))
            tags = cleanHtml(soup.select(".clear.small"))
            #remove redundant tags
            tags = tags.split(",")[:-5]
            # join and remove tags so that every word gets it's own item.
            tags = " ".join(tags).split()
            
            imageEntry = {
                "pjId": num,
                "title": title,
                "author": author,
                "date": datetimeObject,
                "faves": faves,
                "desc": desc,
                "tags": tags
            }
            collection.insert_one(imageEntry)

            print(num)
            # print(title)
            # print(author)
            # print(datetimeObject)
            # print(faves)
            # print(desc)
            # print(tags)
            # print("-----------")

            
    except OSError as error:
        print("error with " + str(num))
        print(error)
        continue

print("done: " + str(stop - start) + " items, " + str(start) + " - " + str(stop))

print("Start time: " + str(startTime))
print("Finish time: " + str(datetime.now()))
print("Total time: " + str(datetime.now() - startTime))
print("Average time per item: " + str((datetime.now() - startTime)/(stop - start)))


