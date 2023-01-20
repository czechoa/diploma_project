import os

import pandas as pd
from datasets import Dataset, DatasetDict

def merge_datasets(polemo2, allegro, mask_allegro):

    path = f"data/połaczone_{mask_allegro.values()}"
    if os.path.exists(path):
        return DatasetDict.load_from_disk(path)

    merged = DatasetDict()

    for set_name in ['train', 'validation', 'test']:
        polemo2_data = polemo2.data[set_name].to_pandas()
        allegro_data = allegro.data[set_name].to_pandas()

        allegro_data['ocena_tekst'] = mask_allegro_ocena(allegro_data,mask_allegro)

        df_merged = pd.concat([allegro_data, polemo2_data])

        df_merged = remove_empty_token_tekst(df_merged)

        merged[set_name] = Dataset.from_pandas(df_merged)

    merged.save_to_disk(f"data/połaczone_{mask_allegro.values()}")

    return merged


def remove_empty_token_tekst(data):
    return data[data['token_tekst'].str.len() != 0]


def mask_allegro_ocena(allegro_data, mask_allegro:dict):
    rating_col = allegro_data['rating']
    for rating,mask in mask_allegro.items():
        allegro_data['ocena_tekst'] = allegro_data['ocena_tekst'].mask((rating_col == rating), mask)

    return allegro_data['ocena_tekst']

# def mask_polemo2_ocena(polemo2_data):
#     return polemo2_data['ocena_tekst'].mask(polemo2_data['ocena_tekst'] == 'dwuznaczne', 'neutralne')
