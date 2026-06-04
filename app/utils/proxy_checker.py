import aiohttp
async def get_stable_proxy(proxies):
    for proxy in proxies:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://api.telegram.org",
                    proxy=proxy,
                    timeout=15
                ) as r:
                    if r.status is not None:
                        return proxy
        except:
            pass
    return None

