import pandas as pd
from dash import Dash, html
from dash.dependencies import Input, Output

from dash_app.backend.db_dictonary import load_datasets
from dash_app.fronend.dash_layout import create_dash_app_layout
from dash_app.fronend.utils.plots.colors import default_colors
from dash_app.fronend.utils.plots.plots import create_graf_histogram, create_violin_plots, create_correlation_plots, \
    create_bar_plots, create_line_plot, create_bar_pdf_plot

db_dict = load_datasets()

app = Dash(__name__)

app.layout = create_dash_app_layout(db_dict)


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


@app.callback(Output('number_of_multiples', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value')
              )
def update_number_of_multiples_graphs(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]

    frequency_of_word = pd.Series(dataset.frequency_of_word_occurrence[set_name])
    n_words = len(frequency_of_word)
    pdf = frequency_of_word.value_counts().sort_index() / n_words
    return create_bar_pdf_plot(pdf)


@app.callback(Output('inverse_cumulative_hist', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value')
              )
def update_inverse_cumulative_hist_graphs(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]

    frequency_of_word = pd.Series(dataset.frequency_of_word_occurrence[set_name])
    n_words = len(frequency_of_word)
    # pdf = frequency_of_word.value_counts().sort_index().cumsum()
    inverse_cumulative = 1 - frequency_of_word.value_counts().sort_index().cumsum() / n_words
    inverse_cumulative = pd.concat([pd.Series([1]), inverse_cumulative], ignore_index=True)

    return create_line_plot(inverse_cumulative)


@app.callback(Output('Dropdown-words', 'options'),
              Output('Dropdown-words', 'value'),

              Input('Dropdown-db', 'value')
              )
def update_dropdown(selected_db_name):
    dataset = db_dict[selected_db_name]
    list_values = list(dataset.mapper_values.values())

    options = [{"label": html.Label([str(value)],
                                    style={'color': color, 'font-size': 20
                                           }),
                "value": str(value)
                }
               for value, color in zip(list_values, default_colors[:len(list_values)])
               ]

    return options, list_values


@app.callback(Output('bar-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value'),
              Input('Dropdown-words', 'value')
              )
def update_bar_graph(selected_db, set_name, selected_group):
    dataset = db_dict[selected_db]

    most_common_words = dataset.common_words[set_name]
    most_common_adj_adv = dataset.common_words_adj_adv[set_name]

    subset_of_two_words = dataset.subset_of_two_words[set_name]
    subset_of_three_words = dataset.subset_of_three_words[set_name]

    graph_common_words = [most_common_words, most_common_adj_adv, subset_of_two_words, subset_of_three_words]

    fig = create_bar_plots(graph_common_words, selected_group)
    return fig


@app.callback(
    Output('table_reviews', 'data'),
    Input('Dropdown-db', 'value'),
    Input('Radio-items-set', 'value'),
    Input('Dropdown-words', 'value')

)
def update_table_review(selected_db, set_name, selected_group):
    dataset = db_dict[selected_db]

    data = dataset.data[set_name].to_pandas()[['ocena_tekst', 'text']]
    data = data[data['ocena_tekst'].isin(selected_group)]

    return data.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
