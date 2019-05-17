from bokeh.plotting import figure
from bokeh.io import curdoc, output_file, show, output_notebook
from bokeh.models import ColumnDataSource, Select, Slider, CheckboxGroup, GMapOptions, HoverTool, TextInput, WheelZoomTool, NumeralTickFormatter, CategoricalColorMapper
from bokeh.layouts import Row, Column
from bokeh.plotting import gmap
from bokeh.palettes import Category20c
from bokeh.transform import factor_cmap
import pandas as pd

df = pd.read_excel('NYCOilConsumption-2018.xlsx')
print(df.dtypes)

def updateMap(attr, old, new):
    print(old, new)
    dfNew = df[df['ComplianceDate'] == compDtSlider.value]
    dfSelect = dfNew[dfNew['BuildingType'] == btypeSelect.value]
    cds.data = dict(comply = dfSelect['ComplyWithGreenerBuildingsLaws'],
                     lat = dfSelect['Latitude'],
                     long = dfSelect['Longitude'],
                     gas=dfSelect['NaturalGasUtilityCompany'],
                     installDt=dfSelect['BoilerInstallationDate'],
                     retireDt=dfSelect['BoilerRetirement_dateEstimated'],
                     dualFuel=dfSelect['DuelFuelBoiler?'],
                     units=dfSelect['NumberOfTotalUnits'],
                     constructedDt=dfSelect['YearConstructed'],
                     compDt=dfSelect['ComplianceDate'],
                     fuel=dfSelect['PrimaryFuel'])

dfbtype = df[(df['BuildingType'] == 'Walk-Up Apartments') & (df['ComplianceDate'] == 2013)]

cds = ColumnDataSource(data=dict(comply = dfbtype['ComplyWithGreenerBuildingsLaws'],
                                 lat = dfbtype['Latitude'],
                                 long = dfbtype['Longitude'],
                                 gas=dfbtype['NaturalGasUtilityCompany'],
                                 installDt=dfbtype['BoilerInstallationDate'],
                                 retireDt=dfbtype['BoilerRetirement_dateEstimated'],
                                 dualFuel=dfbtype['DuelFuelBoiler?'],
                                 units=dfbtype['NumberOfTotalUnits'],
                                 constructedDt=dfbtype['YearConstructed'],
                                 compDt=dfbtype['ComplianceDate'],
                                 fuel=dfbtype['PrimaryFuel']))

mapOpt = GMapOptions(lat=40.730610, lng=-73.935242, map_type='roadmap', zoom=11)
mymap = gmap("AIzaSyAD0M7aeSE_Rn01x6W5BTsy8hO45s7VDoI", mapOpt, title="Compliant NYC Buildings",
             tools=['hover', 'pan', 'reset'])

mapper = CategoricalColorMapper(palette=["red", "green"], factors=["6 (Dirty Oil)", "4 (Clean Oil)"])

mymap.circle(x='long',y='lat', source=cds, size=10, color={'field': 'fuel', 'transform': mapper})

compDtSlider = Slider(title='Compliance Date',
                      start=df['ComplianceDate'].min(),
                      end=df['ComplianceDate'].max(),
                      value=df['ComplianceDate'].min(),
                      step=1)

compDtSlider.on_change('value', updateMap)

btypeSelect = Select(title='Select a building type',
                     options=list(sorted(df['BuildingType'].unique())),
                     value='Walk-Up Apartments')

btypeSelect.on_change('value', updateMap)

mapHover = HoverTool(tooltips=[('Natural Gas Utility Company', '@gas'),
                               ('Boiler Installation Date', '@installDt'),
                               ('Boiler Retirement Date', '@retireDt'),
                               ('Is Duel Fuel', '@dualFuel'),
                               ('# of total units', '@units'),
                                ('Year Constructed', '@constructedDt'),
                                ('Compliance Date', '@compDt')])

mymap.add_tools(mapHover)

curdoc().add_root(Row(Column(compDtSlider, btypeSelect), mymap))