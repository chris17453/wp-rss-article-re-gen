import os
import re
import hashlib
from bs4 import BeautifulSoup
import unicodedata
import string
import json
from config import config


def strip_html_tags(html_string):
    # Parse the HTML string
    soup = BeautifulSoup(html_string, "html.parser")

    # Get the text content without HTML tags
    text = soup.get_text()

    return text

def get_env(env_variable_name):
    # Check if the environment variable exists
    if env_variable_name in os.environ:
        env_variable_value = os.environ[env_variable_name]
        #print(f'The value of {env_variable_name} is: {env_variable_value}')
    else:
        print(f'The environment variable {env_variable_name} is not set.')
        exit()
    return env_variable_value


def clean_title(title):
    cleaned_title = title.strip()
    cleaned_title = ''.join(ch for ch in cleaned_title if ch in string.printable)
    cleaned_title = unicodedata.normalize('NFKD', cleaned_title).encode('ascii', 'ignore').decode('utf-8')
    cleaned_title = re.sub(r'[^\w\s-]', '', cleaned_title).strip()
    cleaned_title = re.sub(r'[-\s]+', '-', cleaned_title)

    return cleaned_title

def article_hash(title):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with your string (encoded as bytes)
    md5_hash.update(title.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    md5_hash_hex = md5_hash.hexdigest()

    file=md5_hash_hex+".json"
    file_path=os.path.join(config['folders']['articles'],file)
    return file_path

def load_article(article):
    file_path=article_hash(article['entry']['title'])
    try:
        with open(file_path, 'r') as file:
            # Load the JSON data from the file
            data = json.load(file)     
            return data
    except:
        return article

def save_article(article):
    # Create a safe filename by removing characters that may cause issues
    file_path=article_hash(article['entry']['title'])

    # Serialize and save the article object to the file
    with open(file_path, 'w') as file:
            json.dump(article, file, ensure_ascii=False, indent=4)

    print(f'Article serialized and saved to: {file_path}')