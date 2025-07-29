import asyncio

print_lock = asyncio.Lock()


async def async_print(*args, **kwargs):
    async with print_lock:
        print(*args, **kwargs)
