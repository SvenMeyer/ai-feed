# https://www.geeksforgeeks.org/python-downloading-captions-from-youtube/
# pip3 install youtube-transcript-api

import os
import sys
from youtube_transcript_api import YouTubeTranscriptApi

# Directory to store text files
TEXT_DIR = "/home/sum/DEV/AI/knowledge-db/youtube/"

def video_id_from_url(video_url):
    # Extract the video ID from the URL
    video_id = video_url.split("=")[-1]
    return video_id


def download_transcript(video_id):
    # assigning srt variable with the list
    # of dictionaries obtained by the get_transcript() function
    srt = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return srt
    
  
# Check if a YouTube video URL is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide a YouTube video URL as a command-line argument.")
    sys.exit(1)

# Retrieve the YouTube video URL from command-line argument
video_url = sys.argv[1]
print("video_url =", video_url)

video_id = video_id_from_url(video_url)
print("video_id  =", video_id)

# Call the function to download the transcript
text_json = download_transcript(video_id)

# Create the directory structure if it doesn't exist
os.makedirs(TEXT_DIR, exist_ok=True)

# creating or overwriting a file "subtitles.txt" with
# the info inside the context manager

# Open the file for writing
file_path = os.path.join(TEXT_DIR, video_id + ".txt")

with open(file_path, "w") as file:
    # iterating through each element of list srt
    for j in text_json:
        print(j['text'])
        file.write(j['text'])


