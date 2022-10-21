import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def create_graf_histogram(target: list, maper_values, title='title', label_name='target'):

    fig = px.histogram(x=target, category_orders={'x': list(maper_values.values())}, histnorm='percent',
                       labels={'x': label_name}, title=title)

    fig.update_layout(title_x=0.5, title_font_size=25, autosize=True, # line_color='black',
        #  meanline_visible=True,
        font_color='white', hoverlabel_bordercolor='lightseagreen')

    fig.update_xaxes(rangeselector_font_size=20)

    return fig


def plot_print_text_statistics(dataset, target_col, mapper_values, title):
    text_desc_col = ['number_of_sentences', 'number_of_words', 'number_of_characters']
    print(dataset.to_pandas()[text_desc_col + [target_col]].describe())

    # target = list(map(lambda x: maper_values[x], dataset[target_col]))

    fig = make_subplots(rows=1, cols=3, # specs=[
                        #     [{"colspan": 3}, None, None],
                        #     [{}, {}, {}]
                        # ],
                        # subplot_titles=("Target","Second Subplot", "Third Subplot", 'a'),
                        )

    # fig.append_trace(
    #         go.Histogram(x=target,
    #         category_orders={'x': list(maper_values.values())}, histnorm='percent',
    #                    labels={'x': target_col}),
    #         row=1, col=1)

    for i, col in enumerate(text_desc_col):
        fig.append_trace(go.Violin(y=dataset[col], box_visible=True, line_color='black', meanline_visible=True,
                                   fillcolor='lightseagreen', opacity=0.6, x0=col.replace('_', " ")), row=1, col=i + 1)

    fig.update_layout(title_x=0.5, autosize=True, title_text="Distribution of text response", showlegend=False

    )

    plot_hist(dataset[target_col], mapper_values, title, target_col)

    fig.show()
