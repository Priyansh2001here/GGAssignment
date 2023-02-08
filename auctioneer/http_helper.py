import asyncio
from datetime import timedelta
from typing import List, Dict
import aiohttp
import asyncio.exceptions

import data_model


async def send_post_request(url: str, data: Dict, session: aiohttp.ClientSession):
    async with session.post(url, json=data) as resp:
        return await resp.json()



async def send_get_request(url: str, data: Dict, session: aiohttp.ClientSession, callback: callable = None,
                           context=None):
    async with await session.get(url, json=data, timeout=0.2) as resp:
        return await resp.json()

# try:
        # task = asyncio.ensure_future(session.get(url, json=data))
        # resp = await asyncio.wait_for(task, timeout=0.2)
        # return await resp.json()
    # except asyncio.TimeoutError as _:
    #     pass


async def trigger_bidders_to_bid(bidders: List[data_model.Bidder]):
    # async with aiohttp.ClientSession() as session:
    #     tasks = []
    #     for bidder in bidders:
    #         url = f"http://{bidder.host}:{bidder.port}/webhook/send_bid"
    #         print(f"sending bid request to {url}")
    #         tasks.append(send_get_request(url, {}, session))
    #     return await asyncio.wait(tasks, timeout=0.2)
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(session.get(f"http://{bidder.host}:{bidder.port}/webhook/send_bid", json={})) for bidder in bidders]
        results = []
        done, pending = await asyncio.wait(tasks, timeout=0.2)
        for task in done:
            resp = task.result()
            if resp is not None:
                results.append(await resp.json())
        return results