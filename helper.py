import asyncio
import sys
import math

from aiohttp import ClientOSError
import aiohttp

players = {}

level_table = [
            0, 46, 99, 159, 229,
            309, 401, 507, 628, 768,
            928, 1112, 1324, 1567, 1847,
            2168, 2537, 2961, 3448, 4008,
            4651, 5389, 6237, 7212, 8332,
            9618, 11095, 12792, 14742, 16982,
            19555, 22510, 25905, 29805, 34285,
            39431, 45342, 52132, 59932, 68892,
            79184, 91006, 104586, 120186, 138106,
            158690, 182335, 209496, 240696, 276536,
            317705, 364996, 419319, 481720, 553400,
            635738, 730320, 838966, 963768, 1107128,
            1271805, 1460969, 1678262, 1927866, 2214586,
            2543940, 2922269, 3356855, 3856063, 4429503,
            5088212, 5844870, 6714042, 7712459, 8859339,
            10176758, 11690075, 13428420, 15425254, 17719014,
            20353852, 23380486, 26857176, 30850844, 35438364,
            40708040, 46761308, 53714688, 61702024, 70877064,
            81416417, 93522954, 107429714, 123404386, 141754466,
            162833172, 187046247, 214859767, 246809111, 283509271,
            325666684, 374092835, 429719875, 493618564, 567018884,
            651333710, 748186012, 859440093, 987237472, 1134038112,
            1302667765, 1496372370, 1718880532, 1974475291, 2268076571,
            2605335878, 2992745089, 3437761413, 3948950932, 4536153492,
            5210672106, sys.maxsize
        ]
ranking_modes = {
            'melee': 'highscores-melee',
            'magic': 'highscores-magic',
            'mining': 'highscores-mining',
            'smithing': 'highscores-smithing',
            'woodcutting': 'highscores-woodcutting',
            'crafting': 'highscores-crafting',
            'fishing': 'highscores-fishing',
            'cooking': 'highscores-cooking',
            'tailoring': 'highscores-tailoring'
        }
url = 'https://www.curseofaros.com'



def block(text,tag):
    text = f"<{tag}>{text}</{tag}>"
    return text
    
def get_rank(player,rank):
    op = f"[{rank}] {player}"
    return op
    
def format_tier(tier,players_list,last_rank):
    last_rank=last_rank
    tier = "Special" if tier == 0 else (11-tier)
    tier_txt = f"Tier {tier} :"
    code = block(block(tier_txt,"b"),"br")
    for player in players_list:
        rank = players_list.index(player) + 1
        code = code + ( get_rank(player,rank) if rank%2==1 else block(get_rank(player,rank),"br") )
    code = block(code,"p")
    return code, last_rank
