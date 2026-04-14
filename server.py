from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# –азрешаем запросы с любого адреса (в том числе с GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "data.json"

# »нициализаци€ базы данных
def load_data():
    if not os.path.exists(DB_FILE):
        return {"cpp": 0, "py": 0, "other": 0}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

@app.get("/stats")
async def get_stats():
    return load_data()

@app.post("/vote/{lang}")
async def vote(lang: str):
    data = load_data()
    if lang in data:
        data[lang] += 1
        save_data(data)
    return data