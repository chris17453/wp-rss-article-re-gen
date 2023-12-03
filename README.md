# Yet another wordpress post generator for RSS

## Config

- you need to create the articles,images folders
- you need to generate  config.json

```json
{
    "folders": {
      "prompts": "prompts",
      "images": "images",
      "articles": "articles"
    },
    "rss_feed_url": "https://website.rss",
    "wordpress": {
      "url": "WP-URL",
      "username": "USERNAME",
      "password": "APPLICATION PASSWORD"
    },
    "openai": {
      "openai_api_key": "sk-ABCDEF1234567890"
    },
    "size": "512x512"
  }

```

## Customization

- To fine tune the content, edit the prompts in the prompt folder.
- a system and user prmpt exist for each prompt
- the validator.txt prompt is what flags an article as being one we want to regenerate
- the title.txt creates the title
- the content.txt generates the article
- the dalle.txt generates the image

## Run

```bash
# enter your shell
pipenv shell
# install the dependencies
pipenv install -r requirements
# run the app
python news_feed.py
```

## Example

- [Example](example.md)
