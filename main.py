import aiohttp
from fastapi import FastAPI
from helper import *


app = FastAPI()
url="https://www.curseofaros.com/highscores-melee.json?p=0"


async def rankings_search(name):
    return await rank_search_helper([mode for mode in ranking_modes.keys()], name)
    

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
