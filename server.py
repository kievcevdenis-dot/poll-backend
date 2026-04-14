from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


BIN_ID = "69de928faaba882197fc0e3c"
API_KEY = "$2a$10$sUJFDsOxThEtWfadAfSJauzsmVzXTAM3K0xNdYbQvDGbQeO3iN1Py"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY}

def load_data():
    try:
        response = requests.get(URL, headers=HEADERS)
        return response.json()["record"]
    except:
        return {"cpp": 0, "py": 0, "other": 0}

def save_data(data):
    requests.put(URL, json=data, headers=HEADERS)

@app.get("/stats")
def get_stats():
    return load_data()

@app.post("/vote/{lang}")
def vote(lang: str):
    data = load_data()
    if lang in data:
        data[lang] += 1
        save_data(data)
    return data

@app.get("/")
def read_root():
    return {"status": "connected to cloud"}
