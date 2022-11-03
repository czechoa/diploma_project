from collections import Counter

import numpy as np
import pandas as pd


def count_most_frequent_words(text, divider=1, most_common=10):
    if isinstance(text, str):
        result_counter = Counter(text.split()).most_common(most_common)

    elif isinstance(text, list):
        result_counter = Counter(" ".join([" ".join(x) for x in text]).split()).most_common(most_common)
    else:
        raise TypeError("text should be list or str")

    result_counter = np.array(result_counter)
    result_counter[:, 1] = result_counter[:, 1].astype(float) / divider

    return result_counter


def count_most_frequent_words_apply(col='token_tekst', the_most_common=10):
    return lambda group: count_most_frequent_words(" ".join(group[col].str.join(" ").values), group.shape[0],
                                                   the_most_common)


def count_most_frequent_words_to_groupby(datadict, col):
    common_words = {}
    for set_name in datadict:
        data = datadict[set_name].to_pandas()

        data = data.groupby('ocena_tekst').apply(count_most_frequent_words_apply(col, 10)).explode()

        data = pd.DataFrame(data=data.to_list(), columns=['word', 'count'],
                            index=data.index).reset_index()
        data['count'] = data['count'].astype(float)
        common_words[set_name] = data.sort_values('count', ascending=False)

    return common_words

# common_words = data.groupby('ocena_tekst').apply(count_most_frequent_words_to_groupby('token_tekst', 20))
# common_words_adj_adv = data.groupby('ocena_tekst').apply(count_most_frequent_words_to_groupby('token_adj_adv', 20))
