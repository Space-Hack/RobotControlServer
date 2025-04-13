#!/usr/bin/env python3

import asyncio

from typing import Dict
from websockets.legacy.server import WebSocketServerProtocol


class Robot:
    def __init__(self, websocket: WebSocketServerProtocol):
        self.websocket = websocket

        self.system_prompt = None

    def attach_task(self, name: str, task_objective: str):
        self.name = name
        self.system_prompt = f"""
You're a helpful assistant and you're job is to maneuver a mars rover. 
The task of the robot is to {task_objective}.
You are provided a json object that encodes all the current stystem states 
and a task objective to complete and find the best next action the robot should take. 
As a response return ONLY a JSON object with the following fields: 
{{ 'action': 'FORWARD' |  'BACKWARD' | 'TURN' | 'GRABBER_HEIGHT' | 'GRABBER_WIDTH', 'param': float }}
where param is different for each action:
- FORWARD: the distance to move forward in centimeters
- BACKWARD: the distance to move backward in centimeters
- TURN: the angle to turn in degrees from -180 to 180
- GRABBER_HIGHT: the height of the grabber in centimeters
- GRABBER_WIDTH: the width of the grabber in centimeters
"""

    def get_name(self) -> str:
        return self.name

    def get_system_prompt(self) -> str:
        return self.system_prompt

    def get_websocket(self) -> WebSocketServerProtocol:
        return self.websocket


robots = []


async def register(websocket):
    robots.append(Robot(websocket))


async def unregister(websocket):
    robots.remove(
        next((robot for robot in robots if robot.get_websocket() == websocket), None))
