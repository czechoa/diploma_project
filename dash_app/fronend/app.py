import pandas as pd
from dash import Dash, html
from dash.dependencies import Input, Output

from dash_app.backend.db_dictonary import load_datasets
from dash_app.fronend.dash_layout import create_dash_app_layout
from dash_app.fronend.utils.plots.colors import return_default_colors
from dash_app.fronend.utils.plots.plots import create_distribution_of_responses_plot, create_violin_plots, \
    create_bar_plots, create_line_plot, create_pdf_bar, create_text_grade_and_length_plots, \
    create_number_of_words_token_graph

db_dict = load_datasets()

app = Dash(__name__)

app.layout = create_dash_app_layout(db_dict)


def get_set_mapper_value(dataset,set_name):
    unique_class = set(dataset.data[set_name]['ocena_tekst'])
    mapper_values = [x for x in dataset.mapper_values.values() if x in list(unique_class)]
    return mapper_values


@app.callback(Output('target-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value'),
              )
def update_histogram_graph(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]
    data = dataset.data[set_name]
    mapper_values = get_set_mapper_value(dataset,set_name)

    hist_fig = create_distribution_of_responses_plot(data, mapper_values)

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
def update_correlation_graphs(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]

    data = dataset.data[set_name]
    # unique_class = data['ocena_tekstu'].unique()
    # mapper_values = [x for x in  dataset.mapper_values.values() if x in list(unique_class) ]
    mapper_values = get_set_mapper_value(dataset,set_name)
    correlation_plots = create_text_grade_and_length_plots(data, mapper_values)

    return correlation_plots


@app.callback(Output('number-of-words-token-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value')
              )
def update_number_of_words_token_graph(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]
    number_of_words_token_graph = create_number_of_words_token_graph(dataset.data[set_name],
                                                                     dataset.frequency_of_word_occurrence[set_name])

    return number_of_words_token_graph


@app.callback(Output('number_of_multiples', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value')
              )
def update_number_of_multiples_graphs(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]

    frequency_of_word = pd.Series(dataset.frequency_of_word_occurrence[set_name])
    n_words = len(frequency_of_word)
    pdf = frequency_of_word.value_counts().sort_index() / n_words
    return create_pdf_bar(pdf)


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

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value')
              )
def update_dropdown(selected_db_name, set_name):
    dataset = db_dict[selected_db_name]

    mapper_values = get_set_mapper_value(dataset,set_name)

    labels_names = list(dict.fromkeys(mapper_values))

    options = [{"label": html.Label([str(value)],
                                    style={'color': color, 'font-size': 20
                                           }),
                "value": str(value)
                }
               for value, color in zip(labels_names, return_default_colors()[:len(labels_names)])
               ]

    return options, labels_names


@app.callback(Output('bar-graph', 'figure'),

              Input('Dropdown-db', 'value'),
              Input('Radio-items-set', 'value'),
              Input('Dropdown-words', 'value'),
              Input('Dropdown-words', 'options')
              )
def update_common_words_graphs(selected_db, set_name, selected_group, options):
    dataset = db_dict[selected_db]

    most_common_words = dataset.common_words[set_name]
    most_common_adj_adv_verb = dataset.common_words_adj_adv_verb[set_name]

    subset_of_two_words = dataset.subset_of_two_words[set_name]
    subset_of_three_words = dataset.subset_of_three_words[set_name]

    graph_common_words = [most_common_words, most_common_adj_adv_verb, subset_of_two_words, subset_of_three_words]
    colors_id, selected_group = zip(
        *[(i, option['value']) for i, option in enumerate(options) if option['value'] in selected_group])

    fig = create_bar_plots(graph_common_words, selected_group, colors_id)

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
