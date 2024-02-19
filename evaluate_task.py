import json
import re
import time
import pandas as pd
from get_completion import get_completion_zero_shot
from get_completion import get_completion_few_shots


class Task:
        def __init__(self, type, json_string, system_prompt):
                self.type = type
                self.json_string = json_string
                self.system_prompt = system_prompt

        def evaluate(self, model, suffix, shots):
                if self.type == "multiple_choice":
                        return evaluate_multiple_choice_task(self.json_string, self.system_prompt, model, shots, suffix)
                elif self.type == "free_response":
                        return evaluate_free_response_task(self.json_string, self.system_prompt, model, shots, suffix)
                else:
                        raise Exception("Task not supported, check the type of the task.")                

def built_system_message(system_prompt, suffix, example):
        system_prompt = system_prompt + " " + suffix + "\nChoices: \n "
        for choice in example.get("target_scores", {}).keys():
            system_prompt = system_prompt + "-" + choice + "\n"
        return system_prompt 
                  
def evaluate_free_response_task(json_string, system_prompt, model, shots, suffix):
        df = pd.DataFrame(columns=['prompt','expected', 'answer', 'explanation', 'correct'])
        with open(json_string, 'r') as file:
                data = json.load(file)
                examples_selected = data.get("examples", [])
                shots_selected = data.get("shots", [])[:shots]
        for example in examples_selected:
                prompt = example.get("input")
                expected = example.get("target")
                response = None
                answer = None
                explanation = None
                new_system_message = system_prompt + " " + suffix

                try:
                        if shots == 0: 
                                response = get_completion_zero_shot(new_system_message, prompt, model)
                        else:
                                response = get_completion_few_shots(new_system_message, prompt, model, shots_selected)
                except Exception as e:
                        print("Completion Exception in example: ", example)
                        time.sleep(60)
                        if shots == 0: 
                                response = get_completion_zero_shot(new_system_message, prompt, model)
                        else:
                                response = get_completion_few_shots(new_system_message, prompt, model, shots_selected)
                finally:                
                        if response is not None :
                                if response.__contains__("\n"):
                                        re.sub("\n+", "\n", response)
                                        explanation, answer = response.rsplit("\n", 1)
                                        answer = answer.replace(' ', '')
                                        correct = expected.lower() in answer.lower()
                                else :
                                        answer = response.replace(' ', '')
                                        explanation = "No explanation provided"
                                        correct = expected.lower() in answer.lower()
                        else :
                                correct = False       
                df.loc[len(df.index)] = [prompt, expected, answer, explanation,  correct]
        accuracy = df['correct'].mean()
        return round(accuracy, 2) , df      

def evaluate_multiple_choice_task(json_string, system_prompt, model, shots, suffix):   
        df = pd.DataFrame(columns=['prompt','expected', 'answer', 'explanation', 'correct'])
        with open(json_string, 'r') as file:
                data = json.load(file)
                examples_selected = data.get("examples", [])
                shots_selected = data.get("shots", [])[:shots]

        for example in examples_selected:
                prompt = example.get("input")
                expected = [k for k, v in example['target_scores'].items() if v == 1][0]
                response = None
                answer = None
                explanation = None
                new_system_message = built_system_message(system_prompt, suffix, example)

                try:
                        if shots == 0: 
                                response = get_completion_zero_shot(new_system_message, prompt, model)
                        else:
                                response = get_completion_few_shots(new_system_message, prompt, model, shots_selected)
                except Exception as e:
                        print("Completion Exception in example: ", example)
                        time.sleep(60)
                        if shots == 0: 
                                response = get_completion_zero_shot(new_system_message, prompt, model)
                        else:
                                response = get_completion_few_shots(new_system_message, prompt, model, shots_selected)
                finally:        
                        if response is not None :        
                                if response.__contains__("\n"):
                                        re.sub("\n+", "\n", response)
                                        explanation, answer = response.rsplit("\n", 1)
                                        correct = expected.lower() in answer.lower()
                                else :
                                        answer = response
                                        explanation = "No explanation provided"
                                        correct = expected.lower() in answer.lower() 
                        else : 
                                correct = False    
                df.loc[len(df.index)] = [prompt, expected, answer, explanation,  correct]  
        accuracy = df['correct'].mean()
        return round(accuracy, 2) , df
        
