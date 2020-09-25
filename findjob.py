import sys
import rows
import feedparser
import urllib.parse
import tqdm
import geopy
import time
from geopy.geocoders import GoogleV3, Nominatim, DataBC
import json

JOBURL ="https://www.jobbank.gc.ca/jobsearch/feed/jobSearchRSSfeed?fage=2&empl={}&sort=D&rows=100"

file = sys.argv[1]

results = rows.import_from_csv(file)
l = []

def job(i, employer):
    employer = r.employer
    feed = urllib.parse.quote_plus(employer)
    url = JOBURL.format(feed)
    resp = feedparser.parse(url)
    joblen = len(resp["entries"])
    i.update({'jobs': joblen, 'joburl': 'https://www.jobbank.gc.ca/jobsearch/jobsearch?empl=' + feed })

def loc(i, employer):
    print(employer)
    if employer.strip():
        res = geolocator.geocode(employer)
        if res:
            print(res.raw)
            i.update({'latitude': res.latitude, 'longitude': res.longitude})


geolocator = DataBC()

for r in tqdm.tqdm(results[:]):
    i = r._asdict()
    loc(i, i.get("address"))
    l.append(i)
table = rows.import_from_dicts(l)
rows.export_to_csv(table, file +".loc.csv")



