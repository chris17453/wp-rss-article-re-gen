import os
import requests
from datetime import datetime
from core import clean_title
import openai
from config import client, config

def get_prompts():
    # Specify the directory where the .txt files are located
    directory_path = './prompts'

    # Initialize an empty dictionary to store the prompts
    prompts = {}
    print("Getting prompts")
    # Loop through all files in the directory
    for filename in os.listdir(directory_path):
        # Check if the file has a .txt extension
        if filename.endswith('.txt'):
        
            # Extract the file name without the .txt extension
            prompt_name = os.path.splitext(filename)[0]
            
            # Construct the full path to the file
            file_path = os.path.join(directory_path, filename)
            
            # Read the content of the file and store it in the dictionary
            with open(file_path, 'r') as file:
                prompts[prompt_name] = file.read()

    # Print the prompts dictionary
    return prompts

prompts=get_prompts()

def generate_content(description, link):
    response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": prompts['system_content']},
        {"role": "user", "content": prompts['user_content'].format(description=description, link=link)}
    ])
    text=response.choices[0].message.content.strip()
    text=text.replace("h3>","h2>")
    return text

def validate_content(description):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompts['system_validation']},
        {"role": "user", "content": prompts['user_validation'].format(description=description)}
    ])
     
    if "PASS" in response.choices[0].message.content:
        return True
    return None

def generate_title(content):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompts['system_title']},
        {"role": "user", "content": prompts['user_title'] + content}
    ])
    return response.choices[0].message.content.strip()



# Define a function to generate blog content with GPT-3.5
def generate_blog_content(title, context):
    # Use the OpenAI API to generate content based on title and context
    response = client.completions.create(engine="text-davinci-002",
    prompt=f"Write a blog post about '{title}' with the following context:\n{context}",
    max_tokens=300,  # Adjust as needed
    n=1,  # Number of completions
    stop=None)
    return response.choices[0].text





def generate_art_prompt(title):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": prompts['dalle_system']},
        {"role": "user", "content": prompts['dalle_user'].format(title=title)}
    ])
    return response.choices[0].message.content.strip()


def generate_image(title):
    prompt=generate_art_prompt(title)
    cleaned_title = clean_title(title)
    img = create_dalle_image(prompt, cleaned_title)
    return img


def create_dalle_image(image_desc, title):
    print("-2--")
    print('\nImage Prompt:',image_desc,'\nTitle:',title)
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_desc,
        size="1024x1024",
        quality="standard",
        n=1,
        )

    image_url = response.data[0].url

    image_data = requests.get(image_url).content

    # Clean and sanitize the title
    cleaned_title = clean_title(title)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    image_filename = f"{current_datetime}-{cleaned_title}.png"

    image_path = os.path.join(config['folders']['images'], image_filename)
    with open(image_path, "wb") as f:
        f.write(image_data)
    return image_path

