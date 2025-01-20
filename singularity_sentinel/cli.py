import argparse
import os
import json
from .news_feed import parse_rss_feed_and_extract_content
from .config import load_config


def main():
    # Load configuration
    config = load_config()

    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Singularity Sentinel: AI News System")

    parser.add_argument(
        "--rss",
        type=str,
        required=False,
        help="RSS feed URL to parse articles from.",
        default="https://www.techcrunch.com/rss"
    )

    parser.add_argument(
        "--output",
        type=str,
        default="output.json",
        help="File to save the extracted articles (default: output.json)."
    )

    args = parser.parse_args()

    # Fetch and process articles
    print(f"Fetching articles from: {args.rss}")
    articles = parse_rss_feed_and_extract_content(args.rss)

    if articles:
        # Save articles to the specified file
        output_path = args.output
        with open(output_path, "w") as outfile:
            json.dump(articles, outfile, indent=4, ensure_ascii=False)

        print(f"Successfully retrieved and saved {len(articles)} articles to {output_path}.")
    else:
        print("No articles were retrieved from the RSS feed.")


if __name__ == "__main__":
    main()
