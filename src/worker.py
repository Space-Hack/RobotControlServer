import json
import asyncio
import websockets
from socketHandler import register, unregister, get_client_id
from parser import parse_vex_data_string_to_ai_input
from my_types import VEXData, AIInput, ControlData
from ai import send_data_to_openai
from websockets.legacy.server import WebSocketServerProtocol


async def handle_message(websocket: WebSocketServerProtocol, message: str, sender: str):
    ai_input: AIInput = parse_vex_data_string_to_ai_input(
        message, sender)

    ai_response: ControlData = await send_data_to_openai(ai_input)

    try:
        ai_json_response = json.loads(ai_response)
        print(f"JSON Response: {ai_json_response}")

        command = f"{ai_json_response["action"]} {ai_json_response["param"]}"
        print(f"Command: {command}")
        await websocket.send(command)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {ai_response}")


def handle_task_result(task):
    try:
        task.result()  # will raise the exception if there was one
    except Exception as e:
        print("Caught exception:", e)


async def handle_client(websocket: WebSocketServerProtocol):
    await register(websocket)
    try:
        async for message in websocket:
            sender = get_client_id(websocket)
            print(f"[{sender}] {message}")
            task = asyncio.create_task(
                handle_message(websocket, message, sender))

            task.add_done_callback(handle_task_result)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)
