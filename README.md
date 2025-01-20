# AI-NewsFeed

AI-NewsFeed is an automated system designed to generate and publish blog posts from RSS feeds to WordPress. It uses AI-powered content generation, image creation, and customizable prompts for automation.

## Features

- Fetches articles from RSS feeds (Tech Crunch right now)
- Generates titles, content, using OpenAI
- Generated images with OpenAI or Replicateother Flux
- Publishes posts to WordPress with metadata (tags, categories, and featured images).
- Customizable prompts for content generation

## Directory Structure

```plaintext
AI-NewsFeed/
├── README.md
├── articles/
├── example.md
├── images/
├── prompts/
├── singularity_sentinel/
│   ├── __init__.py
│   ├── __main__.py
│   ├── a.py
│   ├── cli.py
│   ├── config.py
│   ├── core.py
│   ├── news_feed.py
│   ├── prompt.py
│   ├── wordpress.py
```

## Configuration

### Prerequisites

1. Create the following folders in the root directory:
   - `articles`
   - `images`
   - `prompts`
2. Set up API keys for OpenAI and Replicate.
3. Configure a WordPress user with an Application Password.

### `config.json` Example

```json
{
  "wordpress": {
    "url": "https://xxx.yyy/",
    "username": "xxx",
    "password": "xxx"
  },
  "openai": {
    "orginization_id": "org-xxx",
    "project_id": "proj_xxx",
    "api_key": "sk-svcacct-xxxxx",
    "llm-model": "gpt-4o-mini-2024-07-18",
    "image-model": "dalle"
  },
  "replicate": {
    "api_key": "r8_xxx"
  },
  "rss_feed_url": "https://news.ycombinator.com/rss.xml",
  "folders": {
    "prompts": "prompts",
    "images": "images",
    "articles": "articles"
  },
  "size": "512x512",
  "img_src": "flux"
}
```

### Prompts Customization

- Edit prompts in the `prompts/` folder for fine-tuned content.
- Available prompts:
  - `validator.txt`: Flags articles for regeneration.
  - `title.txt`: Generates titles.
  - `content.txt`: Generates article content.
  - `dalle.txt`: Generates image prompts.

## Installation

1. Install dependencies:
   ```bash
   pipenv install
  ```


2. Activate a Python virtual environment:
   ```bash
   pipenv shell
   ```

## Usage

Run the application with the following command:

```bash
python -m singularity_sentinel
or 
make run
```

## Example Output

See [example.md](example.md) for a sample generated post.

## License

This project is licensed under the BSD 3 License. See `LICENSE` for details.
