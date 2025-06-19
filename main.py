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

# Helper function to fetch matchup data (limited by API capability)
def fetch_matchup_data(pitcher_id: int, batter_id: int):
    url = f"https://statsapi.mlb.com/api/v1/people/{pitcher_id},{batter_id}/stats?stats=vsPlayer"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Unable to fetch data"}

# Example endpoint for a pitcher vs. batter matchup
@app.get("/matchup/{pitcher_id}/{batter_id}")
def get_matchup(pitcher_id: int, batter_id: int):
    data = fetch_matchup_data(pitcher_id, batter_id)
    return data
