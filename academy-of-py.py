#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
# 
# ## Table of Content
# 0. Data Preparation
# 1. District Summary
# 2. School Summary
# 3. Top Performing Schools by Passing Rate
# 4. Bottom Performing Schools by Passing Rate
# 5. Math Scores by Grade Levels
# 6. Reading Score by Grade
# 7. Scores by School Spending
# 8. Scores by School Size
# 9. Scores by School Type

# ## 0. Data Preparation

# In[62]:


#Import packages
import pandas as pd
import numpy as np
import os
import re
os.chdir('D:\\2019 Spring Baruch\\Columbia Engineering\\Homework\\Week 4 HWK Pandas')


# In[63]:


#Load data
school = pd.read_csv('schools_complete.csv')
student = pd.read_csv('students_complete.csv')

#Combine data
complete = pd.merge(student, school, how='left', on=['school_name','school_name'])
complete.head()


# ## 1. District Summary

# In[64]:


#Creat dictionary for district summary
district_summary = {}

#Total number of schools
num_school = complete['school_name'].nunique()
district_summary['Total Schools'] = num_school

#Total number of students
num_student = complete['Student ID'].count()
district_summary['Total Students'] = num_student

#Total Budget
total_budget = complete['budget'].unique().sum()
district_summary['Total Budget'] = total_budget


# In[65]:


#Average math score
avg_math = round(complete['math_score'].mean(),6)
district_summary['Average Math Score'] = avg_math

#Average reading score
avg_reading = round(complete['reading_score'].mean(),6)
district_summary['Average Reading Score'] = avg_reading


# In[66]:


#Percentage passing math
pass_math = (complete.loc[complete['math_score']>=70])['Student ID'].count()
percent_math = round((pass_math / num_student) * 100,6)
district_summary['% Passing Math'] = percent_math

#Percentage passing reading
pass_reading = (complete.loc[complete['reading_score']>=70])['Student ID'].count()
percent_reading = round((pass_reading / num_student) * 100,6)
district_summary['% Passing Reading'] = percent_reading

#Overall passing rate
passing_rate = (avg_math + avg_reading) / 2
district_summary['% Overall Passing Rate'] = passing_rate


# In[67]:


#View the dictionary output
district_summary


# In[68]:


#Convert dictionary to dataframe
district_df = pd.DataFrame(district_summary, index=[0])
district_df['Total Budget'] = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % district_df['Total Budget'])
district_df['Total Students'] = re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1,", "%d" % district_df['Total Students'])
district_style = district_df.style.hide_index()
district_style


# In[69]:


#Give a cleaner formatting
district_clean = district_df.transpose()
district_clean.rename(columns={0:' '}, inplace=True)

print('DISTRICT SUMMARY')
print(district_clean.round(2))


# ## 2. School Summary

# In[70]:


#Summarize school names and types 
get_school = complete.groupby(['school_name','type'])

#Summarize number of students
school_student = get_school['Student ID'].count()
school_student = pd.DataFrame(school_student)
school_student.rename(columns={'Student ID':'Total Students'}, inplace=True)

#School budgets
school_budget = get_school['budget'].sum()
school_student['Total Budget'] = school_budget

#Budget per student
per_student = school_student['Total Budget'] / school_student['Total Students']
school_student['Budget Per Student'] = per_student

#Average math score
school_math = get_school['math_score'].mean()
school_student['Average Math Score'] = school_math

#Average reading score
school_reading = get_school['reading_score'].mean()
school_student['Average Reading Score'] = school_reading


# In[71]:


#Filter all students who passed math
pass_math_df = (complete.loc[complete['math_score']>=70])[['Student ID','school_name','type']]
school_pass_math = pass_math_df.groupby(['school_name','type'])

#Find number of students who passed math for each school
num_pass_math = school_pass_math['Student ID'].count()
school_student['# of Students Passing Math'] = num_pass_math

#Percentage passing math for each school
school_percent_pass_math = (school_student['# of Students Passing Math']/school_student['Total Students'])*100
school_student['% Passing Math'] = school_percent_pass_math

#Filter all students who passed reading
pass_reading_df = (complete.loc[complete['reading_score']>=70])[['Student ID','school_name','type']]
school_pass_reading = pass_reading_df.groupby(['school_name','type'])

#Find number of students who passed math for each school
num_pass_reading = school_pass_reading['Student ID'].count()
school_student['# of Students Passing Reading'] = num_pass_reading

#Percentage passing math for each school
school_percent_pass_reading = (school_student['# of Students Passing Reading']/school_student['Total Students'])*100
school_student['% Passing Reading'] = school_percent_pass_reading


# In[72]:


#Overall Passing Rate
school_overall = (school_student['% Passing Reading'] + school_student['% Passing Math'])/2
school_student['Overall Passing Rate'] = school_overall

#Remove the extra columns
del school_student['# of Students Passing Math']
del school_student['# of Students Passing Reading']


# In[73]:


#School Summary
school_student


# ## 3. Top Performing Schools by Passing Rate

# In[74]:


top_schools = school_student.sort_values(by=['Overall Passing Rate'], ascending=False)
top_schools.head(5)


# ## 4. Bottom Performing Schools by Passing Rate

# In[75]:


bottom_schools = school_student.sort_values(by=['Overall Passing Rate'], ascending=True)
bottom_schools.head(5)


# ## 5. Math Scores by Grade Levels

# In[77]:


get_grade = complete.groupby(['grade'])
student_grade = get_grade['Student ID'].count()
student_grade = pd.DataFrame(student_grade)
student_grade.rename(columns={'Student ID':'# of Students'}, inplace=True)
student_grade


# In[ ]:




