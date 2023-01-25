import pandas as pd

from dash_app.backend.db_dictonary import load_datasets
from unidecode import unidecode
from pretty_confusion_matrix import pp_matrix


def get_unicode_text(col, train, validation, test, token_pattern):
    # texts_org = train[col].str.join(token_pattern)
    # texts = texts_org.apply(unidecode)

    texts = get_unicode_text_from_set(col, train, token_pattern)

    texts_val = get_unicode_text_from_set(col, validation, token_pattern)

    # texts_test = test[col].str.join(token_pattern).apply(unidecode)
    texts_test = get_unicode_text_from_set(col, test, token_pattern)
    return texts, texts_val, texts_test


def get_unicode_text_from_set(col, set, token_pattern):
    return set[col].str.join(token_pattern).apply(unidecode)


def get_polaczone_dataset_and_split():
    db_dict = load_datasets()
    merged_data = db_dict['połączone'].data
    train = merged_data['train'].to_pandas()
    validation = merged_data['validation'].to_pandas()
    return train, validation


def get_polaczone_dataset_and_split():
    db_dict = load_datasets()
    merged_data = db_dict['połączone'].data
    train = merged_data['train'].to_pandas()
    validation = merged_data['validation'].to_pandas()
    test = merged_data['test'].to_pandas()

    return train, validation, test


def map_target_result(data):
    mapper_target_value = {
        'negatywne': 0,
        'dwuznaczne': 1,
        'pozytywne': 2,
        'neutralne': 3,

    }

    return list(map(lambda x: mapper_target_value[x], data['ocena_tekst']))


def plot_and_print_score_model(target_val, y_pred, target_names=None):
    if target_names is None: target_names = ['pozytywne', 'dwuznaczne', 'negatywne']

    conf_matrix = confusion_matrix(y_true=target_val, y_pred=y_pred)
    #
    # fig, ax = plt.subplots(figsize=(5, 5))
    # ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
    # for i in range(conf_matrix.shape[0]):
    #     for j in range(conf_matrix.shape[1]):
    #         ax.text(x=j, y=i, s=conf_matrix[i, j], va='center', ha='center', size='xx-large')
    #
    # plt.xlabel('Predictions', fontsize=18)
    # plt.ylabel('Actuals', fontsize=18)
    # plt.title('Confusion Matrix', fontsize=18)
    # plt.show()
    df_cm = pd.DataFrame(data=conf_matrix, index=target_names, columns=target_names)
    pp_matrix(df_cm)

    print(metrics.classification_report(target_val, y_pred,
                                        # target_names=target_names,
                                        digits=3))


from sklearn import metrics
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix


def model_fit__and_model_statistics(model, text, target, text_val, target_val, target_names=None, text_test=None,
                                    target_test=None):
    model.fit(text, target)
    print('train dataset:\n')
    y_pred_train = model.predict(text)

    plot_and_print_score_model(target, y_pred_train, target_names)

    print('validate dataset:\n')
    y_pred = model.predict(text_val)
    plot_and_print_score_model(target_val, y_pred, target_names)

    if text_test is not None and target_test is not None:
        print('test:')

        y_pred = model.predict(text_test)
        plot_and_print_score_model(target_test, y_pred, target_names)
