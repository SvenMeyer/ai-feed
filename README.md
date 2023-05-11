# ai-feed

## collection of script to feed AI with knowledge

### getYoutubeTranscript.py

Get english transcript for a given youtube video and store it in a text file.

`$ python getYoutubeTranscript.py https://www.youtube.com/watch?v=SW14tOda_kI`

### cat wgetText.py

Starting with a given URL of a web page, downloads its html, writes html code into a directory structure.
Extracts text from html and stores text in an identical parallel directory structure.
Follows all links it finds, however not leaving the domain (TODO: not go up in path)
Will stop if no new links were found.

`$ python wgetText https://docs.centrifuge.io/learn/terms`


