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
total_connection_retries = 5

async def get_page_info( link, tries=0):
    if tries > total_connection_retries:
        return None

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(link)
            data = await response.json(content_type=None)
    except ClientOSError:
        return await get_page_info(link, tries + 1)
    except ValueError:
        return None
    else:
        return data

async def set_rank_tasks(mode, name):
        max_page = 80000

        split = math.ceil(max_page / 4)
        tasks = []
        i = 0
        while i < max_page:
            temp = i + split
            mid = (temp + i) // 2
            tasks.append(get_rank_info(mode, name, i, max_page if temp > max_page else mid))
            tasks.append(get_rank_info(mode, name, -max_page if temp > max_page else -temp, -mid))
            i = temp
        done = None
        if tasks:
            done, pending = await asyncio.wait(tasks, timeout=600, return_when=asyncio.FIRST_COMPLETED)
            [p.cancel() for p in pending]
        if done:
            result = done.pop().result()
            #result = (mode,       (       (rank,xp,name),       color)       )
            #mode=result[0]
            #rank=result[1][0][0]
            #xp=result[1][0][1]
            #name=result[1][0][2]
            #color=result[1][1]
            #
            print(f'Rank info found for {name}, {mode}: {result}')
            return result
        else:
            print(f'Rank not info found for {name}, {mode}')
            return (mode, (None, None))

async def get_rank_info(mode, name, start_page=0, end_page=sys.maxsize):
        info = None
        color = None
        resource = ranking_modes[mode]
        found = False
        json_data = await get_page_info(f'{url}/{resource}.json?p={abs(start_page)}')
        page = start_page
        while json_data and not found and page <= end_page:
            j = 0
            while j < len(json_data) and not found:
                player = json_data[j]
                if player['name'].lower() == name:
                    found = True
                    rank = abs(page) * 20 + j + 1
                    info = (rank, player['xp'], player['name'])
                    color = player['name_color'] if player['name_color'] else '99aab5'
                else:
                    j += 1
            page += 1
            json_data = await get_page_info(f'{url}/{resource}.json?p={abs(page)}')

        if not found:
            await asyncio.sleep(600)
        return (mode, (info, color))

def get_level(xp):
    level = 0
    while xp >= level_table[level]:
        level += 1
    return level




async def rank_search_helper( modes, name):
    if len(name) < 3 or len(name) > 14:
        print('Invalid name!')
    name = name.lower()
    rank_mode_sub = [mode for mode in ranking_modes.keys() if mode in modes]
    info = {}
    color = None
    found_name = None
    futures = [set_rank_tasks(mode, name) for mode in rank_mode_sub]
    done, _ = await asyncio.wait(futures)
    for task in done:
        player_ranks = task.result()
        sub_info, temp_color = player_ranks[1]
        if not color and temp_color:
            color = temp_color
        if not found_name and sub_info:
            found_name = sub_info[2]
        info[player_ranks[0]] = sub_info
    return info

