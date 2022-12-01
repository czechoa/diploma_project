from dash_app.backend.utils.nlp.words_counter import count_most_frequent_words_to_groupby, \
    count_frequency_of_word_occurrence
from dash_app.backend.utils.object.merge_datasets.merge import merge_datasets
from dash_app.backend.utils.prepared_date import load_dataset_from_hugging_face


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

        self.common_words_adj_adv_verb = count_most_frequent_words_to_groupby(self.data, "token_adj_adv_verb")

        self.subset_of_two_words = count_most_frequent_words_to_groupby(self.data, "subset_of_two_words")

        self.subset_of_three_words = count_most_frequent_words_to_groupby(self.data, "subset_of_three_words")

        self.frequency_of_word_occurrence = count_frequency_of_word_occurrence(self.data)
