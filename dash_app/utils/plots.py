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
        fig.append_trace(go.Violin(y=dataset[col], box_visible=True, line_color='black', meanline_visible=True,
                                   fillcolor='lightseagreen', opacity=0.6, x0=col.replace('_', " ")), row=1, col=i + 1)

    fig.update_layout(title_x=0.5, autosize=True, title_text="Tekst statystyk", showlegend=False)

    return fig


def create_correlation_plots(dataset):
    text_desc_col = [ 'liczba_znaków',"ocena_tekst"]
    df = dataset.to_pandas()
    # print(df.head())
    fig = px.violin(df[text_desc_col],color="ocena_tekst")
    return fig
