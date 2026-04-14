from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "data.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {"cpp": 0, "py": 0, "other": 0}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {"cpp": 0, "py": 0, "other": 0}

@app.get("/stats")
def get_stats():
    return load_data()

@app.post("/vote/{lang}")
def vote(lang: str):
    data = load_data()
    if lang in data:
        data[lang] += 1
        with open(DB_FILE, "w") as f:
            json.dump(data, f)
    return data

@app.get("/")
def read_root():
    return {"status": "ok"}
