import random
import json
import os

N_EXAMPLES = 60
MAX_SHOTS = 5

def extract_datasets():  
       for filename in os.listdir('full_data'):
              with open(f"full_data/{filename}", 'r') as file:
                     data = json.load(file)
                     examples = data.get("examples", [])
              random.shuffle(examples) # shuffle examples so the difficult ones are not always at the end
              if filename.__contains__("color"):
                     examples = random.sample(examples, (N_EXAMPLES//4)+MAX_SHOTS)
              elif len(examples) > N_EXAMPLES+MAX_SHOTS:
                     examples = random.sample(examples, N_EXAMPLES+MAX_SHOTS) 
              shots = examples[:MAX_SHOTS]
              examples = examples[MAX_SHOTS:]
              data = {"examples": examples, "shots": shots}
              with open(f'datasets/{filename}', 'w') as file:
                     json.dump(data, file)
