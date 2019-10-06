#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

# 
# assign the path of the code-for-nashville open data portal on githup to a variable
# 
dataPath = 'https://raw.githubusercontent.com/code-for-nashville/open-data-portal/feature/scooter-2019-08-clean-up/nashville/scooter-data/'
# dataPath = 'https://raw.githubusercontent.com/code-for-nashville/open-data-portal/feature/scooter-extract/nashville/scooter-data/'

# 
# Make a list of all the files to download from the open data portal
# currently files for July 22 through Sept 9 are available
# 
fileNames = ['scooter_extract_2019-07-'+str(x)+'.csv' for x in range(22,32)]
fileNames = fileNames + ['scooter_extract_2019-08-0'+str(x)+'.csv' for x in range(1,6)]
# fileNames = ['scooter_extract_2019-07-20_to_2019-09-09.csv']


# 
# make a list of the columns for the facts table
# 
factColumns = ['availability_duration', 'availability_duration_seconds',
       'availability_start_date', 'availability_start_date_cst',
       'availability_start_time', 'availability_start_time_cst',
       'company_name', 'extract_date_cst',
       'extract_date_utc', 'extract_time_cst', 'extract_time_utc',
       'gps_latitude', 'gps_longitude', 'real_time_fare',
       'sumd_id']

# 
# make a list of the columns for the company dimension table and sumd dimension table
# 
companyColumns = ['company_name', 'company_phone', 'company_website']
sumdColumns = ['company_name', 'sumd_group', 'sumd_id', 'sumd_type']


# In[2]:


get_ipython().run_cell_magic('time', '', '# \n# load all the data files into a single dataframe\n# this take approximately 8 minutes to load this file\n# \nrawData = pd.concat([pd.read_csv(dataPath+f) for f in fileNames], sort = False)')


# In[3]:


get_ipython().run_cell_magic('time', '', "# \n# create fact and dimension tables\n# \nrawData['company_name'] = [x.upper() for x in rawData['company_name']]\nrawData['sumd_group'] = [x.upper() for x in rawData['sumd_group']]\ncompany = rawData[companyColumns].drop_duplicates()\nsumd = rawData[sumdColumns].drop_duplicates()\nsumd = sumd[sumd['sumd_group']=='SCOOTER']\nscooterFacts = rawData[rawData['sumd_group']=='SCOOTER']\nscooterFacts = scooterFacts[factColumns]")


# In[4]:


# 
# Create two new columns with the latitude and longitdue rounded to 3 places
# Using this rounded location, will allow for scooters within about 350 ft of each other
# to appear in the same location, thus minimizing the number of unique locations.
# 
scooterFacts['latitude_rnd'] = round(scooterFacts['gps_latitude'], 3)
scooterFacts['longitude_rnd'] = round(scooterFacts['gps_longitude'], 3)


# In[5]:


# 
# How many scooters does each company have in Nashville?
# 
companyStats = sumd[['company_name', 'sumd_id']]                 .groupby('company_name').count()                 .reset_index()                 .rename(columns={'company_name': 'Company', 'sumd_id': 'Number Of Scooters'})

companyStats


# In[6]:


# 
# What are the 25 most popular scooters?
# The table below shows the 25 scooters that were reported in the most locations in a day.
# the numbers under the 'latitude_rnd' and 'longitude_rnd' columns represent the average number
# of locations on each day in the dataset.
# 
numOfLocsPerDay = scooterFacts[['availability_start_date_cst', 'latitude_rnd', 'longitude_rnd', 'sumd_id']]                     .drop_duplicates()                     .groupby(['sumd_id', 'availability_start_date_cst']).count() - 1

avgLocsPerDay = numOfLocsPerDay.groupby('sumd_id').mean()

totLocs = numOfLocsPerDay.groupby('sumd_id').sum()

twtyfiveMostMovedScooters = avgLocsPerDay                             .sort_values(by='latitude_rnd', ascending = False)                             .head(25)                             .merge(sumd[['company_name', 'sumd_id']], on='sumd_id')
twtyfiveMostMovedScooters


# In[7]:


companyStats = companyStats.merge(                                   totLocs[totLocs['latitude_rnd'] == 0]                                     .merge(sumd[['company_name', 'sumd_id']], on='sumd_id')                                     .groupby('company_name')                                     .count()                                     .reset_index()[['company_name', 'sumd_id']]                                     .rename(columns={'company_name': 'Company', 'sumd_id': 'Scooters Not Ridden'})                                     ,on='Company')


# In[8]:


companyStats['Active Scooters'] = companyStats['Number Of Scooters'] - companyStats['Scooters Not Ridden']


# In[9]:


companyStats


# In[10]:


# 
# Calculate the total number of rides per company
# over all of the days in the dataset (15 days)
# 
companyStats = totLocs                 .merge(sumd[['company_name', 'sumd_id']], on='sumd_id')                 .groupby('company_name')                 .sum()                 .reset_index()[['company_name', 'latitude_rnd']]                 .rename(columns={'company_name': 'Company', 'latitude_rnd': 'Total Rides'})                 .merge(companyStats, on='Company')                 .sort_values(by=['Total Rides'], ascending = False)

companyStats = companyStats                 .append(pd.Series(['TOTAL'], index=['Company']).append(companyStats.sum(numeric_only = True)),                         ignore_index = True)

companyStats['Avg Rides Per Scooter'] = companyStats['Total Rides'] / companyStats['Active Scooters']


# In[11]:


columnFormats = {'Total Rides': '{:,d}',
                 'Number Of Scooters': '{:,d}',
                 'Scooters Not Ridden': '{:,d}',
                 'Active Scooters': '{:,d}',
                 'Avg Rides Per Scooter': '{:.2f}'}

companyStats.style.format(columnFormats)


# In[ ]:




