import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ПРОВЕРЬ ЭТИ ДВЕ СТРОЧКИ:
BIN_ID = "69de928faaba882197fc0e3c"
API_KEY = "$2a$10$sUJFDsOxThEtWfadAfSJauzsmVzXTAM3K0xNdYbQvDGbQeO3iN1Py"

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {"X-Master-Key": API_KEY, "Content-Type": "application/json"}

def load_data():
    try:
        res = requests.get(URL, headers=HEADERS)
        data = res.json().get("record", {})
        # Если база пустая, возвращаем заготовку
        if "py" not in data:
            return {"cpp": 0, "py": 0, "other": 0}
        return data
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
    else:
        data[lang] = 1
    save_data(data)
    return data

@app.get("/")
def home():
    return {"status": "ok"}
