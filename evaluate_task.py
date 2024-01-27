import os
import json
import random
import time
import pandas as pd
from get_completion import get_completion_zero_shot


N_EXAMPLES = 5


def shrink_examples(data):
    #shrinks the examples to n examples randomly selected with no repetitions
        examples = data.get("examples", [])
        if len(examples) > N_EXAMPLES:
            examples = random.sample(examples, N_EXAMPLES) 
        return examples

                  

def evaluate_multiple_choice_task(json_string, system_message, model):    
    
        df = pd.DataFrame(columns=['prompt','expected', 'answer', 'correct'])


        with open(json_string, 'r') as file:
                data = json.load(file)

        examples_selected = shrink_examples(data)

        for example in examples_selected:
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
                                #check on the first word of the answer if it contains the expected answer
                                correct = answer.split()[0].__contains__(expected) 
                        else :
                                correct = False       
                df.loc[len(df.index)] = [prompt, expected, answer, correct]
        df.to_csv("results/anachronisms_gpt3_5.csv", index=True)
        
        accuracy = df['correct'].mean()
        return accuracy * 100
        
