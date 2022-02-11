from typing import List

from twint import output, tweet
import twint
import re
import requests
import json
import os
import time
from requests.models import Response


def get_tweet(username : str) -> str:
  config : twint.Config = twint.Config()
  config.Username = username
  config.Filter_retweets = True
  config.Store_object = True
  config.Hide_output = True

  twint.run.Search(config)

  tweets : List[tweet.tweet] = output.tweets_list
  result : str = ""

  print(f"scraped: {len(tweets)}")

  for t in tweets:
    if "@" in t.tweet:
      continue

    text = re.sub("https://(.*)", "", t.tweet)
    text = re.sub("\n", " ", text).strip()

    if text.strip() != "":
      result += f"@{username} {text}\n"
  
  return result + f"@{username}"

def generate_tweet(username : str) -> str:
  tweets = get_tweet(username)
  tweets = "\n".join(list(set(tweets.split("\n"))))
  
  tweet_text : str = f"this is tweets from @{username}\n" + tweets

  print(tweet_text)
  
  headers= {
      "Authorization": os.environ["api_key"]
  }

  payload : dict  = {
      "prompt": tweet_text,
      "temperature": 1.0,
      "top_k": 40, 
      "top_p": 1.0, 
      "seed": 0,
      "stop": "\n"
    }
    
  resp : Response = requests.post("https://api.textsynth.com/v1/engines/gptj_6B/completions",data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers=headers)

  text = json.loads(resp.text)["text"]

  return "\n".join([f"<p>@{username} {tweet}</p>" for tweet in text.split("\n")])