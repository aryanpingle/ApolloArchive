from typing import no_type_check
import requests

# Constants
HTML_URL = "https://www.toptal.com/developers/html-minifier/raw"
JS_URL = "https://www.toptal.com/developers/javascript-minifier/raw"
CSS_URL = "https://www.toptal.com/developers/cssminifier/raw"
HTML_FILE = "Datapoints"
JS_FILE = "JS/Datapoints"
CSS_FILE = "CSS/Datapoints"

# HTML Code
print("Creating data")
data = {"input": open(f"{HTML_FILE}.html", 'rb').read()}
print("Sending request")
response = requests.post(HTML_URL, data)
print("Saving file")
open(f"{HTML_FILE}-min.html", 'w', encoding='utf-8').write(response.text)

# JS Code
print("Creating data")
data = {"input": open(f"{JS_FILE}.js", 'rb').read()}
print("Sending request")
response = requests.post(JS_URL, data)
print("Saving file")
open(f"{JS_FILE}-min.js", 'w', encoding='utf-8').write(response.text)

# CSS Code
print("Creating data")
data = {"input": open(f"{CSS_FILE}.css", 'rb').read()}
print("Sending request")
response = requests.post(CSS_URL, data)
print("Saving file")
open(f"{CSS_FILE}-min.css", 'w', encoding='utf-8').write(response.text)