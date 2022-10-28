from dash_app.utils.prepared_date import load_dataset_from_hugging_face
from dash_app.utils.words_counter import count_most_frequent_words_to_groupby


class DataSet:
    def __init__(self, name, mapper_values, target_col, merged_Dataset=None):
        self.name = name
        self.mapper_values = mapper_values
        self.target_col = target_col

        if not merged_Dataset:
            self.data = load_dataset_from_hugging_face(name, mapper_values, target_col)
        else:
            self.data = merge_datasets(*merged_Dataset)

        self.common_words = count_most_frequent_words_to_groupby(self.data, "token_tekst")
        self.common_words_adj_adv = count_most_frequent_words_to_groupby(self.data, "token_adj_adv")


from datasets import Dataset
import pandas as pd


def merge_datasets(polemo2, allegro_reviews):
    merged = {}

    for set_name in ['train', 'validation', 'test']:
        polemo2_data = polemo2.data[set_name].to_pandas()
        allegro_reviews_data = allegro_reviews.data[set_name].to_pandas()

        allegro_reviews_data = mask_ocena(allegro_reviews_data)

        allegro_reviews_data = get_only_positive_negative_rows(allegro_reviews_data)
        polemo2_data = get_only_positive_negative_rows(polemo2_data)

        merged[set_name] = Dataset.from_pandas(pd.concat([allegro_reviews_data, polemo2_data]))

    return merged


def get_only_positive_negative_rows(data):
    return data[data['ocena_tekst'].str.contains(r"negatywn|pozytywn", regex=True)]


def index_contains_name_rows(data, name):
    return data['ocena_tekst'].str.contains(name, regex=True)


def mask_ocena(data):
    data['ocena_tekst'] = data['ocena_tekst'].mask(index_contains_name_rows(data, 'pozytywn'), 'pozytywne')
    data['ocena_tekst'] = data['ocena_tekst'].mask(index_contains_name_rows(data, 'negatywn'), 'negatywne')

    return data
