from typing import List


from twint import output, tweet
import twint
import re
import requests
import json
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
      result += f"tweet: {text}\n"
  
  return result

def generate_tweet(username : str) -> str:
  tweet_text : str = get_tweet(username)

  payload : dict  = {
    "prompt": tweet_text,
    "temperature": 0.9,
    "top_k": 40, 
    "top_p": 0.9, 
    "seed": 0
  }

  resp : Response = requests.post("https://bellard.org/textsynth/api/v1/engines/gptj_6B/completions",data=json.dumps(payload, ensure_ascii=False).encode("utf-8"))

  text = filter(lambda x: x != "",[chunk for chunk in resp.text.split("\n")])
  text = "".join([json.loads(chunk)["text"] for chunk in text]).strip()

  return "\n".join([f"<p>{tweet}</p>" for tweet in text.split("\n")])