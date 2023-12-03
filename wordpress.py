import requests
import json
from config import config

def publish(article):
    # Post data (title and content)
    post ={
        'title': article['title'],
        'content': article['content'],
        'status': 'publish',  # Set the post status (e.g., 'publish', 'draft')
        'featured_media': article['featured_media_id'],  # Set the featured image ID
        'tags':article['tag_ids'],
        'categories':[article['categories']]
    }
    print(post)

    # Send the HTTP request
    post_endpoint= config['wordpress']['url']+'wp-json/wp/v2/posts'
    response = requests.post(post_endpoint, auth=(config['wordpress']['username'], config['wordpress']['password']), json=post)

    # Check the response
    if response.status_code == 201:
        print('Post created successfully')
        article_id = response.json().get('id')
        return article_id

    else:
        with open("temp.txt", 'w') as file:
            json.dump(response.text, file, ensure_ascii=False, indent=4)

        print('Failed to create post: error is in temp.txt' )
        exit()

def publish_img(image_file_path):
    try:
        media_endpoint = config['wordpress']['url'] + 'wp-json/wp/v2/media'
        print(media_endpoint)
        files = {'file': ('image.jpg', open(image_file_path, 'rb'), 'image/jpeg')}
        media_response = requests.post(media_endpoint, auth=(config['wordpress']['username'], config['wordpress']['password']), files=files)

        if media_response.status_code == 201:
            attachment_id = media_response.json().get('id')
        else:
            print("Failed to upload the image. Status code:", media_response.status_code)
            attachment_id = None
    except Exception as ex:
            print(ex)

    return attachment_id

def get_or_create_tags(tag_names):
    try:
        if tag_names==None:
            print("No Tags")
            return
        print(tag_names)
        # Initialize an empty list to store tag IDs
        tag_ids = []

        for tag_name in tag_names:
            # Check if the tag already exists
            tag_exists = False
            tag_id = None

            # Query the WordPress API to find the tag by name
            tags_url = config['wordpress']['url'] + "wp-json/wp/v2/tags"
            params = {'search': tag_name}
            response = requests.get(tags_url, auth=(config['wordpress']['username'], config['wordpress']['password']), params=params)

            if response.status_code == 200:
                tags_data = response.json()
                for tag in tags_data:
                    if tag.get('name') == tag_name:
                        tag_exists = True
                        tag_id = tag.get('id')
                        break

            if not tag_exists:
                # If the tag doesn't exist, create it
                tag_data = {
                    'name': tag_name
                }
                create_tag_response = requests.post(tags_url, auth=(config['wordpress']['username'], config['wordpress']['password']), json=tag_data)

                if create_tag_response.status_code == 201:
                    tag_id = create_tag_response.json().get('id')
                else:
                    print(f"Failed to create tag '{tag_name}'. Status code:", create_tag_response.status_code)

            if tag_id:
                tag_ids.append(tag_id)
        return tag_ids
    except Exception as ex:
        print(ex)
        exit()

def create_or_get_feed_id(category):
    # Define the category data
    category_data = {
        'name': category,
        'description': 'Category for feed posts'
    }

    # Check if the "Feed" category already exists
    category_exists = False
    categories_endpoint = config['wordpress']['url'] + 'wp-json/wp/v2/categories'
    categories = requests.post(categories_endpoint, auth=(config['wordpress']['username'], config['wordpress']['password']))

    categories_response = requests.get(categories_endpoint)
    if categories_response.status_code == 200:
        categories = categories_response.json()
        for category in categories:
            if category['name'] == 'Feed':
                category_exists = True
                category_id = category['id']
                break

    # If the category doesn't exist, create it
    if not category_exists:
        category_response = requests.post(categories_endpoint, json=category_data, auth=(config['wordpress']['username'], config['wordpress']['password']))

        if category_response.status_code == 201:
            print('Category "Feed" created successfully!')
            category_id = category_response.json()['id']
        else:
            print(f'Failed to create the category. Status code: {category_response.status_code}')
            print(category_response.text)
    return category_id