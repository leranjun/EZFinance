import os
from newsapi.newsapi_client import NewsApiClient
from pandas import json_normalize
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import json

my_secret = os.environ['newsapi_key']
newsapi = NewsApiClient(api_key=my_secret)

def top_headlines():
  country="us"
  category="business"
  top_headlines =newsapi.get_top_headlines(category=category,
  language='en',country=country)   
  top_headlines=json_normalize(top_headlines['articles'])   
  newdf=top_headlines[["title","url"]]
  dic=newdf.set_index('title')['url'].to_dict()
  # print(dic)
  # dic["time_stamp_lol"] = str(datetime.datetime.now())
  with open("static/finance_data/news_data.json","w") as file:  
    json.dump(dic, file)
