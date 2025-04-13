import os
from openai import OpenAI
from my_types import AIInput
import json

SYSTEM_PROMPT = """
You're a helpful assistant and you're job is to maneuver a mars rover. 
You are provided a json object that encodes all the current stystem states 
and a task objective to complete and find the best next action the robot should take. 
As a response return ONLY a JSON object with the following fields: 
{'action': 'FORWARD' |  'BACKWARD' | 'TURN' | 'GRABBER_HIGHT' | 'GRABBER_WIDTH', 'param': float}"
where param is different for each action:
- FORWARD: the distance to move forward in centimeters
- BACKWARD: the distance to move backward in centimeters
- TURN: the angle to turn in degrees
- GRABBER_HIGHT: the height of the grabber in centimeters
- GRABBER_WIDTH: the width of the grabber in centimeters
"""


async def send_data_to_openai(ai_data: AIInput) -> str:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"The current system state is: {json.dumps(ai_data.__dict__)}"
                }
            ],
        )

        response = completion.choices[0].message.content
        return response.strip().replace("\\n", "").replace("```", "").replace("json", "")

    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return None
