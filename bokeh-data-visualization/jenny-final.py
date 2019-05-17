from bokeh.plotting import figure
from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.models import ColumnDataSource, Select, Slider, CheckboxGroup, GMapOptions, HoverTool, TextInput, WheelZoomTool, NumeralTickFormatter
from bokeh.layouts import Row, Column
from bokeh.plotting import gmap
from bokeh.palettes import Category20c
from bokeh.transform import factor_cmap
from math import pi
import pandas as pd

df = pd.read_excel('NYCOilConsumption-2018.xlsx')
df.head()
df.columns


# =============================================================================
# add a SELECT widget to Q5 that will allow a user to select from a dropdown [Variables to use: BoilerRetirement_dateEstimated, ComplianceDate, BoilerInstallationDate]. In short this will allow users to view:
# h.	how many buildings will be retiring boilers in each year over a number of years
# i.	how many buildings will be compliant in each year over a number of years
# j.	how many buildings have installed boilers each year over a number of years
# =============================================================================

def updateLine(attr, old, new):
    print(old, new)
    dfNew = df.groupby(xSelect.value)['BBL_id'].count().reset_index()
    cds.data = dict(xVal=dfNew[xSelect.value],
                    yVal=dfNew['BBL_id'])
    line.xaxis.axis_label=xSelect.value
    
retire = df.groupby('BoilerRetirement_dateEstimated')['BBL_id'].count().reset_index()
print(retire)
cds = ColumnDataSource(data=dict(xVal = retire['BoilerRetirement_dateEstimated'],
                                 yVal = retire['BBL_id']))
cds.column_names


line=figure(height=400, width=600,
           title='Summarizing NYC Buildings Data',
            tools=['tap', 'lasso_select', 'box_select', 'pan', 'reset']
           )
line.circle(x='xVal', y='yVal',
           size=10, color='blue',
            alpha=.75,
            selection_color='orange',
            nonselection_fill_alpha=.5,
            nonselection_color='blue',
           source=cds)
line.line(x='xVal', y='yVal',
         color='red',
          line_width=2,
          nonselection_alpha=.5,
          nonselection_color='blue',
          source=cds)

line.xaxis.axis_label = "Years"
line.yaxis.axis_label = "Number of buildings"

lineHover = HoverTool(tooltips=[('Year','@xVal'),
                              ('# of buildings', '@yVal')])
line.add_tools(lineHover)

xSelect = Select(title='Select the X variable from the list',
                 options=['BoilerRetirement_dateEstimated','ComplianceDate','BoilerInstallationDate'],
                 value='BoilerRetirement_dateEstimated')
xSelect.on_change('value', updateLine)



# =============================================================================
# create a chart that allows users to see total number of buildings within each buildingType 
# for each of the fuel category [Fuel category to be selected from a dropdown]. The chart and 
# its widget should appear below the chart and widget you created in question # 6
# =============================================================================

cdsbtu = ColumnDataSource(data=dict(area = df['BuildingArea'],
                                    high=df['TotalConsumption_HighEstimateMMBTUs'],
                                     low=df['TotalConsumption_LowEstimateMMBTUs'],
                                     addr=df['FacilityAddress'],
                                     comp=df['ComplyWithGreenerBuildingsLaws'],
                                     fuel=df['PrimaryFuel'],
                                     btype=df['BuildingType'],
                                     neighborhood=df['NTA']
                                    ))

#Scatter plot 1
scatHigh = figure(height=400, width=600,
                 title='Examining Estimated High BTU Consumption by Building Area',
                 tools=['tap', 'lasso_select', 'box_select', 'pan', 'reset', 'wheel_zoom', 'box_zoom'])
scatHigh.circle(x='area',
              y='high',
                size=3, color='blue',
            alpha=.75,
            selection_color='orange',
            nonselection_fill_alpha=.5,
            nonselection_color='gray',
             source = cdsbtu)
scatHigh.xaxis[0].formatter = NumeralTickFormatter(format="0a")
scatHigh.yaxis[0].formatter = NumeralTickFormatter(format="0a")
scatHigh.xaxis.axis_label='Building Area in SF'
scatHigh.yaxis.axis_label='Fuel consumption in BTUs'
scatHigh.x_range.start=0
scatHigh.y_range.start=0

highHover=HoverTool(tooltips=[('Facility Address', '@addr'),
                            ('Compliance with Greener Buildings Laws', '@comp'),
                            ('Primary fuel used in boilers', '@fuel'),
                            ('Type of building', '@btype'),
                            ('Neighborhood', '@neighborhood')])
scatHigh.add_tools(highHover)


#Scatter plot 2
scatLow = figure(height=400, width=600,
                 title='Examining Estimated High BTU Consumption by Building Area',
                 tools=['tap', 'lasso_select', 'box_select', 'pan', 'reset', 'wheel_zoom', 'box_zoom'],
                x_range=scatHigh.x_range,
                y_range=scatHigh.y_range)
scatLow.circle(x='area',
              y='low',
                size=3, color='red',
            alpha=.75,
            selection_color='orange',
            nonselection_fill_alpha=.5,
            nonselection_color='gray',
             source = cdsbtu)
scatLow.xaxis[0].formatter = NumeralTickFormatter(format="0a")
scatLow.yaxis[0].formatter = NumeralTickFormatter(format="0a")
scatLow.xaxis.axis_label='Building Area in SF'
scatLow.yaxis.axis_label='Fuel consumption in BTUs'
scatLow.x_range.start=0
scatLow.y_range.start=0

lowHover=HoverTool(tooltips=[('Facility Address', '@addr'),
                            ('Compliance with Greener Buildings Laws', '@comp'),
                            ('Primary fuel used in boilers', '@fuel'),
                            ('Type of building', '@btype'),
                            ('Neighborhood', '@neighborhood')])
scatLow.add_tools(lowHover)

#Chart 3
def updateBar(attr, old, new):
    print(old, new)
    dfNew = dfbar[dfbar['PrimaryFuel'] == fuelSelect.value]
    dfNew.sort_values(by=['BBL_id'], ascending=False)
    cdsbar.data = dict(btype=dfNew['BuildingType'],
                       fuel=dfNew['PrimaryFuel'],
                       count=dfNew['BBL_id'])
    
dfbar = df.groupby(['PrimaryFuel','BuildingType'])['BBL_id'].count().reset_index()

#sliece dfbar for initial value of select
dfbarDef = dfbar[dfbar['PrimaryFuel'] == '4 (Clean Oil)']
dfbarDef = dfbarDef.sort_values(by=['BBL_id'], ascending=False)

print(dfbarDef)

cdsbar = ColumnDataSource(data=dict(btype=dfbarDef['BuildingType'],
                                    fuel=dfbarDef['PrimaryFuel'],
                                    count=dfbarDef['BBL_id']))
print(cdsbar.column_names)

bar = figure(height=500, width=1000,
             x_range=list(dfbarDef['BuildingType'].unique()),
             title='Which buildings use what fuel?',
             tools=['pan', 'reset', 'tap'])

bar.xaxis.axis_label='Types of Buildings in NYC'
bar.yaxis.axis_label='Total number of Buildings'

bar.xaxis.major_label_orientation = pi/3


barColor = factor_cmap('btype',
                      palette=Category20c[20],
                      factors=sorted(df['BuildingType'].unique()))

bar.vbar(x='btype', top='count',
         width=.3,
         color=barColor,
         source=cdsbar)

fuelSelect = Select(title='Select the fuel type',
                    options=list(df['PrimaryFuel'].unique()),
                    value='4 (Clean Oil)')

fuelSelect.on_change('value', updateBar)

barHover=HoverTool(tooltips=[('Type of building','@btype'),
                             ('Fuel used', '@fuel'),
                             ('Total # of buildings', '@count')])

bar.add_tools(barHover)

curdoc().add_root(Column(Column(xSelect, line), Row(scatHigh,scatLow), Column(fuelSelect, bar)))

