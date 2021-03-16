import json
import re


def _substitution_dict(path):
    '''
    create a dictionary where the key is either a phrase or synonym,
    and the value is the replacement token.

    >>> _substitution_dict('test-dictionary')
    {'Washington, D.C.': 'washington,_d.c.', 'Washington': 'washington,_d.c.', 'District of Columbia': 'washington,_d.c.', 'DC': 'washington,_d.c.', 'D.C.': 'washington,_d.c.', 'Washington D.C.': 'washington,_d.c.', 'Washington DC': 'washington,_d.c.'}
    '''
    sub_dict = {}
    # open the file
    with open(path, 'r') as f:
        # iterate through jsonl file
        for line in f:
            item_dict = json.loads(line).popitem()
            replacement_token = re.sub(' ', '_', item_dict[0].lower())

            # add original word to dict
            sub_dict.update({item_dict[0]: replacement_token})

            # add each synonym to dict
            for synonym in item_dict[1]:
                sub_dict.update({synonym: replacement_token})

        return sub_dict


def substitute_tokens(text, sub_dict):
    '''
    preprocess the training corpus by replacing each token that appears
    in the substitution_dict with its corresponding value.
    
    >>> substitute_tokens('Washington, D.C., formally the District of Columbia and also known as D.C. or just Washington, is the capital city of the United States of America.', 'test-dictionary')
    'washington,_d.c., formally the washington,_d.c. and also known as washington,_d.c. or just washington,_d.c., is the capital city of the United States of America'
    '''

    # lowercase and remove punctuation
    clean_text = re.sub('[^\w\s]', '', text).split()
    for token in clean_text:
        new_text = []
        # find tokens that match a key entry in the dictionary.



def syn_to_sub(dictionary):
    '''
    turn single synonym dict into sub_dict
    '''
    sub_dict = {}
    item_dict = dictionary.popitem()
    replacement_token = re.sub(' ', '_', item_dict[0].lower())

    # add original word to dict
    sub_dict.update({item_dict[0]: replacement_token})

    # add each synonym to dict
    for synonym in item_dict[1]:
        sub_dict.update({synonym: replacement_token})

    return sub_dict

#_substitution_dict('test-dictionary')
