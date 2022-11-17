from dash import html, dcc, dash_table


def create_dash_app_layout(db_dict):
    layout = html.Div([

        dcc.Dropdown(list(db_dict.keys()), list(db_dict.keys())[0], id='Dropdown-db'),

        dcc.RadioItems(['train', 'validation', 'test'], 'train', id='Radio-items-set'

                       ),

        dcc.Graph(id='target-graph', ),

        dcc.Graph(id='violin-graph', ),

        dcc.Graph(id='correlation-graph', ),

        dcc.Graph(id='number_of_multiples'),

        dcc.Graph(id='inverse_cumulative_hist'),

        dcc.Checklist(id='Dropdown-words',  # inline=True
                      ),

        dcc.Graph(id='bar-graph',  # hoverData={'points': [{'customdata': 'Japan'}]}
                  ),

        dash_table.DataTable(
            style_data={'whiteSpace': 'normal', 'height': 'auto', 'overflow': 'hidden', 'textOverflow': 'ellipsis',
                        # 'textAlign': 'left'

                        }, style_cell={'textAlign': 'left'},  # left align text in columns for readability
            page_size=5,

            id='table_reviews')

    ])
    return layout
