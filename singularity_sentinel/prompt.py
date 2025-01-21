import os
import replicate
import requests
from datetime import datetime
from PIL import Image
import openai
from .core import clean_title
from .config import client, config

def compress_image(input_path, output_path, quality=85):
    """
    Compress an image and save it to a new file.
    :param input_path: Path to the input image file.
    :param output_path: Path to save the compressed image file.
    :param quality: Compression quality (1-100). Lower means more compression.
    """
    print(f"Compressing image: {input_path}")
    
    # Open the image
    with Image.open(input_path) as img:
        # Convert to RGB (to ensure compatibility with JPEG)
        img = img.convert("RGB")
        # Save with the desired quality
        img.save(output_path, "JPEG", quality=quality)
    
    print(f"Compressed image saved to: {output_path}")

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
    response = client.completions.create(engine=config['openai']['llm-model'],
    prompt=f"Write a blog post about '{title}' with the following context:\n{context}",
    max_tokens=300,  # Adjust as needed
    n=1,  # Number of completions
    stop=None)
    #text=response.choices[0].message.content.strip()
    #text=text.replace("h3>","h2>")
    return response.choices[0].text





def generate_art_prompt(title):
    if config['img_src']=="flux":
        system_prompt=prompts['flux_system']
        user_prompt=prompts['flux_user'].format(title=title)
    elif config['img_src']=="dalle":
        system_prompt=prompts['dalle_system']
        user_prompt=prompts['dalle_user'].format(title=title)
    else:
        print("No IMG Source configured")
        return

    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ])
    return response.choices[0].message.content.strip()


def generate_image(title):
    prompt=generate_art_prompt(title)
    cleaned_title = clean_title(title)
    if config['img_src']=="flux":
        img = create_flux_pro_image(prompt, cleaned_title)
    elif config['img_src']=="dalle":
        img = create_dalle_image(prompt, cleaned_title)
    else:
        print("No IMG Source configured")
        return
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


# Function to create an image using FLUX PRO
def create_flux_pro_image(image_desc, title):
    print("Creating image with FLUX PRO...")

    # Clean and sanitize the title
    cleaned_title = clean_title(title)
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    image_filename = f"{current_datetime}-{cleaned_title}.jpg"
  
    # FLUX PRO configuration
    replicate_client = replicate.Client(api_token=config['replicate']['api_key'])
    
    # Input data for FLUX PRO
    input_data = {
        "prompt": image_desc,
        "prompt_upsampling": True,
        "output_format":"png"
    }
    
    # Run FLUX PRO model
    output = replicate_client.run(
        "black-forest-labs/flux-1.1-pro",
        input=input_data
    )
    # Fetch the output image
    image_data = output.read()
    #print(image_data)
    
    # Define the path and save the image
    image_path = os.path.join(config['folders']['images'], image_filename)
    output_path=os.path.join(config['folders']['images'], f"zz_{image_filename}")
    with open(image_path, "wb") as f:
        f.write(image_data)
    compress_image(image_path, output_path, quality=85)
    print(f"FLUX PRO image saved at: {image_path}")
    return output_path