from dash_app.backend.utils.object.dataset import DataSet


def load_datasets():
    db_information = [{
        'name': "clarin-pl/polemo2-official",
        'target_col': 'target',
        'mapper_values': {1: 'negatywne', 3: 'dwuznaczne', 0: 'neutralne', 2: 'pozytywne'}},

        {'name': 'allegro_reviews',
         'target_col': 'rating',
         'mapper_values': {1: 'bardzo negatywne', 2: 'negatywne', 3: 'neutralne dwuznaczne', 4: 'pozytywne',
                           5: 'bardzo pozytywne'}}

    ]

    db_dict = {values['name']: DataSet(**values) for values in db_information}

    db_dict['połączone'] = DataSet('merge', {0: 'negatywne', 1: 'pozytywne'}, 'ocena_tekstu', db_dict.values())

    return db_dict
