import json
from my_types import VEXData, AIInput
from positions import get_position


def input_to_object(input_data: str) -> VEXData:
    try:
        json_input_data = json.loads(input_data)
        vex_data = VEXData(
            bumper_switch=json_input_data.get('bumper_switch', None),
            grabber_torque=json_input_data.get('grabber_torque', None),
            arm_torque=json_input_data.get('arm_torque', None),
            infrared_distance=json_input_data.get('infrared_distance', None),
            heading=json_input_data.get('heading', None)
        )

        if any(value is None for value in vars(vex_data).values()):
            raise ValueError("One or more required fields are missing or None")

        return vex_data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON string provided", input_data)


def parse_vex_data_string_to_ai_input(vexDataString: str, client_id: str) -> AIInput:
    vexData: VEXData = input_to_object(vexDataString)
    position = get_position(client_id)

    ai_input = AIInput(
        position=position,
        distance_to_object=vexData.infrared_distance,
        has_object=vexData.bumper_switch,
        grabber_height=None,
        grabber_width=None,
    )

    return ai_input
