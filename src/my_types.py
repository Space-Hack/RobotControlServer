class VEXData:
    def __init__(self, bumper_switch: bool, grabber_angle: float, arm_angle: float, infrared_distance: float, heading: float):
        self.bumper_switch = bumper_switch
        self.grabber_angle = grabber_angle
        self.arm_angle = arm_angle
        self.infrared_distance = infrared_distance
        self.heading = heading


class AIInput:
    def __init__(self, has_object: bool, grabber_width: float, grabber_height: float, distance_to_object: float):
        self.has_object = has_object
        self.grabber_width = grabber_width
        self.grabber_height = grabber_height
        self.distance_to_object = distance_to_object


class ControlData:
    def __init__(self, action: str, param: float):
        self.action = action
        self.param = param
