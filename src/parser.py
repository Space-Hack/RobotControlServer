import json
from my_types import VEXData, AIInput, ControlData


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
    # Mapping grabber angle [0, 30] to grabber width [9, 0]
    grabber_angle_min = 0
    grabber_angle_max = 30
    grabber_width_min = 9
    grabber_width_max = 0

    # Linear transformation
    grabber_width = ((grabber_angle - grabber_angle_min) / (grabber_angle_max -
                     grabber_angle_min)) * (grabber_width_max - grabber_width_min) + grabber_width_min
    return grabber_width


def grabber_width_to_grabber_angle(grabber_width: float) -> float:
    # Inverse of the grabber angle to grabber width mapping
    grabber_angle_min = 0
    grabber_angle_max = 30
    grabber_width_min = 9
    grabber_width_max = 0

    # Inverse linear transformation
    grabber_angle = ((grabber_width - grabber_width_min) / (grabber_width_max -
                     grabber_width_min)) * (grabber_angle_max - grabber_angle_min) + grabber_angle_min
    return grabber_angle


def arm_angle_to_grabber_height(arm_angle: float) -> float:
    # Mapping arm angle [-200, 100] to grabber height [33, 8]
    arm_angle_min = -200
    arm_angle_max = 100
    grabber_height_min = 33
    grabber_height_max = 8

    # Linear transformation
    grabber_height = ((arm_angle - arm_angle_min) / (arm_angle_max - arm_angle_min)
                      ) * (grabber_height_max - grabber_height_min) + grabber_height_min
    return grabber_height


def grabber_height_to_arm_angle(grabber_height: float) -> float:
    # Inverse of the previous mapping
    arm_angle_min = -200
    arm_angle_max = 100
    grabber_height_min = 33
    grabber_height_max = 8

    # Inverse linear transformation
    arm_angle = ((grabber_height - grabber_height_min) / (grabber_height_max -
                 grabber_height_min)) * (arm_angle_max - arm_angle_min) + arm_angle_min
    return arm_angle


def parse_vex_data_string_to_ai_input(vex_data_string: str) -> AIInput:
    vexData: VEXData = input_to_object(vex_data_string)

    ai_input = AIInput(
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
