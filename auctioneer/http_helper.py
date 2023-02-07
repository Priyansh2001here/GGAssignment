import asyncio
from datetime import timedelta
from typing import List, Dict
import aiohttp
import asyncio.exceptions


async def send_post_request(url: str, data: Dict, session: aiohttp.ClientSession):
    async with session.post(url, json=data) as resp:
        return await resp.json()



async def send_get_request(url: str, data: Dict, session: aiohttp.ClientSession, callback: callable = None,
                           context=None):
    try:
        async with await session.get(url, json=data, timeout=0.2) as resp:
            if callback is not None:
                callback(context['bidder_id'])
            return await resp.json()
    except asyncio.exceptions.TimeoutError:
        pass
