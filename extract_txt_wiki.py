#!/usr/bin/python3

# Set of Python funcitons for text extraction and preprocessing; made for the aim of wikipedia articles extraction for mimic3 synthesis
# Author:
#  _          _       ____            _ _        
# | |   _   _| | __  / ___|___   __ _(_) |_ ___  
# | |  | | | | |/ / | |   / _ \ / _` | | __/ _ \ 
# | |__| |_| |   <  | |__| (_) | (_| | | || (_) |
# |_____\__,_|_|\_\  \____\___/ \__, |_|\__\___/ 
#                               |___/            

import re
from num2words import num2words
import sys
import requests
from bs4 import BeautifulSoup

# Verify args
# If there are less than 1 arg
if len(sys.argv) != 1:
    # Instructate the user
    print("Usage: extract_txt_wiki <URL>")
    # And exit with error
    sys.exit(1)
    
# https://stackoverflow.com/questions/16778435/python-check-if-website-exists
# Define a function for an URL existence veirification
def does_url_exist(url):
    # Get HTTP request
    response = requests.get(url)
    # If response is succesful
    if response.status_code == 200:
        return True
    else:
        return False

# Define a function for extracting text from a html file
def get_string_from_html(url):
    # Get the HTML document behind the URL
    html = requests.get(url)
    # Make soup out of it
    soup = BeautifulSoup(html.text, 'html.parser')
    # Extract only content text from soup
    text = soup.get_text()
    
    # Return the text
    return text

url = "https://en.wikipedia.org/wiki/Bitcoin#"
if does_url_exist(url):
    print(get_string_from_html(url))

# Prepare a dict with special chars to be replaced
special_chars = {
        '+': 'plus',
        '€': ' Euro',
        '£': ' Pound',
        '%': 'percent',
        '>': 'greater than',
        '$': 'dollar ',
        '=': 'equals',
        '&': 'and',
        '|': 'or',
        '/': ' in proportion to ',
        '~': 'tilde',
        '×': 'times',
        '−': 'minus',
        '°': 'degree',
        '√': 'Square root',
        '*': 'asterisk',
        '_': 'Underscore',
        '□': 'Square symbol',
        '…': 'Ellipsis',
    }

# Define a function for replacing special chars with their transcription in alpha chars
def replace_special_chars(text):
    # Iterrate over the dict
    for char, transcription in special_chars.items():
        # For each iterration replace char with its transcription
        text = text.replace(char, transcription)
    
    # Return the result text
    return text

# Define a function to lowercase words longer than 4 characters (likely not acronyms)
def lowercase_words(text):
    # Create a regular expression to find words with at least 4 capital letters
    reg_pattern = r'\b[A-Z]{4,}\b'

    # Define a sub-function to lowercase the matching pattern
    def make_lowercase(match):
        return match.group().lower()

    # Use the re.sub() method to replace matching words in the text
    text = re.sub(reg_pattern, make_lowercase, text)

    # Return the result text
    return text


# Define a function to replace numbers with their word equivalents
def replace_numbers_with_words(text):
    # Create a regular expression to find numbers in the text
    reg_pattern = r'\b\d+\b'

    # Define a sub-function to replace matching numbers with their word equivalents
    def replace_number(match):
        number = int(match.group())
        return num2words(number)

    # Use the re.sub() method to replace matching numbers in the text
    text = re.sub(reg_pattern, replace_number, text)

    # Return the result text
    return text


# Define a function to remove empty lines from the text
def remove_empty_lines(file_path):
    # Open the text file in read-write mode
    with open(file_path, 'rw') as file:
        lines = file.readlines()
        # Use a lambda function to filter out empty lines and convert the result back to a list
        lines = list(filter(lambda s: s != "\n", lines))
        file.writelines(lines)
    print(f"Empty lines were removed from the file at {file_path}.")

if __name__ == "__main__":
    url = sys.argv[0]
    if does_url_exist(url):
        text = get_string_from_html(url)
        print("HTML downloaded and converted to text.")
        text = replace_special_chars(text)
        print("Special characters replaced with their alpha characters transcription.")
        text = lowercase_words(text)
        print("Non-acronyms with capitals lowercased.")
        text = replace_numbers_with_words(text)
        print("Numbers replaced with words.")
        print(text)
    else:
        print("Specified link can not be reached!")