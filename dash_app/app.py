from dash import Dash
from dash import dcc, html
from dash.dependencies import Input, Output

from dash_app.utils.dataset import DataSet
from dash_app.utils.plots import create_graf_histogram, create_violin_plots, create_correlation_plots

app = Dash(__name__)

db_information = [{
    'name': "clarin-pl/polemo2-official",
    'target_col': 'target',
    'mapper_values': {1: 'negatywne', 3: 'dwuznaczne', 0: 'neutralne', 2: 'pozytywne'}},

    {'name': 'allegro_reviews',
     'target_col': 'rating',
     'mapper_values': {1: 'bardzo negatywne', 2: 'negatywne', 3: 'neutralne dwuznaczne', 4: 'pozytywne',
                       5: 'bardzo pozytywne'}, }

]

db_dict = {values['name']: DataSet(**values) for values in db_information}
print(db_dict["clarin-pl/polemo2-official"].data)

app.layout = html.Div([dcc.Dropdown(list(db_dict.keys()), list(db_dict.keys())[0], id='Dropdown-db'

                                    ),

                       dcc.Graph(id='target-graph',  # hoverData={'points': [{'customdata': 'Japan'}]}
                                 ),

                       dcc.Graph(id='violin-graph',  # hoverData={'points': [{'customdata': 'Japan'}]}
                                 ),

                       dcc.Graph(id='correlation-graph',  # hoverData={'points': [{'customdata': 'Japan'}]}
                                 )

                       ])


@app.callback(Output('target-graph', 'figure'),

              Input('Dropdown-db', 'value'))
def update_histogram_graph(selected_db_name):
    dataset = db_dict[selected_db_name]
    hist_fig = create_graf_histogram(dataset.data, dataset.mapper_values)

    return hist_fig


@app.callback(Output('violin-graph', 'figure'),

              Input('Dropdown-db', 'value'))
def update_violin_graphs(selected_db_name):
    dataset = db_dict[selected_db_name]
    violin_fig = create_violin_plots(dataset.data)

    return violin_fig


@app.callback(Output('correlation-graph', 'figure'),

              Input('Dropdown-db', 'value'))
def update_violin_graphs(selected_db_name):
    dataset = db_dict[selected_db_name]
    correlation_plots = create_correlation_plots(dataset.data)

    return correlation_plots


if __name__ == '__main__':
    app.run_server(debug=True)
