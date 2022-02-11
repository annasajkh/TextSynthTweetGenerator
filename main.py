import os
os.system("pip3 install --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint")
os.system("pip3 uninstall dataclasses -y")

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse


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
    return util.generate_tweet(username)
  except Exception as e:
    return f"<p>{e}</p>"

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)