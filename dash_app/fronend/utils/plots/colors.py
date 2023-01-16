# default_colors = ['#1f77b4',  # muted blue
#                   '#ff7f0e',  # safety orange
#                   '#2ca02c',  # cooked asparagus green
#                   '#d62728',  # brick red
#                   '#9467bd',  # muted purple
#                   '#8c564b',  # chestnut brown
#                   '#e377c2',  # raspberry yogurt pink
#                   '#7f7f7f',  # middle gray
#                   '#bcbd22',  # curry yellow-green
#                   '#17becf'  # blue-teal
#                   ]

import plotly.express as px


def return_default_colors():
    return px.colors.sequential.Turbo[::3]