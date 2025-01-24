import argparse
import os
import json
from .news_feed import parse_rss_feed_and_extract_content
from .config import load_config
from .prompt import generate_image

def main():
    # Load configuration
    config = load_config()

    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Singularity Sentinel: AI News System")

    # RSS Feed Parser
    parser.add_argument(
        "--rss",
        type=str,
        required=False,
        help="RSS feed URL to parse articles from.",
        default="https://www.techcrunch.com/rss"
    )

    # Output File for Articles
    parser.add_argument(
        "--output",
        type=str,
        default="output.json",
        help="File to save the extracted articles (default: output.json)."
    )

    # Ad Generator
    parser.add_argument(
        "--generate-ad",
        type=str,
        required=False,
        help="Prompt for generating an advertisement image."
    )

    # Parse the arguments
    args = parser.parse_args()

    if args.generate_ad:
        # Generate Advertisement Image
        print(f"Generating advertisement based on prompt: {args.generate_ad}")
        ad_image_path = generate_image(args.generate_ad)
        print(f"Advertisement image saved at: {ad_image_path}")
    else:
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
