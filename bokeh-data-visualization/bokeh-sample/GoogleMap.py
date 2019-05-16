from bokeh.plotting import gmap, figure
from bokeh.layouts import column
from bokeh.io import show,curdoc
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, TextInput

import pandas as pd

# Event handler fucntion for GMAP chart
def updateMap(attr, old, new):
    print(zipcode.value) # Just for debugging
    
    # Slicing the dataset to include only those FDNY locations that match the user-entered zipcode
    dfNew = fdLoc[fdLoc.Postcode == int(zipcode.value)] 
    
    # Updating CDS with the new DF
    cdsFDLoc.data = dict(
             mapLat=dfNew['Latitude'],
             mapLng=dfNew['Longitude'],
             mapName=dfNew['FacilityName'],
             mapAddr=dfNew['FacilityAddress'],
             mapZip=dfNew['Postcode'])    
    
    # Following code allows you to zoom in to that particular zipcode
    # by updating properties of GMAPOptions object
    map_opt.zoom = 14
    map_opt.lat = zipCoord.loc[int(zipcode.value),"LAT"]
    map_opt.lng = zipCoord.loc[int(zipcode.value),"LNG"]


# Getting the data ready for the use in the chart
fdLoc = pd.read_excel('data/FDNY_Locations.xlsx')
df1 = pd.read_excel('data/ZipcodeLatLong.xlsx')

# Setting zipcode column to serve as an index for easy searching when used in Event handler function
# drop False will ensure ZIP colum still remains as a regular columns 
# even after it becomes an index 
zipCoord = df1.set_index("ZIP", drop = False)

# Creating CDS object with only those columns we need
cdsFDLoc = ColumnDataSource(data=dict(
        mapLat=fdLoc['Latitude'],
        mapLng=fdLoc['Longitude'],
        mapName=fdLoc['FacilityName'],
        mapAddr=fdLoc['FacilityAddress'],
        mapZip=fdLoc['Postcode']
        ))

# Creating the google map options. Make sure you have imported it
map_opt = GMapOptions(lat=40.730610, lng=-73.935242, map_type="roadmap", zoom=11)

# creating gmap object. Make sure you have imported it 
# first part is Google API Key. I will keep this key active for one week so that you can practice bokeh
# charts for class purposed. After one week, I will be deactivating this key. 
# Please remember to not use this key for purposes other than the class work.
myMap = gmap("AIzaSyAD0M7aeSE_Rn01x6W5BTsy8hO45s7VDoI", map_opt, title="NYC")
myMap.width=800
myMap.height=600

# Adding the TEXTINPUT widget to allow user to enter zipcode value
zipcode = TextInput(value="", title="Enter 5 digit Zipcode...", width=100)

# Adding circle glyph with lat lng values of FDNY locations. 
myMap.circle(y='mapLat', x='mapLng', source=cdsFDLoc, size=10)

# Adding the hover tool with name and address of FDNY location
mapHover = HoverTool(tooltips=[("Name","@mapName"),("Addr","@mapAddr")])
myMap.add_tools(mapHover)

# Capturing the event change for TEXTINPUT widget
zipcode.on_change('value', updateMap)

# Adding chart and widgets to Curdoc's root so that they are rendered in the browser
curdoc().add_root(column(zipcode, myMap))

