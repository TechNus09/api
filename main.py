import aiohttp
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from helper import *
from db_helper import *


app = FastAPI()
url="https://www.curseofaros.com/highscores-melee.json?p=0"
tiers = { "1": 8000000,"2": 16000000,"3": 32000000,"4": 40000000,
        "5": 56000000,"6": 64000000,"7": 80000000,"8": 112000000,
        "9":180000000,"10":200000000}


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
        current_tier = "none"
        for tier in tiers:
            if "69420" in str(xp_gains[player]):
                current_tier="11"
                break
            elif xp_gains[player]>=tiers[tier]:
                current_tier = tier
                pass
            elif xp_gains[player]<tiers[tier]:
                break
        if current_tier != "none":
            rank = player + " --- " + "{:,}". format(xp_gains[player])
            tiers_list[int(current_tier)-1].append(rank)
        total_xp += xp_gains[player]
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
    
@app.get("/event",response_class=HTMLResponse)
async def show_tiers():
    results = get_tiers()
    total_xp = "{:,}".format(results[1])
    tiers_list = results[0]
    code = ""
    current_rank = 0
    total_xp_gained = f"<br><strong>Total XP gained : {total_xp}</strong></b>" 
    code = code + total_xp_gained
    tiers_list.reverse()
    start = 0
    if len(tiers_list[0]) == 0:
        start = 1
    for i in range(start,11):
        f_t = format_tier(i,tiers_list[i],current_rank)
        current_rank = f_t[1]
        code = code + f_t[0]
    code = block(block("Event Leaderboard","title"),"head") + code
    code = block(block(code,"body"),"html")
    return f"""{code}"""
    
