import sys
import rows
import feedparser
import urllib.parse
import tqdm

JOBURL ="https://www.jobbank.gc.ca/jobsearch/feed/jobSearchRSSfeed?fage=2&empl={}&sort=D&rows=100"

file = sys.argv[1]

results = rows.import_from_csv(file)
l = []
for r in tqdm.tqdm(results[:]):
    i = r._asdict()
    employer = r.employer
    feed = urllib.parse.quote_plus(employer)
    url = JOBURL.format(feed)
    resp = feedparser.parse(url)
    joblen = len(resp["entries"])
    i.update({'jobs': joblen, 'joburl': 'https://www.jobbank.gc.ca/jobsearch/jobsearch?empl=' + feed })
    l.append(i)
table = rows.import_from_dicts(l)
rows.export_to_csv(table, file +".joburl.csv")



