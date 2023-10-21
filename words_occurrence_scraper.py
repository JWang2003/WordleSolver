from bs4 import BeautifulSoup
import requests
from jsonArrayFileManip import *

# Web scraper that gets all past occurrences of words in wordle answers and updates word.json

def add_occurrence(json_file_name, answer_name):
    with open(json_file_name) as f: 
        listData = json.load(f)

    filtered_dicts = list(filter(lambda word: word['name'] == answer_name, listData))
    # We know that the size of filtered_dicts must be 1 if the word exists in words.json
    try:
        matching_dict = filtered_dicts[0]
    # If answer does not exist in words.json, we make a new item for that answer and set occurrences to 1
    except IndexError:
        print(f"{answer_name} missing in {json_file_name}")
        add_to_json('words.json', {"name" : answer_name,
                                   "occurrences" : 1}, 
                                   "name")
        return

    matching_dict['occurrences'] += 1
    write_into(json_file_name, listData)

    print(f"Added occurrence to {matching_dict['name']}; {matching_dict['occurrences']}")



def get_occurrences():
    html_text = requests.get('https://wordfinder.yourdictionary.com/wordle/answers/').text
    soup = BeautifulSoup(html_text, 'lxml')

    # Past Answers
    past_answer_data = soup.find_all('strong')
    for past_answer in past_answer_data:
        past_answer_name = past_answer.text
        add_occurrence('words.json', past_answer_name)

    sort_json_ascending('words.json', "occurrences")



def get_answer():
    html_text = requests.get('https://wordfinder.yourdictionary.com/wordle/answers/').text
    soup = BeautifulSoup(html_text, 'lxml')

    # Today's Answer
    todays_answer = soup.find('span', class_="answer").text.strip()
    add_occurrence('words.json', todays_answer)
    return todays_answer