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
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CERT_PATH = os.path.join(BASE_DIR, "certs", "cert.pem")
    KEY_PATH = os.path.join(BASE_DIR, "certs", "cert-key.pem")

    # Start API server
    config = uvicorn.Config(app, host="0.0.0.0", port=443, ssl_keyfile=KEY_PATH, ssl_certfile=CERT_PATH)
    server = uvicorn.Server(config)
    
    # Run both servers concurrently
    await asyncio.gather(
        websocket_server,
        server.serve()
    )

if __name__ == "__main__":
    asyncio.run(main())
