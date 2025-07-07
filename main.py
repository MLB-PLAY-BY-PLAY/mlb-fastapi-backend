from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root endpoint — this keeps Render happy!
@app.get("/")
def read_root():
    return {"message": "API is running. Use /player/{player_id}."}

# Fetch player stats
def fetch_player_stats(player_id: int):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=career"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch data"}

@app.get("/player/{player_id}")
def get_player(player_id: int):
    data = fetch_player_stats(player_id)
    return data
