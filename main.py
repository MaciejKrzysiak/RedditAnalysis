import psaw
import json
import re
import datetime as dt
from psaw import PushshiftAPI

api = PushshiftAPI()

data = ""
with open('currencies.json') as f:
    data = json.load(f)

tickers = list(data.keys())
currencies = list(data.values())

start_epoch=int(dt.datetime(2017, 1, 1).timestamp())

submissions = list(api.search_submissions(after=start_epoch,
                            subreddit='cryptocurrency',
                            filter=['title'],
                            limit=1000))

counts = [0] * len(tickers)
for submission in submissions:
    words = submission.title.split()
    for word in words:
        trimmed = re.sub('[\W_]+', '', word).upper()
        pos = -1
        if (trimmed in tickers):
            pos = tickers.index(trimmed)
            counts[pos] = counts[pos] + 1
        elif (trimmed in currencies):
            pos = currencies.index(trimmed)
            counts[pos] = counts[pos] + 1

output = dict()
for i in range(len(counts)):
    output[tickers[i]] = counts[i]

print(sorted(output.items(), key=lambda item: item[1], reverse=True)) 
