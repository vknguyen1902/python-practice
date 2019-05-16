import pandas as pd

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool, TextInput
from bokeh.layouts import Column
from bokeh.plotting import gmap

def updateMap(attr, old, new):
    print(old, new)
    
    dfNew = dfFire[dfFire.Postcode == int(zipcode.value)]
    
    cdsFire.data = dict(
                        lat=dfNew['Latitude'],
                        long=dfNew['Longitude'],
                        name=dfNew['FacilityName'],
                        addr=dfNew['FacilityAddress'])
    myMapOpt.zoom = 14
    myMapOpt.lat = dfCode.loc[int(zipcode.value), "LAT"]
    myMapOpt.lng = dfCode.loc[int(zipcode.value), "LNG"]
    

myMapOpt = GMapOptions(lat=40.730610, lng=-73.935242, map_type='roadmap', zoom=11)

myMap = gmap("AIzaSyAD0M7aeSE_Rn01x6W5BTsy8hO45s7VDoI", myMapOpt, title="NY Fire Dept Locations")

dfFire = pd.read_excel('data/FDNY_Locations.xlsx')
dfZip = pd.read_excel('data/ZipcodeLatLong.xlsx')

dfCode = dfZip.set_index(keys="ZIP", drop=False)

cdsFire = ColumnDataSource(data=dict(lat=dfFire['Latitude'],
                                     long=dfFire['Longitude'],
                                     name=dfFire['FacilityName'],
                                     addr=dfFire['FacilityAddress'])
        )


zipcode = TextInput(title="Enter 5 digit zipcode",
                    width=100,
                    value="10010")

myMap.circle(x='long', y='lat', source=cdsFire, size=10)

mapHover = HoverTool(tooltips=[("Name","@name"),
                               ("Address", "@addr")])

myMap.add_tools(mapHover)


zipcode.on_change('value', updateMap)
curdoc().add_root(Column(zipcode, myMap))