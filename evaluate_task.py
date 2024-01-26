import os
import json
import time
import pandas as pd
from get_completion import get_completion_zero_shot

def evaluate_multiple_choice_task(json_string, system_message, model):    
    

    df = pd.DataFrame(columns=['prompt','expected', 'answer', 'correct'])


    with open(json_string, 'r') as file:
        data = json.load(file)

    for example in data.get("examples", []):
        prompt = example.get("input")
        expected = [k for k, v in example['target_scores'].items() if v == 1][0]
        answer = None
        try:
                answer = get_completion_zero_shot(system_message, prompt, model)
        except Exception as e:
                print("Error in example: ", example)
                print("Exeption: ", e.args[0])
                #mi fermo per 30 secondi
                time.sleep(30)
                #ritento la richiesta
                answer = get_completion_zero_shot(system_message, prompt, model)
        finally:                
                if answer is not None :
                      correct = answer[1:] == expected
                else :
                      correct = False
                df.append({'prompt': prompt, 'answer': answer, 'expected': expected, 'correct': correct}, ignore_index=True)  # type: ignore
    
    return df