import pandas as pd
from datasets import Dataset


def merge_datasets(polemo2, allegro):
    merged = {}

    for set_name in ['train', 'validation', 'test']:
        polemo2_data = polemo2.data[set_name].to_pandas()
        allegro_data = allegro.data[set_name].to_pandas()

        allegro_data['ocena_tekst'] = mask_allegro_ocena(allegro_data)

        polemo2_data['ocena_tekst'] = mask_polemo2_ocena(polemo2_data)

        df_merged = pd.concat([allegro_data, polemo2_data])

        df_merged = remove_empty_token_tekst(df_merged)

        merged[set_name] = Dataset.from_pandas(df_merged)

    return merged


def remove_empty_token_tekst(data):
    return data[data['token_tekst'].str.len() != 0]


def mask_allegro_ocena(allegro_data):
    rating = allegro_data['rating']

    return allegro_data['ocena_tekst'].mask((rating == 1) | (rating == 2), 'negatywne').mask(rating == 3,
                                                                                             'neutralne').mask(
        (rating == 4) | (rating == 5), 'pozytywne')


def mask_polemo2_ocena(polemo2_data):
    return polemo2_data['ocena_tekst'].mask(polemo2_data['ocena_tekst'] == 'dwuznaczne', 'neutralne')

# def get_only_positive_negative_rows(data):
#     return data[data['ocena_tekst'].str.contains(r"negatywn|pozytywn", regex=True)]
#
#
# def index_contains_name_rows(data, name):
#     return data['ocena_tekst'].str.contains(name, regex=True)
#
#
# def mask_ocena(data):
#     data['ocena_tekst'] = data['ocena_tekst'].mask(index_contains_name_rows(data, 'pozytywn'), 'pozytywne')
#     data['ocena_tekst'] = data['ocena_tekst'].mask(index_contains_name_rows(data, 'negatywn'), 'negatywne')
#
#     return data
#
#
# def mask_ocena_allegro(data):
#     rating = data['rating']
#     data['ocena_tekst'] = data.mask((rating == 1) | (rating == 2), 'negatywne').mask(rating == 3, 'neutralne').mask(
#         (rating == 4) | (rating == 5), 'pozytywne')
#     return data
#
#
# def mask_ocena_polemo2(data):
#     data['ocena_tekst'] = data['ocena_tekst'].mask(data['ocena_tekst'] == 'dwuznaczne', 'neutralne')
#     return data
