class VEXData:
    def __init__(self, bumper_switch: bool, grabber_torque: float, arm_torque: float, infrared_distance: float, heading: float):
        self.bumper_switch = bumper_switch
        self.grabber_torque = grabber_torque
        self.arm_torque = arm_torque
        self.infrared_distance = infrared_distance
        self.heading = heading


class AIInput:
    def __init__(self, has_object: bool, grabber_width: float, grabber_height: float, distance_to_object: float, position: dict):
        self.has_object = has_object
        self.grabber_width = grabber_width
        self.grabber_height = grabber_height
        self.distance_to_object = distance_to_object
        self.position = position


class AIResponse:
    def __init__(self, action: str, param: float):
        self.action = action
        self.param = param
