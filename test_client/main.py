import asyncio
import websockets
import json


class VEXData:
    def __init__(self, bumper_switch: bool, grabber_angle: float, arm_angle: float, infrared_distance: float, heading: float):
        self.bumper_switch = bumper_switch
        self.grabber_angle = grabber_angle
        self.arm_angle = arm_angle
        self.infrared_distance = infrared_distance
        self.heading = heading


async def test():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to server. Type messages to send (Ctrl+C to quit)")

        # send test data to server
        test_data = VEXData(
            bumper_switch=True,
            grabber_angle=0.5,
            arm_angle=0.8,
            infrared_distance=10.0,
            heading=90.0
        )
        await websocket.send(json.dumps(test_data.__dict__))

        # Task to receive messages
        async def receive_messages():
            while True:
                try:
                    msg = await websocket.recv()
                    print(f"Received: {msg}")
                except websockets.exceptions.ConnectionClosed:
                    print("Connection closed")
                    break

        # Start receive task
        receive_task = asyncio.create_task(receive_messages())

        # Send user input
        try:
            while True:
                user_input = await asyncio.get_event_loop().run_in_executor(
                    None, input, "Send: "
                )
                await websocket.send(user_input)
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            receive_task.cancel()

asyncio.run(test())
