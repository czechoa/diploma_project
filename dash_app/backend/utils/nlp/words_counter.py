# from collections import Counter

# import numpy as np
import pandas as pd


# from sklearn.feature_extraction.text import CountVectorizer


# def count_most_frequent_words(text, divider=1, most_common=10):
#     if isinstance(text, str):
#         result_counter = Counter(text.split())
#
#     elif isinstance(text, list):
#         # result_counter = Counter(" ".join([" ".join(x) for x in text]).split()).most_common(most_common)
#         result_counter = Counter(text)
#
#     else:
#         raise TypeError("text should be list or str")
#
#     divider = sum(result_counter.values())
#     result_counter = result_counter.most_common(most_common)
#
#     result_counter = np.array(result_counter)
#     result_counter[:, 1] = result_counter[:, 1].astype(float) / divider
#
#     return result_counter


# def count_documnet_frequency_by_CountVectorizer(token_tekst, divider, most_common):
#     docs = list(token_tekst.str.join(" "))
#
#     cv = CountVectorizer()
#     word_count_vector = cv.fit_transform(docs) > 0
#     # word_count_vector = cv.fit_transform(docs)
#
#     tf = pd.DataFrame(word_count_vector.toarray(), columns=cv.get_feature_names_out())
#     cv_sum = tf.sum().reset_index().sort_values(0, ascending=False)
#     cv_sum['value'] = cv_sum[0] / divider
#     # cv_sum['value'] = cv_sum[0] / tf.sum().sum()
#     cv_sum = cv_sum.drop(0, axis=1)
#
#     return cv_sum[0:most_common].values


# def flatten_nested_list(nested_list):
#     out = []
#     for text in nested_list:
#         out.extend(text)
#     return out

# def count_most_frequent_words_apply(col='token_tekst', the_most_common=10):
#     return lambda group: count_most_frequent_words(flatten_nested_list(group[col]), group.shape[0],
#                                                    the_most_common)
#


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

        data = data.groupby('ocena_tekst').apply(count_most_document_frequency_apply(col, 10)).explode()

        data = pd.DataFrame(data=data.to_list(), columns=['word', 'count'],
                            index=data.index).reset_index()

        data['count'] = data['count'].astype(float)
        common_words[set_name] = data.sort_values('count', ascending=False)

    return common_words

# common_words = data.groupby('ocena_tekst').apply(count_most_frequent_words_to_groupby('token_tekst', 20))
# common_words_adj_adv = data.groupby('ocena_tekst').apply(count_most_frequent_words_to_groupby('token_adj_adv', 20))
