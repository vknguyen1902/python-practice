import pandas as pd

from bokeh.plotting import figure
from bokeh.io import curdoc, output_file, show
from bokeh.models import ColumnDataSource, Select, Slider, CheckboxGroup
from bokeh.layouts import Row, Column

# Event handler function for SCATTER PLOT
def updateScatter(attr, old, new):
    print(old, new) # Just for debugging purposes
    
    # etting the labels for those active checkboxes
    optionsSelected = [bodyCheck.labels[i] for i in bodyCheck.active]
    
    # Slicing the dataframe to make sure only cars whose curb weights are 
    # above or equal to the slider value. 
    dfNew = dfAuto[dfAuto.Curb_Weight >= weightSlider.value]
    dfCheck = dfNew[dfNew.Body_Style.isin(optionsSelected)]
    
    #update CDS to reflect updated DF
    cdsAuto.data= dict(
            xVal=dfCheck[xSelect.value],
            yVal=dfCheck['City_MPG'])
    
    # update the axes label
    scatChart.xaxis.axis_label=xSelect.value


# Event handler function for BAR chart    
def updateBar(attr,old, new):
    print(old,new) # Just for debugginf purposes
    
    # Updating label of axes
    barChart.xaxis.axis_label=barSelect.value
    
    # Updating data source to reflect user's selection values for bar chart
    dfNew = dfAuto.groupby([barSelect.value])['City_MPG'].mean().reset_index()
    
    # Unique step specific to bar charts to update their range factors
    barChart.x_range.factors = list(dfNew[barSelect.value])
    
    #Update CDS
    cdsMean.data = dict(xVal=dfNew[barSelect.value],
                        yVal=dfNew['City_MPG'])

# Getting the dataset ready for use in the charts
dfAuto = pd.read_excel('Auto_Insu.xlsx')

# Preparing CDS object with only the columns that we need
cdsAuto = ColumnDataSource(data=dict(
         xVal = dfAuto['HP'],
         yVal = dfAuto['City_MPG']))

# Adding SELECT widget to allow selection of variables to be displayed on X-axis
xSelect = Select(title="Select the X variable from the list",
                 options=['HP','Length','Width'],
                 value='HP')

# Adding SLIDER widget to allow user to filter cars based on the curb_weight
weightSlider = Slider(title="Select weight threshold",
                      start=dfAuto['Curb_Weight'].min(),
                      end=dfAuto['Curb_Weight'].max(),
                      value=dfAuto['Curb_Weight'].min(),
                      step=100)

# Adding Checkbox widget for use with the scatter plot
bodyCheck = CheckboxGroup(labels=list(dfAuto['Body_Style'].unique()),
                          active=[])

#Adding SELECT widget for bar chart X-axis variable selection
barSelect = Select(title="Select Categorical variable to summarize",
                   options=['Fuel_Type','Body_Style', 'Engine_Type', 'Fuel_System'],
                   value='Engine_Type')

# Creating figure objects for scatter plot
scatChart = figure(height=500, width=500,
                   title="Using Widgets",
                   x_axis_label="HP",
                   y_axis_label="City MPG")

# Adding the square glyph to the scatterplot
scatChart.square(x='xVal', y='yVal',source=cdsAuto)

# Getting dataset ready for viewing mean MPG values by Body_style.
# reset_index() converts the groupby object back to the dataframe.
meanCity = dfAuto.groupby(['Body_Style'])['City_MPG'].mean().reset_index()

# Preparing CDS object ready to populate the bar chart
cdsMean = ColumnDataSource(data=dict(xVal = meanCity['Body_Style'],
                                      yVal = meanCity['City_MPG']))

# Bar chart and its vbar glyph
# Again remember that for bar charts, you need to specify x_range when you create 
# the figure. List passed here should be unique values of type 'string'.
barChart = figure(height=400, width=700,
                  title="Summarizing City_MPG mean values",
                  x_range=meanCity['Body_Style'].unique())

barChart.vbar(x='xVal', top='yVal', source=cdsMean, width=.3)

# Capturing the event of change of value
xSelect.on_change('value', updateScatter)
barSelect.on_change('value', updateBar)
weightSlider.on_change('value', updateScatter)
bodyCheck.on_change('active', updateScatter)
# Equivalent of show()... Curdoc() allows your charts to be rendered with server.
curdoc().add_root(Row(Column(xSelect, weightSlider, bodyCheck, scatChart), 
                      Column(barSelect, barChart)))
