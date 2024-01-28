import os
import json
import random
import re
import time
import pandas as pd
from get_completion import get_completion_zero_shot



N_EXAMPLES = 2
MULTIPLE_CHOICE_SUFFIX = "First answer repeating the answer you choose, in the second line explain your answer in 20 words. Choices:"
FREE_RESPONSE_SUFFIX = "In the first line you answer just the result, in the second line explain your answer in 20 words."

class Task:
        def __init__(self, type, json_string, system_message):
                self.type = type
                self.json_string = json_string
                self.system_message = system_message

        def evaluate(self, model):
                if self.type == "multiple_choice":
                        return evaluate_multiple_choice_task(self.json_string, self.system_message, model)
                elif self.type == "free_response":
                        return evaluate_free_response_task(self.json_string, self.system_message, model)
                else:
                        raise Exception("Task not supported, check the type of the task.")
                

def shrink_examples(data, n):
        examples = data.get("examples", [])
        random.shuffle(examples) # shuffle examples so the difficult ones are not always at the end
        if len(examples) > n:
            examples = random.sample(examples, n) 
        return examples

def built_system_message(system_message, example):
        system_message = system_message + " " + MULTIPLE_CHOICE_SUFFIX
        for choice in example.get("target_scores", {}).keys():
            system_message = system_message + "-" + choice + "\n"
        return system_message 
                  
def evaluate_free_response_task(json_string, system_message, model):
        df = pd.DataFrame(columns=['prompt','expected', 'answer', 'explanation', 'correct'])
        with open(json_string, 'r') as file:
                data = json.load(file)
        
        examples_selected = shrink_examples(data, N_EXAMPLES)
        for example in examples_selected:
                prompt = example.get("input")
                expected = example.get("target")
                response = None
                answer = None
                explanation = None
                new_system_message = system_message + " " + FREE_RESPONSE_SUFFIX

                try:
                        response = get_completion_zero_shot(new_system_message, prompt, model)
                except Exception as e:
                        print("Completion Exception in example: ", example)
                        time.sleep(60)
                        response = get_completion_zero_shot(new_system_message, prompt, model)
                finally:                
                        if response is not None :
                                re.sub("\n+", "\n", response)
                                answer, explanation = response.split("\n", 1)
                                answer = answer.replace(' ', '')
                                correct = answer.__contains__(expected) 
                        else :
                                correct = False       
                df.loc[len(df.index)] = [prompt, expected, answer, explanation,  correct]
        
        result_path = f"results/{json_string.split('/')[1].split('.')[0]}_results.json"       
        df.to_json(result_path, index=True)
        accuracy = df['correct'].mean()
        return round(accuracy, 2)       

def evaluate_multiple_choice_task(json_string, system_message, model):   
        df = pd.DataFrame(columns=['prompt','expected', 'answer', 'explanation', 'correct'])
        with open(json_string, 'r') as file:
                data = json.load(file)

        if(json_string.__contains__("color")):
               examples_selected = shrink_examples(data, N_EXAMPLES//4)
        else:
               examples_selected = shrink_examples(data, N_EXAMPLES)


        for example in examples_selected:
                prompt = example.get("input")
                expected = [k for k, v in example['target_scores'].items() if v == 1][0]
                response = None
                answer = None
                explanation = None
                new_system_message = built_system_message(system_message, example)

                try:
                        response = get_completion_zero_shot(new_system_message, prompt, model)
                except Exception as e:
                        print("Completion Exception in example: ", example)
                        time.sleep(60)
                        response = get_completion_zero_shot(new_system_message, prompt, model)
                finally:                
                        if response is not None :
                                re.sub("\n+", "\n", response)
                                answer, explanation = response.split("\n", 1)
                                correct = answer.__contains__(expected) 
                        else :
                                correct = False       
                df.loc[len(df.index)] = [prompt, expected, answer, explanation,  correct]

        result_path = f"results/{json_string.split('/')[1].split('.')[0]}_results.json"       
        df.to_json(result_path, index=True)     
        accuracy = df['correct'].mean()
        return round(accuracy, 2)
        
