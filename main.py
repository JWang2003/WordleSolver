import random
from jsonArrayFileManip import *
from words_scraper import *
from words_occurrence_scraper import *

# Wordle Solver
# Note: Success is not guaranteed. Can run out of attempts.
    
def get_words_zero_occ():
    write_json_into_another('words_zero_occ.json', 'words.json')
    

def is_answer_found(current_answer):
    for letter in current_answer:
        if letter == "=":
            return False
    return True


def check_format_match(given_list, template_list):    
    # Checks both lists are same length
    if len(template_list) != len(given_list):
        return False
    
    # Checks that all elements in given_list are a single letter string
    for elt in given_list:
        if len(elt) != 1:
            return False
    return True


# Function that checks if letter matches between for each of the two list's element if they are not '='
def check_matching_letter_pos(given_list, template_list):
    for ind in range(len(template_list)):
        if template_list[ind] == "=" or given_list[ind] == "=":
            continue
        if template_list[ind] != given_list[ind]:
            return False
    return True


# Filter word_list by next_guess_as_list and current_answer
# This is used to deal with any letters known to be valid but are in the wrong position in next_guess_as_list.
# EFFECTS: - Will filter out any word that does not agree in value with current_answer
#          - WIll filter out any word that has any same letter with the same index as next_guess_as_list, while
#            current_answer still remains to be "=" at the same index.
def filter_by_ng_ca(word_list, next_guess_as_list, current_answer): 
    filtered_list = []
    for word in word_list:
        curr_word_as_list = " ".join(word).split(" ")
        
        if not check_matching_letter_pos(curr_word_as_list, current_answer):
            continue
  
        for ind in range(len(curr_word_as_list)):
            # current_answer[ind] == "=" means that next_guess[ind] letter is incorrect for that ind
            if current_answer[ind] == "=" and curr_word_as_list[ind] == next_guess_as_list[ind]:
                break
            
            # if we get to the last letter and the word is still valid according to previous conditional,
            # append to filtered_list
            if ind ==  len(curr_word_as_list) - 1:
                filtered_list.append(word)
        
    return filtered_list


def lstA_contains_lstB_elts(lstA, lstB):
    for elt in lstB:
        if elt not in lstA:
            return False
    return True

    
def remove_words_with_letters(letter_list, word_list):
    filtered_list = []
    for word in word_list:
        curr_word_as_list = " ".join(word).split(" ")
        # if curr_word_as_list and letter_list do not share any common elements/letters
        if not (bool(set(curr_word_as_list) & set(letter_list))):
            filtered_list.append(word)
    return filtered_list


def keep_words_with_all_letters(letter_list, word_list):
    filtered_list = []
    for word in word_list:
        curr_word_as_list = " ".join(word).split(" ")
        # if curr_word_as_list contains ALL letters from letter_list
        if (set(letter_list).issubset(curr_word_as_list)):
            filtered_list.append(word)
    return filtered_list


def arrange_optimal_guess(json_file_name, optimal_guess_list):
    for guess in optimal_guess_list:
        place_into_front(json_file_name, "name", guess)
    


    

print("Setting up JSON file...")
# Refreshing occurrences in words.json
# get_words_zero_occ()
# get_occurrences()


sort_json_ascending('words.json', 'name')
sort_json_ascending('words.json', "occurrences")
optimal_guess_list = ['REACT']
arrange_optimal_guess('words.json', optimal_guess_list)

print("Finished. Thank you for waiting!")
print("---------------------------------------------------------------------")


# Setting up word lists to be used in the program
word_dict_list = get_json_array_data('words.json')
word_list = [d["name"] for d in word_dict_list]
# print(word_list)
word_list_no_dupe = []
word_list_with_dupe = []

for word in word_list:
    if len(set(word)) == len(word):
       word_list_no_dupe.append(word)
    else:
       word_list_with_dupe.append(word)

     


attempts_left = 6
num_of_guesses = 0 
keepRunning = True
invalidLetters = []
validLetters = []
currentAnswer = ["=", "=", "=", "=", "="]

print("Welcome to wordle solver application!")

while attempts_left > 0:
    if word_list_no_dupe:
        nextGuess = " ".join(word_list_no_dupe[0])
        word_list_no_dupe.pop(0)
    else:
        nextGuess = " ".join(word_list_with_dupe[0])
        word_list_with_dupe.pop(0)

    next_guess_as_list = nextGuess.split(" ")
    print(f"Next generated guess:    {nextGuess}")
    print(f"Current answer progress: {' '.join(currentAnswer)}")

    # Asks user for the results of their answer guess

    while True:
        format_string = input("""Please indicate which letters were placed in the correct position [separated by space]
                       : """).strip().upper()
        format_list = format_string.split(" ")
        if   not check_format_match(format_list, currentAnswer):
            print("Incorrect formatting. Please make sure there is a space between each letter or equal sign. (ex. = O = R N)")
        elif not check_matching_letter_pos(next_guess_as_list, format_list):
            print("One or more letters that were inputted are not contained in current generated guess")
        elif not check_matching_letter_pos(format_list, currentAnswer):
            print("One or more letters that were inputted do not agree with the current answer progress")
        else:
            currentAnswer = format_list
            attempts_left  -= 1
            num_of_guesses += 1
            
            if is_answer_found(currentAnswer):
                print(f"Correct answer has been found!: {' '.join(currentAnswer)}")
                print(f"Number of guesses: {num_of_guesses}")
                keepRunning = False
                break

            if attempts_left == 0:
                print("Sorry! All attempts have been used.")
            
            # Filter out words according to  next_guess_as_list and current_answer
            temp_no_dupe = filter_by_ng_ca(word_list_no_dupe, next_guess_as_list, currentAnswer)
            temp_with_dupe = filter_by_ng_ca(word_list_with_dupe, next_guess_as_list, currentAnswer)

            if not (temp_no_dupe or temp_with_dupe):
                print("Given input is incorrect as there are no more possible words left after filtration")
                continue
        
            word_list_no_dupe = temp_no_dupe
            word_list_with_dupe = temp_with_dupe
            break

    if not keepRunning:
        break

    
    while True:
        input_string = input(f""""Which letter(s) are not in the word at all? [separate by space; leave blank if none]; 
        Currently Known: {invalidLetters}\n""").strip().upper()
        # handling empty input
        if input_string == "":
            break

        new_invalids = input_string.split(" ")
        
        # new_invalids and currentAnswer share any same elements/letters
        if bool(set(new_invalids) & set(currentAnswer)):
            print("Cannot give letters that are set in current answer progress")
        # new_invalids and validLetters share any same elements/letters
        elif bool(set(new_invalids) & set(validLetters)):
            print(f"Cannot give letters already known to be valid: {validLetters}")
        # next_guess_as_list does not contain any letter(s) from new_invalids
        elif not lstA_contains_lstB_elts(next_guess_as_list, new_invalids):
            print("Cannot give letters that are not in current generated guess")
        else:
            # Filter out words according to invalid words
            temp_no_dupe   = remove_words_with_letters(new_invalids, word_list_no_dupe)
            temp_with_dupe = remove_words_with_letters(new_invalids, word_list_with_dupe)

            if not (temp_no_dupe or temp_with_dupe):
                print("Given input is incorrect as there are no more possible words left after filtration")
                continue

            word_list_no_dupe = temp_no_dupe
            word_list_with_dupe = temp_with_dupe


            # Add all letters that were not already known to be invalid into invalidList
            if not lstA_contains_lstB_elts(invalidLetters, new_invalids):
                invalidLetters.extend(new_invalids)
            break


    while True:
        input_string = input(f"""Which letter(s) are in the word but not in the correct position? [separate by space; leave blank if none];
        Currently Known: {validLetters}\n""").strip().upper()
        # handling empty imput
        if input_string == "":
            break

        new_valids = input_string.split(" ")

        # new_valids and currentAnswer share any same elements/Aletters
        if bool(set(new_valids) & set(currentAnswer)):
            print("Cannot give letters that are set in current answer progress")
        # new_valids and invalidLetters share any same elements/letters
        elif bool(set(new_valids) & set(invalidLetters)):
            print(f"Cannot give letters already known to be invalid: {invalidLetters}")
        # next_guess_as_list does not contain any letter(s) from new_valids
        elif not lstA_contains_lstB_elts(next_guess_as_list, new_valids):
            print("Cannot give letters that are not in current generated guess")
        else:
            # Filter out words according to valid words
            temp_no_dupe   = keep_words_with_all_letters(new_valids, word_list_no_dupe)
            temp_with_dupe = keep_words_with_all_letters(new_valids, word_list_with_dupe)

            if not (temp_no_dupe or temp_with_dupe):
                print("Given input is incorrect as there are no more possible words left after filtration")
                continue
            
            word_list_no_dupe = temp_no_dupe
            word_list_with_dupe = temp_with_dupe


            # Add all letters that were not already known to be valid into validList
            if not lstA_contains_lstB_elts(validLetters, new_valids):
                validLetters.extend(new_valids)
            break


    print(f"Attempts left: {attempts_left}")
    
    print("-------------------------------------------------------------------------------------")
   
    

# from_list = ["A", "B", "O", "R", "T"]
# to_list =   ["A", "=", "=", "=", "="]
# insert_valid_letters(from_list, to_list)
# print(to_list)










# # Requires: check_format_match(from_list, to_list) and checking_mathing_letter_pos(from_list, to_list) returns True
# def insert_valid_letters(from_list, to_list):
#     for ind in range(len(from_list)):
#         if from_list[ind] == "=":
#             continue
#         else:
#             to_list[ind] = from_list[ind]


# def filter_by_current_answer(given_list):
#     filtered_list = []
#     for word in given_list:
#         curr_word_as_list = " ".join(word).split(" ")
#         if check_matching_letter_pos(curr_word_as_list, currentAnswer):
#             filtered_list.append(word)
#     return filtered_list