import pandas as pd

from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import Row,column

auto = pd.read_excel('Downloads/Auto_Insu.xlsx')

def updateScatter(attr, old, new):
    cds_auto.data = dict(
            xVal = auto[xSelect.value],
            yVal = auto['City_MPG'])

cds_auto = ColumnDataSource(data = dict(
            xVal = auto['HP'],
            yVal = auto['City_MPG']))

scatter_chart = figure(height = 500, width = 500,
                       title = "Using Widgets",
                       x_axis_label = "HP",
                       y_axis_label = "City MPG")

xSelect = Select(title = "Select the X variable from the list",
                 options = ['HP','Length','Width'], value = 'HP')

scatter_chart.square(x='xVal', y='yVal', source=cds_auto)

xSelect.on_change('value', updateScatter)

curdoc().add_root(Row(xSelect,scatter_chart))