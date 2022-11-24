import re

import numpy as np
import psutil
# from autocorrect import Speller
from datasets import load_dataset

from dash_app.backend.utils.nlp.text_processing import tokenizing_text, get_adj_adv_from_text, autocorrect

# import language_tool_python

# spell = Speller(lang='pl')
# tool = language_tool_python.LanguageTool('pl-PL')

pl_char = 'żźćńółęąś'


def maper_text_function(row, mapper_values, target_col, ):
    text = row['text']

    text = replace_all_white_space_to_single_space(text)

    n_of_sentences = count_sentences(text)

    len_text = count_characters(text)

    target = mapper_values[abs(row[target_col])]

    token_text = tokenizing_text(text)

    token_text_with_autocorrect = tokenizing_text(autocorrect(text))

    n_of_words = len(token_text)

    token_adj_adv = get_adj_adv_from_text(text)

    subset_of_two_words = get_subset_of_two_words(token_text)

    subset_of_three_words = get_subset_of_three_words(token_text)

    return {'text': text,
            'liczba_zdań': n_of_sentences,
            'liczba_słów': n_of_words,
            'liczba_znaków': len_text,
            'ocena_tekst': target,
            'token_tekst': token_text,
            'token_tekst_with_autocorrect': token_text_with_autocorrect,
            'token_adj_adv': token_adj_adv,
            'subset_of_two_words': subset_of_two_words,
            'subset_of_three_words': subset_of_three_words
            }


def replace_all_white_space_to_single_space(text):
    return re.sub('\s+', " ", text).strip()


def add_maper_values_to_mapper_function(mapper_values, target_col):
    return lambda x: maper_text_function(x, mapper_values, target_col)


def get_subset_of_two_words(text):
    if len(text) > 2:
        return list(np.char.array(text[:-1]) + " " + np.char.array(text[1:]))
    return list(" ")


def get_subset_of_three_words(text):
    return list(np.char.array(text[:-2]) + " " + np.char.array(text[1:-1]) + " " + np.char.array(text[2:]))


def count_characters(text):
    return len(re.sub('\s+', "", text))


def count_words(text):
    pattern = f'[a-zA-z{pl_char}{pl_char.upper()}]+'
    return len(re.findall(pattern, text))


def count_sentences(text):
    pattern = f'(\.(\s*)[A-Z{pl_char.upper()}])|$'
    return len(re.findall(pattern, text))


def load_dataset_from_hugging_face(name=None, mapper_values=None, target_col=None):
    name = "clarin-pl/polemo2-official" if name is None else name

    dataDict = load_dataset(name)

    mapper_function = add_maper_values_to_mapper_function(mapper_values, target_col)

    dataDict = dataDict.map(mapper_function, num_proc=psutil.cpu_count(logical=True))

    return dataDict
