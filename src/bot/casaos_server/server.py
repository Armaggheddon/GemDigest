import asyncio
from aiohttp import web

async def start_casaos_alive_server():
    
    app = web.Application(loop = asyncio.get_event_loop())
    app.add_routes([web.get("/", lambda x: web.Response(status=200))])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080, reuse_port=True)
    await site.start()
    print(f"Server started at http://{site._host}:{site._port}")
    while True:
        # keep the server running forever
        await asyncio.sleep(3600)
