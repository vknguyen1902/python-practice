#!/usr/bin/env python
# coding: utf-8

# In[67]:


import os
import pandas as pd
import numpy as np


# In[68]:


os.chdir('D:\\2019 Spring Baruch\\Columbia Engineering\\Python\\python-challenge\\PyPoll')
os.getcwd()


# In[69]:


raw_poll = pd.read_csv('election_data.csv')
raw_poll.head()


# In[70]:


total_votes = raw_poll['Voter ID'].count()
print(f'Total Votes: {total_votes}')

candidate = raw_poll.groupby(['Candidate'])
print(type(candidate))

count_candidate = candidate['Candidate'].count()
count_candidate = pd.DataFrame(count_candidate)
count_candidate.columns = ['Vote Count']
count_candidate
print(type(count_candidate))

sort_candidate = count_candidate.sort_values(by = ['Vote Count'], ascending=False)
sort_candidate.reset_index(inplace=True)

percent = (sort_candidate['Vote Count']/(sort_candidate['Vote Count'].sum()))*100
sort_candidate['Percentage Vote'] = round(percent,3)
sort_candidate


# In[77]:


print(f'Election Results')
print('-------------------------------')
print(f'Total Votes: {total_votes}')
print('-------------------------------')
for index, row in sort_candidate.iterrows():
    print(f'{row["Candidate"]}: {row["Percentage Vote"]}% ({row["Vote Count"]})')
print('-------------------------------')
print(f'Winner: ')
print('-------------------------------')


# In[75]:





# In[ ]:




