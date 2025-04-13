import asyncio
import websockets

from worker import handle_client

from dotenv import load_dotenv

load_dotenv()


async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("🟢 WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
