import random
import json
import os

N_EXAMPLES = 50
MAX_SHOTS = 4

def extract_datasets(): #persistenti 
       for filename in os.listdir('data'):
              with open(filename, 'r') as file:
                     data = json.load(file)
                     examples = data.get("examples", [])
              random.shuffle(examples) # shuffle examples so the difficult ones are not always at the end

              if len(examples) > N_EXAMPLES+MAX_SHOTS:
                     examples = random.sample(examples, N_EXAMPLES+MAX_SHOTS) 

              shots = examples[:MAX_SHOTS]
              examples = examples[MAX_SHOTS:]
#devo fare la scrittura su file
              with open(f'datasets/{filename}', 'w') as file:
                     json.dump(data, file)
              
        if(json_string.__contains__("color")):
               examples_selected = shrink_examples(data, N_EXAMPLES//4)
        else:
               examples_selected = shrink_examples(data, N_EXAMPLES)

        with open(json_string, 'r') as file:
                data = json.load(file)
