import json
import asyncio
import websockets
from socketHandler import register, unregister, robots
from parser import parse_vex_data_string_to_ai_input
from my_types import VEXData, AIInput, ControlData
from ai import send_data_to_openai
from websockets.legacy.server import WebSocketServerProtocol


async def handle_message(websocket: WebSocketServerProtocol, message: str):
    ai_input: AIInput = parse_vex_data_string_to_ai_input(message)

    robot = next(
        (robot for robot in robots if robot.get_websocket() == websocket), None)
    # check if robots has a system prompt
    if robot is None or robot.get_system_prompt() is None:
        print("No system prompt found for robot")
        return

    ai_response: ControlData = await send_data_to_openai(robot.get_system_prompt(), ai_input)

    try:
        ai_json_response = json.loads(ai_response)
        print(f"JSON Response: {ai_json_response}")

        command = f"{ai_json_response["action"]} {ai_json_response["param"]}"
        print(f"Command: {command}")
        await websocket.send(command)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {ai_response}")


async def handle_client(websocket: WebSocketServerProtocol):
    print("Client connected")
    await register(websocket)
    try:
        async for message in websocket:
            await handle_message(websocket, message)

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        await unregister(websocket)
