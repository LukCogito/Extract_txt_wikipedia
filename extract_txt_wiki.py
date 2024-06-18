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
import pathlib

# https://stackoverflow.com/questions/22947427/getting-home-directory-with-pathlib
home_dir = pathlib.Path.home()

# Verify args
# If there are less than 2 args
if len(sys.argv) != 3:
    # Instructate the user
    print("Usage: extract_txt_wiki <URL> <lang>")
    # And exit with error
    exit(1)

# Verify the lang
if sys.argv[2] in ["cz", "en"]:
    
    if sys.argv[2] == "cz":
        special_chars_trans = {
            '+': 'plus',
            '€': ' euro',
            '£': ' libra',
            '%': ' procento',
            '>': ' větší než',
            '$': ' dolar',
            '=': ' rovná se',
            '&': ' a',
            '|': ' paralelně s',
            '/': ' v poměru k',
            '~': ' vlnovka',
            '×': ' krát',
            '−': ' minus',
            '°': ' stupeň',
            '√': ' druhá odmocnina',
            '*': ' hvězdička',
            '_': ' podtržítko',
            '□': ' čtverec',
            '...': ' trojtečka',
            }

    else:
        special_chars_trans = {
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

else:
    print("Language must be \"en\" or \"cz\"")
    exit(1)

    
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

# Define a function for replacing special chars with their transcription in alpha chars
def replace_special_chars(text):
    # Iterrate over the dict
    for char, transcription in special_chars_trans.items():
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
    reg_pattern = re.compile(r'\b\d+\b')

    # Define a sub-function to replace matching numbers with their word equivalents
    def replace_number(match):
        number = int(match.group())
        return num2words(number, lang=sys.argv[2])

    # Use the re.sub() method to replace matching numbers in the text
    text = re.sub(reg_pattern, replace_number, text)

    # Return the result text
    return text


# Define a function to remove empty lines from the text
def remove_empty_lines(text):
    # Split text to list with each line as an item
    text_splitted = text.splitlines()
    # Prepare a list for text concat
    text_concat = []
    # Iterrate over the splitted text

    for line in text_splitted:
        # If line isn't empty
        if line != "":
            # Append it to the list
            text_concat.append(line)
    # And finally join the list without empty lines
    text = "\n".join(text_concat)

    return text

def remove_square_brackets(text):
    reg_pattern = re.compile(r"\[(.*?)\]")
    text = re.sub(reg_pattern, "", text)

    return text

if __name__ == "__main__":
    url = sys.argv[1]
    if does_url_exist(url):
        text = get_string_from_html(url)
        print("HTML downloaded and converted to text.")
        text = replace_special_chars(text)
        print("Special characters replaced with their alpha characters transcription.")
        text = lowercase_words(text)
        print("Non-acronyms with capitals lowercased.")
        text = replace_numbers_with_words(text)
        print("Numbers replaced with words.")
        text = remove_empty_lines(text)
        print("Empty lines removed.")
        text = remove_square_brackets(text)
        print("Square breckets and its content removed.")
        url_splitted = url.split("/")
        article_name = url_splitted[len(url_splitted)-1].lower()
        output_path = f"{home_dir}/{article_name}.txt"
        with open(output_path, "w", encoding="UTF8") as output:
            output.write(text)
            print(f"Article about {article_name} saved to \"{output_path}\"")
    else:
        print("Specified link can not be reached!")