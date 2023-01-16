import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dash_app.fronend.utils.plots.colors import return_default_colors


def create_distribution_of_responses_plot(data: list, maper_values, title='Rozkład odpowiedzi',
                                          label_name='ocena_tekst'):
    df = data.to_pandas()
    target = df.groupby(label_name).count()

    fig = go.Figure(data=[go.Bar(
        x=list(maper_values.values()),
        y=100 * target.loc[list(maper_values.values()), 'text'] / target['text'].sum(),
        marker_color=return_default_colors()  # marker color can be a single color value or an iterable
    )])

    fig.update_layout(title_x=0.5, autosize=True,
                      title_text=title
                      )
    fig.update_yaxes(title_text="Procent")

    return fig


def create_pdf_bar(pdf):
    # print(pdf)
    fig = go.Figure(data=[go.Bar(x=pdf.index[:10], y=pdf.iloc[:10] * 100,
                                 # range_x=[0, 10],
                                 marker_color='lightseagreen'
                                 )])

    fig.update_yaxes(title_text="Procent")
    fig.update_xaxes(title_text="Liczba wielokrotności występowania słów")

    fig.update_layout(title_x=0.5,  autosize=True,
                      title_text='Funkcja gęstości prawdopodobieństwa (miara pdf)',
                      )
    return fig


def create_line_plot(inverse_cumulative):
    title = 'Odwortny histogram skumulowany'
    fig = go.Figure(go.Scatter(x=inverse_cumulative.index[:10] + 1,
                               y=inverse_cumulative[:10] * 100,
                               line_color='lightseagreen'
                               ))

    fig.update_yaxes(title_text="Procent")
    fig.update_xaxes(title_text="Liczba wielokrotnisci wystopowania słów ")

    fig.update_layout(title_x=0.5, autosize=True,
                      title_text='Odwrotny histogram skumulowany',
                      )
    return fig


def create_violin_plots(dataset):
    text_desc_col = ['liczba_zdań', 'liczba_słów', 'liczba_tokenów']

    fig = make_subplots(rows=1, cols=3,
                        )

    for i, col in enumerate(text_desc_col):
        fig.add_trace(go.Violin(y=dataset[col], box_visible=True, line_color='black', meanline_visible=True,
                                fillcolor='lightseagreen', opacity=0.6, x0=col.replace('_', " ")), row=1, col=i + 1)

    fig.update_layout(title_x=0.5, autosize=True, title_text="Długość tekst", showlegend=False)

    return fig


def create_bar_plots(graph_common_words, selected_group, colors_id):
    fig = make_subplots(rows=len(graph_common_words), cols=1, subplot_titles=(
        "Wszystkie", "Przymiotniki i przysłowki", "Dwa słowa koło siebie", "Trzy słowa koło siebie"),
                        # vertical_spacing = 0.1,

                        )

    for i, dataset in enumerate(graph_common_words):
        for color, t in zip(colors_id, selected_group):
            dfp = dataset[dataset['ocena_tekst'] == t]
            fig.add_trace(
                go.Bar(x=dfp['word'], y=dfp['count'], name=t, marker_color=return_default_colors()[color],
                       legendgroup=i,
                       showlegend=False if i > 0 else True), row=1 + i, col=1)

    fig.update_layout(height=900, title_x=0.5, autosize=True, title_text="Częstotliwość dokumentów (miara df)")

    fig.update_yaxes(title_text="Częstość")

    return fig


def create_text_grade_and_length_plots(dataset, maper_values):
    df = dataset.to_pandas()

    fig = go.Figure()

    for color, evaluation in enumerate(list(maper_values.values())):
        fig.add_trace(go.Violin(x=df['ocena_tekst'][df['ocena_tekst'] == evaluation],
                                y=df['liczba_słów'][df['ocena_tekst'] == evaluation],
                                name=evaluation,
                                box_visible=True,
                                meanline_visible=True,
                                line_color=return_default_colors()[color]
                                ))

    fig.update_layout(title_x=0.5, autosize=True, title_text="Liczba słów a ocena")

    return fig
