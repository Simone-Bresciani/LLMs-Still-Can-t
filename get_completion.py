import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path=".env")

def get_completion_zero_shot(system, prompt, model):
    #if the model is the 3.5 turbo, I use my personal free api key, otherwise I use the one of the organization
    if(model == "gpt-3.5-turbo-1106"):
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_3.5"))
    else:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_3.5"), organization = "org-FwcUlxzfJx5sO1h5F3lxshSC")
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system },
                  {"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content