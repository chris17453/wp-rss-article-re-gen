import json
from openai import OpenAI



def load_config():
  with open('config.json') as f:
    return json.load(f)
  
# load your config file
config = load_config()

# Configure your OpenAI API key
client = OpenAI(api_key=config['openai']['api_key'],organization=config['openai']['orginization_id'])

