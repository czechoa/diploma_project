import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def create_graf_histogram(data: list, maper_values, title='Rozkład odpowiedzi', label_name='ocena_tekst'):
    target = data[label_name]

    fig = px.histogram(x=target, category_orders={'x': list(maper_values.values())}, histnorm='percent',
                       labels={'x': 'ocena'}, title=title)

    fig.update_layout(title_x=0.5, title_font_size=25, autosize=True,  # line_color='black',
                      #  meanline_visible=True,
                      # font_color='white',
                      hoverlabel_bordercolor='lightseagreen')
    fig.update_yaxes(title_text="Procent")

    return fig


def create_violin_plots(dataset):
    text_desc_col = ['liczba_zdań', 'liczba_słów', 'liczba_znaków']

    fig = make_subplots(rows=1, cols=3,  # specs=[
                        #     [{"colspan": 3}, None, None],
                        #     [{}, {}, {}]
                        # ],
                        # subplot_titles=("Target","Second Subplot", "Third Subplot", 'a'),
                        )

    for i, col in enumerate(text_desc_col):
        fig.add_trace(go.Violin(y=dataset[col], box_visible=True, line_color='black', meanline_visible=True,
                                fillcolor='lightseagreen', opacity=0.6, x0=col.replace('_', " ")), row=1, col=i + 1)

    fig.update_layout(title_x=0.5, autosize=True, title_text="Długość tekst", showlegend=False)

    return fig


def create_bar_plots(graph_common_words, selected_group):
    fig = make_subplots(rows=len(graph_common_words),
                        cols=1,
                        subplot_titles=("Wszystkie", "Przymiotniki i przysłowki", "Dwa słowa koło siebie","Trzy słowa koło siebie"),
                    # vertical_spacing = 0.1,

    )
    # colors = ["orange", "red", "green", "blue", "purple"]
    colors = px.colors.qualitative.Alphabet

    for i, dataset in enumerate(graph_common_words):
        for color, t in enumerate(selected_group):
            dfp = dataset[dataset['ocena_tekst'] == t]
            fig.add_trace(go.Bar(x=dfp['word'], y=dfp['count'], name=t, marker_color=colors[color], legendgroup=i, showlegend= False if i > 0 else True), row=1 + i, col=1)


    fig.update_layout(height=900, title_x=0.5, autosize=True, title_text="Częstotliwość dokumentów (miara df)")

    fig.update_yaxes(title_text="Częstość")
    # fig.update_layout(title_text="Stacked Subplots")
    # fig.update_xaxes(title_text="słowa")

    return fig


def create_correlation_plots(dataset):
    text_desc_col = ['liczba_znaków', "ocena_tekst"]
    df = dataset.to_pandas()
    # print(df.head())
    fig = px.violin(df[text_desc_col], color="ocena_tekst")
    fig.update_layout(title_x=0.5, autosize=True, title_text="Ilość znaków a ocena")

    return fig
