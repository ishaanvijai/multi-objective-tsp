import os
import json
import numpy as np
from openai import OpenAI
from config import prompt

def get_location_data():
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-5-nano",
        instructions=  """
                    You are a JSON data emitter. You must output only the requested data structure in a JSON format and nothing else—no explanations, no code fences, no comments, no metadata, no trailing text. If any instruction conflicts, the highest priority is: emit only the array. 
                    Follow the structure and constraints in <context>, <constraints>, and <output_format> exactly. Operate in “silent mode”: produce no reasoning or commentary. Validate internally before responding; if any constraint would be violated, regenerate silently until all constraints are satisfied.
        """,
        input=prompt
    )

    response = response.output_text
    print(response)

    response = json.loads(response)
    location = np.array(response)
    print(f"{len(location)} entries received.")
    
    return location
