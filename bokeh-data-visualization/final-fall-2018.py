#!/usr/bin/env python
# coding: utf-8

# # NYC Building Oil Consumption for Year 2017
# 1. Data Inspection and Preparation
# 2. Number of buildings becoming retiring boilers over years (line and dots)
# 3. Estimated high and low BTU consumption by building area (two charts)

# In[1]:


import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import show, output_notebook
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap
from bokeh.layouts import Row, Column
from bokeh.models import BoxSelectTool, NumeralTickFormatter

output_notebook()


# ## 1. Data Inspection and Preparation
# - View data, print columns, inspect data types
# - Assign columns needed to ``boiler`` for boiler retirement plot
# - Assign columns needed to ``btu`` for plots on BTU consumption by building area <br>
# 
# <p>Note: HoverTool still cannot handle column name with space, so it's good practice to avoid having column name with space.</p>

# In[2]:


# Load dataset and view the first few rows
data = pd.read_excel('NYCOilConsumption-2018.xlsx')
data.head()


# In[3]:


# Print all available columns for easy grabs later
print(data.columns)

# Inspect the variable data types
data.info()


# In[4]:


# Get building id and boiler retirement date 
boiler = data[['BBL_id','BoilerRetirement_dateEstimated']]
boiler = boiler.rename(columns={'BoilerRetirement_dateEstimated':'Year'})
boiler = boiler.groupby('Year').count().rename(columns={'BBL_id':'NumberOfBuildings'}).reset_index()
boiler.head()


# In[5]:


# Get columns for BTU consumption (heat consumption)
btu = data[['BuildingArea', 'TotalConsumption_HighEstimateMMBTUs', 
            'TotalConsumption_LowEstimateMMBTUs','FacilityAddress',
            'ComplyWithGreenerBuildingsLaws','BuildingType','NTA',
            'PrimaryFuel']]

# Rename columns to make life easier
btu = btu.rename(columns={'TotalConsumption_HighEstimateMMBTUs':'HighEstimate',
                          'TotalConsumption_LowEstimateMMBTUs':'LowEstimate',
                          'ComplyWithGreenerBuildingsLaws':'GreenBuilding'})
btu.head()


# ## 2. Retiring Boilers Over Years
# - Use ``boiler`` to plot the number of buildings that will have retired boilders over years
# - Create a ``boiler_chart`` figure and add line and circle glyphs
# - Make sure dots and lines have at least following properties specified as needed: Size, color, nonselection_alpha, nonselection_color, and selection_color
# - X axis should be labeled as '<strong>Years</strong>' and Y axis should be labeled as '<strong>Number of Buildings</strong>'
# - Chart title should be ‘<strong>Summarizing NYC Buildings Boiler Data</strong>’
# - Add hover tooltips to show <strong>Year</strong> and <strong>Total Number of Buildings</strong>
# - Include lasso select, box select, pan, reset, and tap plot tools

# In[6]:


cds_boiler = ColumnDataSource(boiler)
cds_boiler.column_names


# In[7]:


# Create figure for the chart
boiler_chart = figure(height=400, width=600,
                      title="Summarizing NYC Buildings Boiler Data",
                      x_axis_label = 'Years',
                      y_axis_label = 'Number of Buildings',
                      x_axis_type="linear",
                      tooltips='lasso_select,box_select,pan,reset,tap')

# Add line glyph
boiler_chart.line(x='Year', y='NumberOfBuildings', line_width=3,
                  line_color='coral', source=cds_boiler)

# Add circle glyph
boiler_chart.circle(x='Year', y='NumberOfBuildings', size=7,
                    color='gray', alpha=0.6, source=cds_boiler)

# Make sure the y-axis started from zero
boiler_chart.y_range.start=0

# Create and add hover tooltips to our boiler_chart figure
boiler_hover = HoverTool(tooltips=[
    ("Year","@Year"), 
    ("Total Number of Buildings","@NumberOfBuildings")])
boiler_chart.add_tools(boiler_hover)

# Show chart
show(boiler_chart)


# ## 3. BTU Consumptions by Building Area
# - Create two both x and y range linked panning charts using ``btu`` to plot estimated high and low BTU consumption, including linked brushing and two charts must be side by side
# - X axis should be labeled as ‘<strong>Building Area in SF</strong>’ and Y axis should be labeled as ‘<strong>Fuel consumption in BTUs</strong>’. 
# - Chart titles should be ‘<strong>Examining Estimated High BTU Consumption by Building Area</strong>’ and ‘<strong>Examining Estimated Low BTU Consumption by Building Area</strong>’, respectively.
# - Format X and Y axis tick marks as needed including label orientation
# - Add hover tooltips to show 
#     1.	Facility Address
#     2.	Compliance with Greener Buildings Laws
#     3.	Primary Fuel used in the boilers
#     4.	Type of Building
#     5.	Neighborhood (use ``NTA``) 
# - Include <strong>only</strong> following plot tools: lasso select, box select, box zoom, wheel zoom, pan, reset, and tap
# 

# In[8]:


cds_btu = ColumnDataSource(btu)
cds_btu.column_names


# In[14]:


# Create figures for the chart
btu_high = figure(height=400, width=440,
                  title="Examining Estimated High BTU Consumption by Building Area",
                  x_axis_label = 'Building Area in SF',
                  y_axis_label = 'Fuel consumption in BTUs',
                  x_axis_type="linear",
                  tooltips='lasso_select,box_select,box_zoom,wheel_zoom,pan,reset,tap')
btu_low = figure(height=400, width=440,
                 title="Examining Estimated Low BTU Consumption by Building Area",
                 x_axis_label = 'Building Area in SF',
                 y_axis_label = 'Fuel consumption in BTUs',
                 x_axis_type="linear",
                 tooltips='lasso_select,box_select,box_zoom,wheel_zoom,pan,reset,tap',
                 # explicitly specify sharing of ranges to enable linked panning
                 x_range=btu_high.x_range,
                 y_range=btu_high.y_range)

# Add circle glyphs
btu_high.circle(x='BuildingArea', y='HighEstimate', size=2,
                color='coral', alpha=0.6, source=cds_btu)
btu_low.circle(x='BuildingArea', y='LowEstimate', size=2,
                color='green', alpha=0.6, source=cds_btu)

# Make sure the x-axis and y-axis started from zero
btu_high.x_range.start=0
btu_low.x_range.start=0
btu_high.y_range.start=0
btu_low.y_range.start=0

# Create hover tooltips for both figures
btu_hover = HoverTool(tooltips=[
    ("Facility Address","@FacilityAddress"), 
    ("Compliance with Greener Buildings Laws","@GreenBuilding"),
    ("Primary Fuel Used","@PrimaryFuel"),
    ("Type of Building","@BuildingType"),
    ("Neighborhood","@NTA")])

# Add hover to both figures
btu_high.add_tools(btu_hover)
btu_low.add_tools(btu_hover)

# Format numbers on the tickers
btu_high.xaxis.formatter = NumeralTickFormatter(format="1,000")
btu_high.yaxis.formatter = NumeralTickFormatter(format="1,000")
btu_low.xaxis.formatter = NumeralTickFormatter(format="1,000")
btu_low.yaxis.formatter = NumeralTickFormatter(format="1,000")

# Show chart
show(Row(btu_high,btu_low))


# In[ ]:




