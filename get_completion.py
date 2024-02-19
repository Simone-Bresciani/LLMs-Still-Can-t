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

def get_completion_few_shots(system, prompt, model, shots_selected):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_4.0"), organization = "org-FwcUlxzfJx5sO1h5F3lxshSC")
    messages = []
    #firt the system message
    messages.append({"role": "system", "content": system})
    #then the shots examples divided by user(the question) and assistant(the answer)
    for shot in shots_selected:
        messages.append({"role": "user", "content": shot.get("input")})
        if "target" in shot: 
            messages.append({"role": "assistant", "content": shot.get("target")})
        elif "target_scores" in shot:
            target = [k for k, v in shot['target_scores'].items() if v == 1][0]
            messages.append({"role": "assistant", "content": target })
        else :
            raise Exception("Invalid shot format")
    #finally the user prompt(the question)
    messages.append({"role": "user", "content": prompt})
    #the actual call to the API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content

    