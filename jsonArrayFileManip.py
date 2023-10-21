import json
# https://howtodoinjava.com/python-json/append-json-to-file/
# General module for Manipulating any JSON array file in directory 
# (JSON array where each element is a dictionary/item)


# Function that writes given item to JSON file associated with given file name, with option of rejecting to add
# if an existing item in the JSON file has the same value associated to given key as item to be added's
def add_to_json(json_file_name, added_item, key_check):
    """
    Input:  json_file_name - name of JSON file to be modified
            item           - item (in form of python dictionary) to be written/added to JSON file 
            key_check      - will not add item to JSON file if an item with value associated to key_check
                             is the same as given item's value associated with key_check. 
                             If the key_check is False then the function will skip this checking step completely.
    Output: adds item to given JSON file associared with json_file_name
    """

    # Access JSON file (JSON array) as python list
    with open(json_file_name) as f: 
        listData = json.load(f)


    # Checks if there is an item in JSON file whose value associated with key_check is the same as 
    # item to be added's value associated with key_check
    if key_check is not False: 
        if is_value_already_present(listData, key_check, added_item[key_check]):
            # print(f"Item with same {key_check} already present: {added_item[key_check]}")
            return

    # Goes into python list and adds given item 
    listData.append(added_item)

    # Verify updated list (DON'T UNCOMMENT WHEN ACTUALLY CALLING THIS FUNCTION FROM words_scraper.py)
    # print(listData)

    # Write to JSON file
    write_into(json_file_name, listData)
    
    # print(f"Successfully appended to the JSON file {added_item}")



def remove_from_json(json_file_name, remove_key, remove_value):

    # Access JSON file (JSON array) as python list
    with open(json_file_name) as f: 
        listData = json.load(f)

    if not is_value_already_present(listData, remove_key, remove_value):
        print("Item with given info not found")
        return
    
    for idx,name in enumerate(listData):
      if name[remove_key]==remove_value:
         deleted_item = listData[idx]
         del listData[idx]
         break
    
    # Write to JSON file
    write_into(json_file_name, listData)

    print(f"Successfully deleted from the JSON file {deleted_item}")
    


# Function that sorts JSON file associated with given JSON file name by given key in descending order
# REQUIRES: associated JSON array file actually contains sort_key
# MODIFIES: associated JSON array file 
def sort_json_descending(json_file_name, sort_key):
    """
    Input:  json_file_name - name of JSON file to be modified
            sort_key       - name of key to sort the file by
    Output: associated JSON file is sorted in descending order according to sort_key
    """

    # Access JSON file (JSON array) as python list
    with open(json_file_name) as f: 
        listData = json.load(f)
    
    # Sorts words in JSON file in descending order by sort_key
    listData.sort(key=lambda x: x[sort_key], reverse=True)
    
    # Verify updated list
    # print(listData)

    # Write to JSON file
    write_into(json_file_name, listData)
    


# Function that sorts JSON file associated with given JSON file name by given key in ascending order
# REQUIRES: associated JSON array file actually contains sort_key
# MODIFIES: associated JSON array file 
def sort_json_ascending(json_file_name, sort_key):
    """
    Input:  json_file_name - name of JSON file to be modified
            sort_key       - name of key to sort the file by
    Output: associated JSON file is sorted in ascending order according to sort_key
    """

    # Access JSON file (JSON array) as python list
    with open(json_file_name) as f: 
        listData = json.load(f)

    # Sorts words in JSON file in ascending by sort_key
    listData.sort(key=lambda x: x[sort_key])

    # Verify updated list
    # print(listData)

    # Write to JSON file
    write_into(json_file_name, listData)


# Function that sets JSON file associatd to given file name to empty array
def clear_json(json_file_name):
    """
    Input:  json_file_name - name of JSON file to be modified
    Output: associated JSON array file becomes empty array
    """
    empty_list = []
    write_into(json_file_name, empty_list)


def get_json_array_data(json_file_name):
    # Access JSON file (JSON array) as python list
    with open(json_file_name) as f: 
        listData = json.load(f)
    return listData



# TODO: add input output comments
# Helper function for determining if an existing item in the JSON file associated to key_check and given value share the same data
def is_value_already_present(json_list_data, key_check, given_value):
    # gets list of all items/dictionaries' values associated with key_check key in JSON file
    valueList = [d[key_check] for d in json_list_data]
    return given_value in valueList
       


# Helper function for writing data completely replacing existing infomation in JSON file associated with given JSON file name 
# with correct JSON format and indentation
def write_into(json_file_name, info_to_write):
    """
    Input:  json_file_name - name of JSON file to be modified
            info_to_write  - info to be written and completely replace everything in associated JSON file
    Output: all information in associated JSON file becomes info_to_write, with correct JSON indentations and format.
    """
    with open(json_file_name, 'w') as json_file:
        json.dump(info_to_write, json_file, 
                        indent=4,  
                        separators=(',',' : '))
        


# Function that replaces json_file_to's information with json_file_from's information
def write_json_into_another(json_file_from, json_file_to):
    """
    Input:  json_file_from - name of JSON file whose data will be copied
            json_file_to   - name of JSON file whose data will be overwritten by json_file_from's data
    """
    with open(json_file_from) as f: 
        overwrite_data = json.load(f)
    
    write_into(json_file_to, overwrite_data)


# Places item with key key_check and value given_value to the front of JSON array
def place_into_front(json_file_name, key_check, given_value):
    # Access JSON file (JSON array) as python list
    with open(json_file_name) as f: 
        listData = json.load(f)
    
    if not is_value_already_present(listData, key_check, given_value):
        # print("Item with given info not found")
        return
    
    for idx,name in enumerate(listData):
      if name[key_check]==given_value:
         moved_item = listData[idx]
         del listData[idx]
         listData.insert(0, moved_item)
         break
      
    # Write to JSON file
    write_into(json_file_name, listData)

    # print(f"Successfully moved to front of JSON array file: {moved_item}")
    
    
    
