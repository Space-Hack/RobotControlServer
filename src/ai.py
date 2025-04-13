import os
from openai import OpenAI
from my_types import AIInput
import json



async def send_data_to_openai(system_prompt: str, ai_data: AIInput) -> str:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    print(f"Sending data to OpenAI: {system_prompt}")
    print(f"AI Data: {ai_data}")


    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
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
