#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")


# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


df = pd.read_csv("311_Service_Requests_from_2010_to_Present.csv")


# In[4]:


df.head()


# In[5]:


df.shape


# In[6]:


df.info()


# In[7]:


colsToDrop = ["Ferry Terminal Name","Ferry Direction",
"Garage Lot Name", "Bridge Highway Segment",
"Road Ramp", "Bridge Highway Direction",
"Bridge Highway Name", "Taxi Pick Up Location",
"Taxi Company Borough", "Vehicle Type",
"School or Citywide Complaint", "Landmark",
"Intersection Street 2", "Intersection Street 1"]
df.drop(colsToDrop,axis=1,inplace=True)


# In[8]:


df.shape


# In[9]:


df.drop(["Unique Key"], axis=1, inplace=True)


# In[10]:


df.shape


# In[12]:


df["Created Date"] = pd.to_datetime(df["Created Date"])


# In[13]:


df["Closed Date"] = pd.to_datetime(df["Closed Date"])


# In[14]:


df.head(2)


# In[15]:


df["Request_Closing_Time"] = df["Closed Date"] - df["Created Date"]


# In[16]:


df[["Closed Date","Created Date","Request_Closing_Time"]].head(5)


# In[17]:


df["Request_Closing_Time"] = df["Request_Closing_Time"].dt.total_seconds()


# In[18]:


df[["Closed Date","Created Date","Request_Closing_Time"]].head(5)


# In[19]:


df.head(2)


# In[20]:


df.drop(["Location"],axis=1,inplace=True)


# In[21]:


df.replace('Unspecified',np.nan,inplace=True)


# In[22]:


df.head(2)


# In[23]:


df.isna().sum()/len(df.index) * 100


# In[24]:


colsToDrop = ["Park Facility Name","School Name",
"School Number","School Region",
"School Code", "School Phone Number",
"School Address", "School City",
"School State", "School Zip"]
df.drop(colsToDrop,axis=1,inplace=True)


# In[25]:


df.shape


# In[26]:


df.head(2)


# In[27]:


df.Agency.unique()


# In[28]:


df.drop(["Agency"],axis=1,inplace=True)


# In[29]:


df.head(2)


# In[30]:


df["Agency Name"].unique()


# In[31]:


df["School Not Found"].unique()


# In[32]:


df.drop(["School Not Found"],axis=1,inplace=True)


# In[33]:


df.head(2)


# In[34]:


sns.countplot(df["Agency Name"])
plt.show()


# In[35]:


df["Agency Name"].value_counts()


# In[36]:


sns.countplot(df["Complaint Type"])
plt.xticks(rotation=90)
plt.show()


# In[37]:


sns.countplot(df["Location Type"])
plt.xticks(rotation=90)
plt.show()


# In[38]:


df["Longitude"].isnull().sum()


# In[39]:


df["Latitude"].isnull().sum()


# In[40]:


df = df[df["Longitude"].isnull() == False]


# In[41]:


df = df[df["Latitude"].isnull() == False]


# In[42]:


df.shape


# In[43]:


df.plot(kind = 'scatter', x = 'Longitude', y = 'Latitude')
plt.show()


# In[44]:


ctcounts = df['Complaint Type'].value_counts()


# In[45]:


ctcounts.head()


# In[46]:


for ctype, count in ctcounts[:10].iteritems():
tmp = df[df['Complaint Type'] == ctype]
tmp.plot(kind='scatter', x='Longitude', y='Latitude', subplots=True,label=ctype, marker=".")


# In[47]:


df.head(2)


# In[48]:


ct_bor_req = df.groupby(["Borough","Complaint Type"]).mean()["Request_Closing_Time"].to_frame()


# In[49]:


ct_bor_req.sort_values('Request_Closing_Time',ascending=False)


# In[50]:


import scipy.stats as stats


# In[51]:


df['Complaint Type'].value_counts()


# In[52]:


top5_complaints_type = df['Complaint Type'].value_counts()[:5]
top5_complaints_type


# In[53]:


top5_complaints_type_names = top5_complaints_type.index
top5_complaints_type_names


# In[54]:


sample_data = df.loc[df['Complaint Type'].isin(top5_complaints_type_names),['Complaint Type', 'Request_Closing_Time']]
sample_data.head()


# In[55]:


sample_data.isnull().sum()


# In[56]:


sample_data.dropna(how='any', inplace=True)
sample_data.isnull().sum()


# In[57]:


s1 = sample_data[sample_data['Complaint Type'] == top5_complaints_type_names[0]].Request_Closing_Time
s1.head()


# In[58]:


s2 = sample_data[sample_data['Complaint Type'] == top5_complaints_type_names[1]].Request_Closing_Time
s2.head()


# In[59]:


s3 = sample_data[sample_data['Complaint Type'] == top5_complaints_type_names[2]].Request_Closing_Time
s3.head()


# In[60]:


s4 = sample_data[sample_data['Complaint Type'] == top5_complaints_type_names[3]].Request_Closing_Time
s4.head()


# In[61]:


s5 = sample_data[sample_data['Complaint Type'] == top5_complaints_type_names[4]].Request_Closing_Time
s5.head()


# In[62]:


stats.f_oneway(s1, s2, s3, s4, s5)


# In[63]:


top5_location = df['City'].value_counts()[:5]
top5_location


# In[64]:


top5_location_names = top5_location.index
top5_location_names


# In[65]:


sample_data_location_c_type = df.loc[(df['Complaint Type'].isin(top5_complaints_type_names)) & (df['City'].isin(top5_location_names)),['Complaint Type', 'City']]
sample_data_location_c_type.head()


# In[66]:


pd.crosstab(sample_data_location_c_type['Complaint Type'],sample_data_location_c_type['City'], margins=True)


# In[67]:


ch2, p_value, df, exp_frq = stats.chi2_contingency(pd.crosstab(sample_data_location_c_type['Complaint Type'],sample_data_location_c_type['City']))


# In[68]:


print(ch2)
print(p_value)


# In[ ]:




