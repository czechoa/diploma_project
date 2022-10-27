from dash_app.utils.prepared_date import load_dataset_from_hugging_face
from dash_app.utils.words_counter import count_most_frequent_words_to_groupby


class DataSet:
    def __init__(self, name, mapper_values, target_col):
        self.name = name
        self.mapper_values = mapper_values
        self.target_col = target_col
        self.data = load_dataset_from_hugging_face(name, mapper_values, target_col)
        self.common_words = count_most_frequent_words_to_groupby(self.data, "token_tekst")
        self.common_words_adj_adv = count_most_frequent_words_to_groupby(self.data, "token_adj_adv")
