import asyncio
import websockets
import uvicorn

from worker import handle_client
from api import app
from dotenv import load_dotenv

load_dotenv()


async def main():
    # Start WebSocket server
    websocket_server = websockets.serve(handle_client, "localhost", 8765)
    print("🟢 WebSocket server running at ws://localhost:8765")
    
    # Start API server
    config = uvicorn.Config(app, host="localhost", port=8000)
    server = uvicorn.Server(config)
    
    # Run both servers concurrently
    await asyncio.gather(
        websocket_server,
        server.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())
