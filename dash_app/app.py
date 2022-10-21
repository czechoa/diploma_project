from dash import Dash
from dash import dcc, html
from dash.dependencies import Input, Output

from dash_app.utils.dataset import DataSet
from dash_app.utils.plots import create_graf_histogram

app = Dash(__name__)

db_information = [
    {
        'name': "clarin-pl/polemo2-official",

        'target_col': 'target',
        'mapper_values': {0: '0_neutral', 1: '1_negative', 2: '2_positive', 3: '3_ambiguous'},
    },
    {
        'name': 'allegro_reviews',
        'target_col': 'rating',
        'mapper_values': {1: '1_really_negative', 2: '2_negative', 3: '3_neutral', 4: '4_positive',
                          5: '5_really_positive'},
    }

]

db_dict = {values['name']: DataSet(**values) for values in db_information}

app.layout = html.Div([
    dcc.Dropdown(
        list(db_dict.keys()),
        list(db_dict.keys())[0],
        id='Dropdown-db'
    ),

    dcc.Graph(
        id='target-graf',
        # hoverData={'points': [{'customdata': 'Japan'}]}
    )

])


@app.callback(
    Output('target-graf', 'figure'),
    Input('Dropdown-db', 'value')
)
def update_graph(selected_db_name):
    dataset = db_dict[selected_db_name]
    print(dataset.__dict__)
    fig = create_graf_histogram(dataset.data[dataset.target_col],dataset.mapper_values)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
