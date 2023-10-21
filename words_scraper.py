from bs4 import BeautifulSoup
import requests
from jsonArrayFileManip import *

# Web scraper that takes all possible wordle words from different websites and adds them to words.json

def setup_words(): 
    setup_words1()    
    # setup_words2()  # A lot higher rate of failure
    

# Function that gets word data from wordunscrambler.net
def setup_words1():
    clear_json('words.json')
    html_text = requests.get('https://www.wordunscrambler.net/word-list/wordle-word-list').text
    soup = BeautifulSoup(html_text, 'lxml')

    wordle_data = soup.find_all('li', class_ = 'invert light')
    for word in wordle_data:
        word_name = word.a.text
        add_to_json('words.json', {"name" : word_name.upper(), 
                                   "occurrences" : 0},
                                   "name")

# Function that gets word data from https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93
# CAUTION: TAKES EXTREMELY LONG TIME TO RUN.
def setup_words2():
    html_text = requests.get('https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93').text
    soup = BeautifulSoup(html_text, 'lxml')

    table   = soup.find(lambda tag: tag.name=='table')
    td_rows = table.find_all("td", class_='blob-code')

    for word in td_rows:
        word_name = word.text
        add_to_json('words.json', {"name" : word_name.upper(), 
                                   "occurrences" : 0},
                                   "name")