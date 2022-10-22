import re

from datasets import load_dataset

pl_char = 'żźćńółęąś'


def add_maper_values_to_mapper_function(mapper_values, target_col):
    return lambda x: maper_text_function(x, mapper_values,target_col)


def maper_text_function(row, mapper_values,target_col):
    text = row['text']

    n_of_sentences = count_sentences(text)
    n_of_words = count_words(text)
    len_text = count_characters(text)

    target = mapper_values[abs(row[target_col])]


    return {'liczba_zdań': n_of_sentences, 'liczba_słów': n_of_words, 'liczba_znaków': len_text, 'ocena_tekst': target}


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

    mapper_function = add_maper_values_to_mapper_function(mapper_values,target_col)

    dataDict = dataDict.map(mapper_function)

    return dataDict['train']
