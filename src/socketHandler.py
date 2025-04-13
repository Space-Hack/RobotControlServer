#!/usr/bin/env python3

import asyncio

from typing import Dict
from websockets.legacy.server import WebSocketServerProtocol


connected_clients: Dict[WebSocketServerProtocol, str] = {}


def get_client_id(websocket: WebSocketServerProtocol) -> str:
    return connected_clients.get(websocket, "Unknown")


async def register(websocket):
    addr = websocket.remote_address
    connected_clients[websocket] = f"{addr[0]}:{addr[1]}"
    print(f"[+] {connected_clients[websocket]} connected")


async def unregister(websocket):
    name = connected_clients.get(websocket, "Unknown")
    connected_clients.pop(websocket, None)
    print(f"[-] {name} disconnected")


async def notify_all(message):
    if connected_clients:
        await asyncio.gather(
            *[ws.send(message) for ws in connected_clients],
            return_exceptions=True  # Prevent one broken client from crashing all
        )
