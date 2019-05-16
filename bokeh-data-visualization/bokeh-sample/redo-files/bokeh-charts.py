
# coding: utf-8

# In[1]:


from bokeh.plotting import figure
from bokeh.io import output_notebook, show
from bokeh.models import ColumnDataSource
import pandas as pd 


# In[2]:


output_notebook()


# In[3]:


#Create figure object
p = figure(height=500, width=500,
           title="My first bokeh chart",
           x_axis_label="x-axis label",
           y_axis_label="y-axis label")


# In[4]:


#Add a glyph (circle, square, line, bar)
x_axis = [1.5,3,4,5,6]
y_axis = [4,8,10,11,12]
p.circle(x=x_axis, y=y_axis, 
         color=['forestgreen','coral','skyblue','red','violet'], 
         size=10, alpha=0.5)
p.line(x=x_axis, y=y_axis, color = 'peru', line_width=2)

#Force the graph to start at 0 on x-axis and y-axis
p.x_range.start = 0
p.y_range.end = 13
p.y_range.start = 0


# In[5]:


show(p)


# In[6]:


#Categorical data graphing
fruits = ['banana','apple','avacado','mango','cherry']
consume = [45,17,60,20,24]
fruit_color = ['yellow','red','forestgreen','orange','tomato']


# In[7]:


from bokeh.models import HoverTool


# In[8]:


b = figure(height=500, width=500,
           x_range = fruits, title = "My favorite fruits",
           tools = 'pan,reset') #control the tools viewers can see 


# In[9]:


#Vertical bar
b.vbar(x = fruits, top = consume, width = 0.4, color = fruit_color)


# In[10]:


show(b)


# # Visualize a Data Set with Bokeh

# In[11]:


df_import = pd.read_excel('Auto_Insu.xlsx')
df_import.info()


# In[12]:


#Convert dataframe to column data source
auto_cds = ColumnDataSource(df_import)


# In[13]:


cds_plot = figure(height=400, width=400,
                  title = 'Column Data Source')


# In[14]:


cds_plot.circle(x='Wheel-Base', y='Engine-Size', source = auto_cds, size=10, alpha=0.5)


# In[15]:


show(cds_plot)

