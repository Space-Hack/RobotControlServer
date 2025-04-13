from typing import Dict
import math

client_positions: Dict[str, Dict[str, float]] = {}


def get_position(client_id: str) -> Dict[str, float]:
    if client_id not in client_positions:
        client_positions[client_id] = {"x": 0.0, "y": 0.0}

    position = client_positions[client_id]
    return position


def update_position(client_id: str, heading: float, distance: float) -> None:
    if client_id not in client_positions:
        client_positions[client_id] = {"x": 0.0, "y": 0.0}

    position = client_positions[client_id]
    position["x"] += distance * math.sin(math.radians(heading))
    position["y"] += distance * math.cos(math.radians(heading))
