import random
import json

N_EXAMPLES = 50
MAX_SHOTS = 4

def shrink_examples(json_string, (N_EXAMPLES,MAX_SHOTS) as n ): #persistenti
        examples = json_string.get("examples", [])
        random.shuffle(examples) # shuffle examples so the difficult ones are not always at the end
        if len(examples) > n:
            examples = random.sample(examples, n) 
        return examples


        if(json_string.__contains__("color")):
               examples_selected = shrink_examples(data, N_EXAMPLES//4)
        else:
               examples_selected = shrink_examples(data, N_EXAMPLES)

        with open(json_string, 'r') as file:
                data = json.load(file)
