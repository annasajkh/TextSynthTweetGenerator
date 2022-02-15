import requests
import json
import os
from requests.models import Response

def generate_tweet(username : str, tweet_text : str) -> str:
  headers= {
      "Authorization": os.environ["api_key"]
  }

  payload : dict  = {
      "prompt": tweet_text,
      "temperature": 0.8,
      "top_k": 40, 
      "top_p": 1.0, 
      "seed": 0,
      "stop": "\n"
    }
    
  resp : Response = requests.post("https://api.textsynth.com/v1/engines/gptj_6B/completions",data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers=headers)

  text = json.loads(resp.text)["text"]

  return "\n".join([f"<p>@{username} {tweet}</p>" for tweet in text.split("\n")])