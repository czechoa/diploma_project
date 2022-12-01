import pandas as pd
from datasets import Dataset


def merge_datasets(polemo2, allegro):
    merged = {}

    for set_name in ['train', 'validation', 'test']:
        polemo2_data = polemo2.data[set_name].to_pandas()
        allegro_data = allegro.data[set_name].to_pandas()

        allegro_data['ocena_tekst'] = mask_allegro_ocena(allegro_data)

        # polemo2_data['ocena_tekst'] = mask_polemo2_ocena(polemo2_data)

        df_merged = pd.concat([allegro_data, polemo2_data])

        df_merged = remove_empty_token_tekst(df_merged)

        merged[set_name] = Dataset.from_pandas(df_merged)

    return merged


def remove_empty_token_tekst(data):
    return data[data['token_tekst'].str.len() != 0]


def mask_allegro_ocena(allegro_data):
    rating = allegro_data['rating']

    return allegro_data['ocena_tekst'].mask((rating == 1) | (rating == 2), 'negatywne').mask(
        (rating == 3) | (rating == 4), 'dwuznaczne').mask((rating == 5), 'pozytywne')

# def mask_polemo2_ocena(polemo2_data):
#     return polemo2_data['ocena_tekst'].mask(polemo2_data['ocena_tekst'] == 'dwuznaczne', 'neutralne')
