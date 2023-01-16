import copy

from dash_app.backend.utils.object.dataset import DataSet


def load_datasets():
    db_information = [{
        'name': "clarin-pl/polemo2-official",
        'target_col': 'target',
        'mapper_values': {1: 'negatywne', 3: 'dwuznaczne', 0: 'neutralne', 2: 'pozytywne'}},

        {'name': 'allegro_reviews',
         'target_col': 'rating',
         'mapper_values': {1: 'bardzo negatywne', 2: 'negatywne', 3: 'dwuznaczne', 4: 'pozytywne',
                           5: 'bardzo pozytywne'}}

    ]

    db_dict = {values['name']: DataSet(**values) for values in db_information}
    polemo2_allegro = list(db_dict.values()).copy()


    db_dict['połączone_3_dwuznaczne'] = DataSet('merge', {1: 'negatywne', 2: 'negatywne',3: 'dwuznaczne', 4:'pozytywne', 5:'pozytywne'}, 'ocena_tekstu', polemo2_allegro)

    db_dict['połączone_2_3_4_dwuznaczne'] = DataSet('merge', {1: 'negatywne', 2: 'dwuznaczne',3: 'dwuznaczne', 4:'dwuznaczne', 5:'pozytywne'}, 'ocena_tekstu', polemo2_allegro)


    return db_dict
