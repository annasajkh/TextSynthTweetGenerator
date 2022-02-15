import os
os.system("pip3 install --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint")
os.system("pip3 uninstall dataclasses -y")

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from multiprocessing.pool import ThreadPool

from typing import List

from twint import output, tweet
import twint
import re
import time
import json
import re

import uvicorn
import util


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
  return "Alive"

@app.get("/{username}", response_class=HTMLResponse)
def generate(username):
  try:
    config : twint.Config = twint.Config()
    config.Username = username
    config.Filter_retweets = True
    config.Store_object = True
    config.Hide_output = True

    twint.run.Search(config)

    result : str = ""
    
    tweets = output.tweets_list
    
    print(f"scraped: {len(tweets)}")
    
    for t in tweets:
      if "@" in t.tweet or username.lower().strip() != t.username.strip():
        continue
    
      text = re.sub("https://(.*)", "", t.tweet)
      text = re.sub("\n", " ", text).strip()
      
      if text.strip() != "":
        result += f"@{username} {text}\n"
    
    r = "\n".join(list(set(result.split("\n")))) + f"\n@{username}"
    print(r)
    return util.generate_tweet(username, f"this is tweets from @{username}\n" + r)
    os.system("rm tweets.json")
  except Exception as e:
    return f"<p>{e}</p>"

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)