from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running. Use /player/{player_id} or /matchup/{pitcher_id}/{batter_id}"}

# Player stats
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

# ✅ NEW: Pitcher vs Batter matchup stats
def fetch_matchup_stats(pitcher_id: int, batter_id: int):
    url = (
        f"https://statsapi.mlb.com/api/v1/people/{batter_id}/stats"
        f"?stats=vsPlayer&opposingPlayerId={pitcher_id}"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch matchup data"}

@app.get("/matchup/{pitcher_id}/{batter_id}")
def get_matchup(pitcher_id: int, batter_id: int):
    data = fetch_matchup_stats(pitcher_id, batter_id)
    return data
