from dash import Dash
from dash import dcc, html
from dash.dependencies import Input, Output

from dash_app.utils.dataset import DataSet
from dash_app.utils.plots import create_graf_histogram, create_violin_plots, create_correlation_plots, create_bar_plots

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

app = Dash(__name__)

app.layout = html.Div([

    dcc.Dropdown(list(db_dict.keys()), list(db_dict.keys())[0], id='Dropdown-db'
                 ),

    dcc.RadioItems(['train', 'validation', 'test'], 'train', id='Radio-items-set'
                   ),

    dcc.Graph(id='target-graph',
              ),

    dcc.Graph(id='violin-graph',
              ),

    dcc.Graph(id='correlation-graph',
              ),

    dcc.RadioItems(id='Dropdown-words',
                 ),

    dcc.Graph(id='bar-graph',  # hoverData={'points': [{'customdata': 'Japan'}]}
              ),

    # dcc.Graph(id='bar-graph',  # hoverData={'points': [{'customdata': 'Japan'}]}
    #           )

])


@app.callback(Output('target-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value'),
              )
def update_histogram_graph(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]
    hist_fig = create_graf_histogram(dataset.data[set_name], dataset.mapper_values)

    return hist_fig


@app.callback(Output('violin-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value'),
              )
def update_violin_graphs(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]
    violin_fig = create_violin_plots(dataset.data[set_name])

    return violin_fig


@app.callback(Output('correlation-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value')
              )
def update_violin_graphs(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]
    correlation_plots = create_correlation_plots(dataset.data[set_name])

    return correlation_plots


@app.callback(Output('Dropdown-words', 'options'),
              Output('Dropdown-words', 'value'),

              Input('Dropdown-db', 'value')
              )
def update_dropdown(selected_db_name):
    dataset = db_dict[selected_db_name]
    list_values = list(dataset.mapper_values.values())
    return list(dataset.mapper_values.values()), list_values[0]


@app.callback(Output('bar-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value'),
              Input('Dropdown-words', 'value')
              )
def update_bar_graph(selected_db, set_name, selected_group):
    dataset = db_dict[selected_db]
    most_common_words = dataset.common_words[set_name][selected_group]
    most_common_adj_adv = dataset.common_words_adj_adv[set_name][selected_group]
    fig = create_bar_plots(most_common_words, most_common_adj_adv)
    return fig


# @app.callback(Output('bar-graph', 'figure'),
#               Input('Dropdown-db', 'value'),
#               )
# def update_bar_graph(selected_db, selected_group):
#     dataset = db_dict[selected_db]
#     most_common_words = dataset.common_words[selected_group]
#     most_common_adj_adv = dataset.common_words_adj_adv[selected_group]
#     fig = create_bar_plots(most_common_words, most_common_adj_adv)
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
