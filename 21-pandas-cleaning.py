#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pandas as pd
import numpy as np
os.getcwd()


# In[3]:


os.chdir('D:\\2019 Spring Baruch\\Columbia Engineering\\Python\\JupyterNotebooks')
os.getcwd()


# ## Portland Crime Data Cleaning

# In[ ]:


raw_crime = pd.read_csv('crime_incident_data2017.csv')
raw_crime.head(5)


# In[9]:


raw_crime.count()


# In[11]:


clean_crime = raw_crime.dropna(how = 'any')
clean_crime.count()


# In[15]:


clean_crime['Offense Type'].value_counts()


# In[19]:


#Combine similar crimes into one
clean_crime['Offense Type'] = clean_crime['Offense Type'].replace(
    {'Commercial Sex Acts': 'Prostitution','Assisting or Promoting Prostitution': 'Prostitution'})
clean_crime.describe()


# In[22]:


vernon_crime = clean_crime.loc[clean_crime['Neighborhood']=='Vernon']
vernon_crime.info()


# ## Pandas Recap

# In[24]:


raw_ufo = pd.read_csv('ufoSightings.csv')
raw_ufo.head(5)


# In[25]:


raw_ufo.info()


# In[31]:


clean_ufo = raw_ufo.dropna(how = 'any')
clean_ufo.count()


# In[42]:


#Filter to US data only
us_ufo = clean_ufo.loc[clean_ufo['country']=='us', :]
us_ufo.info()


# In[35]:


state_counts = us_ufo['state'].value_counts()
state_counts


# In[36]:


#Convert state_counts Series into DataFrame
state_counts_df = pd.DataFrame(state_counts)
state_counts_df.head()


# In[38]:


# Convert the column name into "Sum of Sightings"
state_counts_df = state_counts_df.rename(
    columns={"state": "Sum of Sightings"})
state_counts_df.head()


# In[44]:


us_ufo.dtypes


# In[45]:


us_ufo["duration (seconds)"] = pd.to_numeric(
    us_ufo["duration (seconds)"])
us_ufo.dtypes


# In[46]:


us_ufo["duration (seconds)"].sum()


# ## Pokemon Data 

# In[48]:


raw_poke = pd.read_csv('pokemon.csv')
raw_poke.head()


# In[49]:


raw_poke.info()


# In[64]:


pokemon = raw_poke[["Type 1", "Type 2", "HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]]
pokemon.head()


# In[65]:


poke_group = pokemon.groupby(['Type 1', 'Type 2'])
poke_avg = poke_group.mean()
poke_avg


# In[66]:


poke_avg_df = pd.DataFrame(poke_avg)
poke_avg_df


# In[67]:


poke_avg_df['Total'] = poke_avg_df['HP'] + poke_avg_df['Attack'] + poke_avg_df['Defense']                      + poke_avg_df['Sp. Atk'] + poke_avg_df['Sp. Def'] + poke_avg_df['Speed']
poke_avg_df['Total']


# In[69]:


sort_poke = poke_avg_df.sort_values(by = ['Total'], ascending=False)
sort_poke.reset_index(inplace=True)
sort_poke.head()


# In[63]:


sort_poke.to_csv("D:\\2019 Spring Baruch\\Columbia Engineering\\Python\\JupyterNotebooks\\ranked_pokemon.csv", index=False, header=True)


# In[ ]:




