import json 


query = input("Enter cateogory of whch you want prompt ")
path = './data.json'

prompts = []

try:
    with open(path,'r') as f:
        prompts = json.load(f)
except Exception as e :
    prompts = []


output_prompt = "prompt not exists"

for p  in prompts :
    if p['category'].lower() == query.lower():
        output_prompt = p['prompt']
        break


print(output_prompt)
