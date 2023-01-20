from collections import Counter

import pandas as pd


def count_document_frequency(token_tekst, most_common):
    document_freq = {}
    frequency = 1 / len(token_tekst)

    for tokens in token_tekst:
        for w in set(tokens):
            if w in document_freq:
                document_freq[w] += frequency
            else:
                document_freq[w] = frequency

    return sorted(document_freq.items(), key=lambda item: -item[1])[:most_common]


def count_most_document_frequency_apply(col='token_tekst', the_most_common=10):
    return lambda group: count_document_frequency(group[col],
                                                  the_most_common)


def count_most_frequent_words_to_groupby(datadict, col):
    common_words = {}
    for set_name in datadict:
        data = datadict[set_name].to_pandas()

        data = data.groupby('ocena_tekst').apply(count_most_document_frequency_apply(col, 1000)).explode()

        data = pd.DataFrame(data=data.to_list(), columns=['word', 'count'],
                            index=data.index).reset_index()

        data['count'] = data['count'].astype(float)
        common_words[set_name] = data.sort_values('count', ascending=False)

    return common_words


def count_frequency_of_word_occurrence(datadict: list):
    results_counter = {}

    for set_name in datadict:
        token_tekst = datadict[set_name]['token_tekst']

        token_tekst = " ".join(map(lambda x: " ".join(x), token_tekst))

        result_counter = Counter(token_tekst.split())
        results_counter[set_name] = result_counter.values()
    return results_counter
