import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from dash_app.fronend.utils.plots.colors import return_default_colors


def create_distribution_of_responses_plot(data: list, maper_values, title='Rozkład odpowiedzi',
                                          label_name='ocena_tekst'):
    df = data.to_pandas()
    target = df.groupby(label_name).count()

    labels_names = list(dict.fromkeys(maper_values.values()))
    fig = go.Figure(data=[go.Bar(
        x=labels_names,
        y=100 * target.loc[labels_names, 'text'] / target['text'].sum(),
        marker_color=return_default_colors()
    )])

    fig.update_layout(title_x=0.5, autosize=True,
                      title_text=title
                      )
    fig.update_yaxes(title_text="Procent")

    return fig


def create_pdf_bar(word_counter):
    # print(pdf)
    fig = go.Figure(data=[go.Bar(x=word_counter.index[:10], y=word_counter.iloc[:10] * 100,
                                 # range_x=[0, 10],
                                 marker_color='lightseagreen'
                                 )])

    fig.update_yaxes(title_text="Procent")
    fig.update_xaxes(title_text="Liczba wielokrotności występowania tych samych tokenów")

    fig.update_layout(title_x=0.5, autosize=True,
                      title_text='Częstość wystepowania tokenów',
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

    fig = make_subplots(rows=1, cols=2,
                        # column_widths=[0.4, 0.6]
                        subplot_titles=("liczba zdań", "liczba słów a liczba tokenów",)
                        )
    col = text_desc_col[0]
    # col_names = "Czestość występowania"
    col_names = "Ilość przypadków"

    fig.add_trace(go.Violin(y=dataset[col]
                            , fillcolor='rgb(150, 10, 10)'
                            # , x0=col.replace('_', " ")
                            , x0=col_names

                            # ,side='positive', orientation='h'
                            , showlegend=False
                            ), row=1, col=1)

    col = text_desc_col[1]
    fig.add_trace(go.Violin(y=dataset[col], side='negative'
                            , fillcolor='mediumpurple'

                            , x0=col_names
                            , name="liczba słów"
                            , showlegend=False
                            ), row=1, col=2)

    col = text_desc_col[2]
    fig.add_trace(go.Violin(y=dataset[col], side='positive'
                            , fillcolor='lightseagreen'
                            , name="liczba tokenów"
                            , x0=col_names
                            , showlegend=False

                            ), row=1, col=2)

    fig.update_traces(meanline_visible=True,
                      opacity=0.6,
                      box_visible=True,
                      line_color='black'
                      , scalemode='count',
                      # xaxis_visible=False

                      )

    fig.update_layout(title_x=0.5,
                      autosize=True,
                      title_text="Statystyki długości tekstu",
                      # violingap=0, violingroupgap=0,
                      # violinmode='overlay'
                      # xaxis_showgrid=False
                      #   xaxis_visible = False
                      )

    return fig


# def create_bar_plots(graph_common_words, selected_group, colors_id):
#     fig = make_subplots(rows=len(graph_common_words), cols=1, subplot_titles=(
#         "Wszystkie", "Przymiotniki i przysłowki", "Dwa słowa koło siebie", "Trzy słowa koło siebie"),
#                         # vertical_spacing = 0.1,
#
#                         )
#
#     for i, dataset in enumerate(graph_common_words):
#         for color, t in zip(colors_id, selected_group):
#             dfp = dataset[dataset['ocena_tekst'] == t].iloc[:10]
#             fig.add_trace(
#                 go.Bar(x=dfp['word'], y=dfp['count'], name=t, marker_color=return_default_colors()[color],
#                        legendgroup=i,
#                        showlegend=False if i > 0 else True), row=1 + i, col=1)
#
#     fig.update_layout(height=900, title_x=0.5, autosize=True, title_text="Częstotliwość dokumentów (miara df)")
#
#     fig.update_yaxes(title_text="Częstość")
#
#     return fig
#

def create_bar_plots(graph_common_words, selected_group, colors_id):
    fig = make_subplots(rows=len(graph_common_words), cols=1, subplot_titles=(
        "Wszystkie", "Przymiotniki i przysłowki", "Dwa słowa koło siebie", "Trzy słowa koło siebie"),
                        # vertical_spacing = 0.1,

                        )

    for i, dataset in enumerate(graph_common_words):
        dataset = dataset[dataset['ocena_tekst'].isin(selected_group)]

        words = list(pd.unique(dataset['word']))[:10]

        # words = dataset.drop_duplicates(subset='word', keep='first', inplace=True)

        for color, label in zip(colors_id, selected_group):
            df =  dataset[dataset['ocena_tekst'] == label]

            # df = df.take(df[df['word'].isin(words)].order().index)
            # words = df.set_index('word').loc[words].reset_index()

            df = df[df['word'].isin(words)]


            fig.add_trace(
                go.Bar(x=df['word'], y=df['count']
                       , name=label
                       , marker_color=return_default_colors()[color],
                       legendgroup=i
                       , showlegend=False if i > 0 else True
                       )
                , row=1 + i, col=1)

    fig.update_layout(height=900, title_x=0.5, autosize=True, title_text="Częstotliwość dokumentów (miara df)",
                      # barmode='group'
                      )

    fig.update_yaxes(title_text="Częstość")

    return fig


def create_number_of_words_token_graph(dataset, frequency_of_word_occurrence):
    word_count = sum(dataset['liczba_słów'])
    word_count_unique = len(set(" ".join(dataset['text']).split(" ")))

    token_sum = sum(dataset['liczba_tokenów'])
    token_unique = len(frequency_of_word_occurrence)

    x_name = ['Liczba słów', 'Liczba tokenów']
    # x= ['liczba słów', 'liczba tokenów','liczba słów unikalnych',"liczba unikalnych tokenów"]
    fig = go.Figure()

    fig.add_traces(data=[
        go.Bar(x=x_name, y=[word_count, token_sum],
               name='suma wszytkich',
               # marker_color=['mediumpurple', 'lightseagreen']
               )
        ,
        go.Bar(x=x_name, y=[word_count_unique, token_unique],
               name='unikalna',
               # marker_color=['mediumpurple', 'lightseagreen']
               )
    ]
    )
    fig.update_layout(title_x=0.5, autosize=True,
                      title_text='Całkowita liczba słów oraz tokenów',
                      barmode='group'
                      )
    return fig


def create_text_grade_and_length_plots(dataset, maper_values):
    df = dataset.to_pandas()

    fig = go.Figure()

    labels_names = list(dict.fromkeys(maper_values.values()))

    for color, evaluation in enumerate(labels_names):
        fig.add_trace(go.Violin(x=df['ocena_tekst'][df['ocena_tekst'] == evaluation],
                                y=df['liczba_słów'][df['ocena_tekst'] == evaluation],
                                name=evaluation,
                                box_visible=True,
                                meanline_visible=True,
                                line_color=return_default_colors()[color]
                                ))

    fig.update_layout(title_x=0.5, autosize=True, title_text="Liczba słów a ocena")

    return fig
