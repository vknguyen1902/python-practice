#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import show, output_notebook, curdoc, output_file
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from bokeh.layouts import Row, Column
from bokeh.models import BoxSelectTool, NumeralTickFormatter, Select

# Add a SELECT widget that will allow a user to select from a dropdown [Variables to use: BoilerRetirement_dateEstimated, ComplianceDate, BoilerInstallationDate]. In short this will allow users to view:

# how many buildings will be retiring boilers in each year over a number of years
# how many buildings will be compliant in each year over a number of years
# how many buildings have installed boilers each year over a number of years

# Load dataset and view the first few rows
data = pd.read_excel('NYCOilConsumption-2018.xlsx')

# Event handler function for Line Chart
def updateLine(attr, old, new):
    print(old,new)
    
    # Update label of axes by the value selected from select widget lineSelect
    boiler_chart.yaxes.axis_label = lineSelect.value
    
    # Update data source accordingly to the lineSelect.value
    boiler_new = boiler.groupby([lineSelect.value]).count()
    boiler_new = boiler_new.rename(columns={'BBL_id':'NumberOfBuildings'}).reset_index()
    
    # Update column data source 
    cds_boiler.data = dict(xVal=boiler_new[lineSelect.value],
                           yVal=boiler_new['NumberOfBuildings'])

# Get building id and boiler retirement date 
boiler = data[['BBL_id','BoilerRetirement_dateEstimated',
               'ComplianceDate', 'BoilerInstallationDate']]
boiler = boiler.rename(columns={'BoilerRetirement_dateEstimated':'BoilerRetirement'})

boiler_default = boiler.groupby('BoilerRetirement').count().rename(columns={'BBL_id':'NumberOfBuildings'}).reset_index()

#boiler_default = meanCity

# Create column data source 
cds_boiler = ColumnDataSource(data=dict(xVal=boiler_default['BoilerRetirement'],
                                        yVal=boiler_default['NumberOfBuildings']))
#cds_boiler = cdsMean
                              
# Create figure for the chart
boiler_chart = figure(height=400, width=600,
                      title="Summarizing NYC Buildings Boiler Data",
                      x_axis_label = 'Years',
                      y_axis_label = 'Number of Buildings',
                      tools='lasso_select,box_select,pan,reset,tap')

# Add line glyph
boiler_chart.line(x='xVal', y='yVal', line_width=3,
                  line_color='coral', source=cds_boiler)

# Add circle glyph
boiler_chart.circle(x='xVal', y='yVal', size=7,
                    color='gray', alpha=0.6, source=cds_boiler)

# Make sure the y-axis started from zero
boiler_chart.y_range.start=0

# Create and add hover tooltips to our boiler_chart figure
boiler_hover = HoverTool(tooltips=[
    ("Year","@Year"), 
    ("Total Number of Buildings","@NumberOfBuildings")])
boiler_chart.add_tools(boiler_hover)

# Add SELECT widget
lineSelect = Select(title="Select a variable",
                    options=['BoilerRetirement',
                             'ComplianceDate', 
                             'BoilerInstallationDate'],
                    value='BoilerRetirement')

# Capture the event at change of value
lineSelect.on_change('value', updateLine)
                              
# Show chart
curdoc().add_root(Column(lineSelect, boiler_chart))

# --------------------------------------------------------------------------------------

# Create a chart that allows users to see total number of buildings within each buildingType for each of the fuel category [Fuel category to be selected from a dropdown]. The chart and its widget should appear below the chart and widget you created in question 

# [20 points] Create the chart using appropriate glyph such that buildingType is sorted by the number of buildings in the descending order.
## Add a SELECT widget that will allow a user to select from a dropdown a fuel type

# [5 points] Style the chart as follows:
    ## Make sure your chosen glyph has at least following properties specified as needed: color, nonselection_alpha, nonselection_color, and selection_color
    ## X axis should be labeled as ‘Types of Buildings in NYC’ and Y axis should be labeled as ‘Total number of Buildings’. 
    ## Chart title should be ‘Which buildings use what fuel?’
    ## Format X and Y axis tick marks as needed including label orientation

# [5 points] Add plot tools as follows:
    ## Add hover tooltips to show 
    ## Type of Building
    ## Fuel used
    ## Total number of buildings
    ## Also include only following plot tools: pan, reset, and tap. 







