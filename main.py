import aiohttp
from fastapi import FastAPI
from helper import *
from db_helper import *


app = FastAPI()
url="https://www.curseofaros.com/highscores-melee.json?p=0"
tiers = { "1": 8000000,"2": 16000000,"3": 32000000,"4": 40000000,
        "5": 56000000,"6": 64000000,"7": 80000000,"8": 112000000,
        "9":180000000,"10":200000000}

async def rankings_search(name):
    return await rank_search_helper([mode for mode in ranking_modes.keys()], name)

def get_tiers():
    tier1 = []
    tier2 = []
    tier3 = []
    tier4 = []
    tier5 = []
    tier6 = []
    tier7 = []
    tier8 = []
    tier9 = []
    tier10 = []
    tierS = []
    tiers_list = [tier1,tier2,tier3,tier4,tier5,tier6,tier7,tier8,tier9,tier10,tierS]
    total_xp = 0
    xp_gains = retrieve("4444")
    xp_gains = {k: v for k, v in sorted(xp_gains.items(), key=lambda item: item[1],reverse=True)}
    for player in xp_gains :
        current_tier = ""
        for tier in tiers:
            if "69420" in str(xp_gains[player]):
                current_tier="11"
                break
            elif xp_gains[player]>=tiers[tier]:
                current_tier = tier
                pass
            elif xp_gains[player]<tiers[tier]:
                break
        total_xp += xp_gains[player]
        rank = player + " --- " + "{:,}". format(xp_gains[player])
        tiers_list[int(current_tier)].append(rank)
    return tiers_list, total_xp

@app.get("/")
async def root():
    async with aiohttp.ClientSession() as session:
        response =  await session.get(url)
        data = await response.json()
    return data
@app.get("/login")
def login():
    return {"username": "password"}

@app.get("/users")
async def search(username:str):
    results = await rank_search_helper([mode for mode in ranking_modes.keys()], username.replace("-"," "))
    return results

    
@app.get("/event")
async def show_tiers():
    results = get_tiers()
    total_xp = results[1]
    tiers_list = total_xp[0]
    current_rank = 0
    ranking = f"Total XP gained : {total_xp}" + "\n \n \n"
    if len(tiers_list[10])>0:
        ranking = ranking + "Special Tier : "
        for player in tiers_list[10]:
            ranking = ranking + "\n" + player
    for i in range(9,-1,-1):
        ranking = ranking + f"\n\nTier {i+1} : "
        for player in tiers_list[i]:
            current_rank += 1
            ranking = ranking + f"\n[{current_rank}] {player}"
    
    return ranking
