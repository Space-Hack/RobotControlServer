import json
from my_types import VEXData, AIInput, ControlData
from positions import get_position


def input_to_object(input_data: str) -> VEXData:
    try:
        json_input_data = json.loads(input_data)
        vex_data = VEXData(
            bumper_switch=json_input_data.get('bumper_switch', None),
            grabber_angle=json_input_data.get('grabber_angle', None),
            arm_angle=json_input_data.get('arm_angle', None),
            infrared_distance=json_input_data.get('infrared_distance', None),
            heading=json_input_data.get('heading', None)
        )

        if any(value is None for value in vars(vex_data).values()):
            raise ValueError("One or more required fields are missing or None")

        return vex_data
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON string provided", input_data)


def grabber_angle_to_grabber_width(grabber_angle: float) -> float:
    return (grabber_angle / 180) * 100


def grabber_width_to_grabber_angle(grabber_width: float) -> float:
    return (grabber_width / 100) * 180


def arm_angle_to_grabber_height(grabber_angle: float) -> float:
    return (grabber_angle / 180) * 50


def grabber_height_to_arm_angle(grabber_height: float) -> float:
    return (grabber_height / 50) * 180


def parse_vex_data_string_to_ai_input(vex_data_string: str, client_id: str) -> AIInput:
    vexData: VEXData = input_to_object(vex_data_string)
    position = get_position(client_id)

    ai_input = AIInput(
        position=position,
        distance_to_object=vexData.infrared_distance,
        has_object=vexData.bumper_switch,
        grabber_height=arm_angle_to_grabber_height(vexData.arm_angle),
        grabber_width=grabber_angle_to_grabber_width(vexData.grabber_angle),
    )

    return ai_input


def parse_ai_response_to_vex_data(ai_response: ControlData) -> ControlData:
    if ai_response.action == "GRABBER_HIGHT":
        return ControlData(
            action="GRABBER_HIGHT",
            param=grabber_height_to_arm_angle(ai_response.param)
        )
    elif ai_response.action == "GRABBER_WIDTH":
        return ControlData(
            action="GRABBER_WIDTH",
            param=grabber_width_to_grabber_angle(ai_response.param)
        )
    else:
        return ai_response
