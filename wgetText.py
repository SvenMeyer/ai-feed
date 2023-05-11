"""
Starting with a given URL of a web page, downloads its HTML, writes HTML code into a directory structure.
Extracts text from HTML and stores text in an identical parallel directory structure.
Follows all links it finds, however not leaving the domain 
Will not go up in path unless --allow_up option is provided
Will stop if no new links were found.

`$ python wgetText https://docs.centrifuge.io/learn/terms`
"""
# author : GPT-4, Sven Meyer

import os
import sys
import argparse
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def expand_path_with_tilde(path):
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return path

# Directory to store HTML files
HTML_DIR = expand_path_with_tilde("~/DEV/AI/knowledge-db/html/")

# Directory to store text files
TEXT_DIR = expand_path_with_tilde("~/DEV/AI/knowledge-db/text/")

# Set to store visited URLs
visited_urls = set()

def download_page(url, allow_up=False):
    # Print the URL before sending the request
    print(f"Downloading: {url}", end=" ")

    # Check if the URL has already been visited
    if url in visited_urls:
        print(" (Skipped - Already Visited)")
        return

    # Send an HTTP GET request and download the page
    response = requests.get(url)

     # Add the URL to visited set - TODO: retry if temprary failure
    visited_urls.add(url)

    # Store the response code in a variable and print it
    status_code = response.status_code
    print(f" : {status_code}")

    # Skip processing if there was a problem (non-2xx status code)
    if not response.ok:
        return

    content = response.text

    # Process content
    # Create directory structure for storing HTML file
    # split url into components
    parsed_abs_url = urlparse(url)
    full_path = os.path.normpath(parsed_abs_url.path)
    path, filename_with_extension = os.path.split(full_path)
    filename, extension = os.path.splitext(filename_with_extension)

    print("full_path :", full_path)
    print("filename_with_extension :", filename_with_extension)
    print("filename :", filename)
    print("extension :", extension)

    if not filename_with_extension.strip():
        filename_with_extension = "index.html"
    else:
        if not extension.strip():
            filename_with_extension = filename + ".html"
        

    dir_path = os.path.join(HTML_DIR, path.lstrip("/"))
    os.makedirs(dir_path, exist_ok=True)

    # Write HTML file
    html_file = os.path.join(dir_path, filename_with_extension)
    print("writing html_file :", html_file)
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(content)


    # Create directory structure for storing text file
    text_dir_path = os.path.join(TEXT_DIR, path.lstrip("/"))
    os.makedirs(text_dir_path, exist_ok=True)

    # Convert page text to a string
    soup = BeautifulSoup(content, "html.parser")

    # extract text
    text = soup.get_text('\n', strip=True)

    # create filename
    if not filename_with_extension.strip():
        filename_with_extension = "index.txt"
    else:
        if not filename.strip():
            filename_with_extension = "index.txt"
        else:
            filename_with_extension = filename + ".txt"

    # Write text file
    text_file = os.path.join(text_dir_path, filename_with_extension)
    print("writing text_file :", text_file)
    with open(text_file, "w", encoding="utf-8") as file:
        file.write(text)


    # Process Links
    # Extract links from the page
    links = soup.find_all("a")
    # print("Links found :", links)

    # Filter and process each link
    for link in links:
        href = link.get("href")
        if href and (href.endswith((".html", ".htm", ".txt"))):
            # Normalize and join the URL
            abs_url = urljoin(url, href)

            # Ensure the link is within the same domain and does not go up in the path
            parsed_abs_url = urlparse(abs_url)
            parsed_base_url = urlparse(base_url)
            if (
                parsed_abs_url.netloc == parsed_base_url.netloc
                and (parsed_abs_url.path.startswith(parsed_base_url.path or allow_up))
            ):
                # Recursively crawl the link
                download_page(abs_url)


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Web crawling and downloading HTML content")
parser.add_argument("url", help="URL of the web page to crawl")
parser.add_argument("--allow_up", action="store_true", help="Allow crawling to go up in the path")
args = parser.parse_args()

# Retrieve the YouTube video URL and allow_up flag from command-line arguments
base_url = args.url
allow_up = args.allow_up

# Start crawling from the base URL
download_page(base_url, allow_up)

