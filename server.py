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

# ТВОИ ДАННЫЕ (ПРОВЕРЬ ИХ ЕЩЕ РАЗ)
BIN_ID = "69de928faaba882197fc0e3c"
API_KEY = "$2a$10$sUJFDsOxThEtWfadAfSJauzsmVzXTAM3K0xNdYbQvDGbQeO3iN1Py" # Должен начинаться с $2a$10$

URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
# ВАЖНО: Добавляем заголовок Content-Type
HEADERS = {
    "X-Master-Key": API_KEY,
    "Content-Type": "application/json"
}

def load_data():
    try:
        response = requests.get(URL, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("record", {"cpp": 0, "py": 0, "other": 0})
        else:
            print(f"Ошибка загрузки: {response.status_code} - {response.text}")
            return {"cpp": 0, "py": 0, "other": 0}
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return {"cpp": 0, "py": 0, "other": 0}

def save_data(data):
    try:
        # Для сохранения используем PUT и отправляем данные напрямую
        response = requests.put(URL, json=data, headers=HEADERS)
        if response.status_code != 200:
            print(f"Ошибка сохранения: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Ошибка сети при сохранении: {e}")

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
    return {"status": "backend is running"}
