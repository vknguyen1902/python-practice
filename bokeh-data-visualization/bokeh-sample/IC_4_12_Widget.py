import pandas as pd

from bokeh.plotting import figure
from bokeh.io import curdoc, output_file, show
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import Row

def updateScatter(attr, old, new):
    print(old, new)
    #update CDS
    cdsAuto.data= dict(
            xVal=dfAuto[xSelect.value],
            yVal=dfAuto['City_MPG'])
    scatChart.xaxis.axis_label=xSelect.value
    
dfAuto = pd.read_excel('data/Auto_Insu.xlsx')

cdsAuto = ColumnDataSource(data=dict(
         xVal = dfAuto['HP'],
         yVal = dfAuto['City_MPG']))

xSelect = Select(title="Select the X variable from the list",
                 options=['HP','Length','Width'],
                 value='HP')
# Figure
scatChart = figure(height=500, width=500,
                   title="Using Widgets",
                   x_axis_label="HP",
                   y_axis_label="City MPG")

scatChart.square(x='xVal', y='yVal',source=cdsAuto)

xSelect.on_change('value', updateScatter)

#output_file('Scat1.html')
#show(Row(xSelect,scatChart))

curdoc().add_root(Row(xSelect,scatChart))

# Glyph