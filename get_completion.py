import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=".env")

def get_completion_zero_shot(system, prompt, model):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_4.0"), organization = "org-FwcUlxzfJx5sO1h5F3lxshSC")
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system },
                  {"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content