"""
Starting with a given URL of a web page, downloads its html, writes html code into a directory structure.
Extracts text from html and stores text in an identical parallel directory structure.
Follows all links it finds, however not leaving the domain (TODO: not go up in path)
Will stop if no new links were found.

`$ python wgetText https://docs.centrifuge.io/learn/terms`
"""
# author : GPT-4, Sven Meyer

import os
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

# Directory to store HTML files
HTML_DIR = expand_path_with_tilde("~/DEV/AI/knowledge-db/html/")

# Directory to store text files
TEXT_DIR = expand_path_with_tilde("~/DEV/AI/knowledge-db/text/")

def expand_path_with_tilde(path):
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return path

# Set to store visited URLs
visited_urls = set()

def download_page(url):
    # Print the URL before sending the request
    print(f"Downloading: {url}", end=" ")
    
    # Check if the URL has already been visited
    if url in visited_urls:
        print(" (Skipped - Already Visited)")
        return
    
    # Send an HTTP GET request and download the page
    response = requests.get(url)
    
    # Store the response code in a variable and print it
    status_code = response.status_code
    print(f" : {status_code}")
    
    # Skip processing if there was a problem (non-2xx status code)
    if response.ok:
        visited_urls.add(url)  # Add the URL to visited set
        content = response.text
        
        # Extract links from the page
        soup = BeautifulSoup(content, "html.parser")
        links = soup.find_all("a")
        print("Links found :", links)
        
        # Filter and process each link
        for link in links:
            href = link.get("href")
            if href and (href.endswith(".html") or href.endswith(".htm") or href.endswith(".txt"):
                # Normalize and join the URL
                abs_url = urljoin(url, href)
                
                # Ensure the link is within the same domain
                parsed_abs_url = urlparse(abs_url)
                parsed_base_url = urlparse(BASE_URL)
                if parsed_abs_url.netloc == parsed_base_url.netloc:
                    # Create directory structure for storing HTML file
                    path = os.path.normpath(parsed_abs_url.path)
                    dir_path = os.path.join(HTML_DIR, path.lstrip("/"))
                    os.makedirs(dir_path, exist_ok=True)
                    
                    # Store HTML file
                    filename = os.path.join(dir_path, "index.html")
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(content)
                    
                    # Create directory structure for storing text file
                    text_dir_path = os.path.join(TEXT_DIR, path.lstrip("/"))
                    os.makedirs(text_dir_path, exist_ok=True)
                    
                    # Convert page text to a string
                    text = soup.get_text()
                    
                    # Store text file
                    text_filename = os.path.join(text_dir_path, "index.txt")
                    with open(text_filename, "w", encoding="utf-8") as file:
                        file.write(text)
                    
                    # Recursively crawl the link
                    download_page(abs_url)

# Check if a web page URL is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide a YouTube video URL as a command-line argument.")
    sys.exit(1)

# Retrieve the YouTube video URL from command-line argument
base_url = sys.argv[1]
# Start crawling from the base URL
download_page(base_url)

