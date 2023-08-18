#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


emp_df = pd.read_csv("employees.csv")
emp_df.head()


# In[49]:


ts_df = pd.read_csv("timesheets.csv")
ts_df.head()


# In[50]:


ts_df['checkin'] = pd.to_datetime(ts_df['checkin'].fillna('09:00:00'))
ts_df['checkout'] = pd.to_datetime(ts_df['checkout'].fillna('17:00:00'))
ts_df['date'] = pd.to_datetime(ts_df['checkout'])


# In[51]:


ts_df['hours_difference'] = (ts_df['checkout'] - ts_df['checkin']).dt.total_seconds() / (60*60)


# In[52]:


merged_df = pd.merge(ts_df, emp_df, left_on='employee_id', right_on='employe_id', how='left')


# In[32]:


df_salary = merged_df.copy()
df_salary = df_salary[["timesheet_id","employee_id","date","salary"]]


# In[53]:


merged_df["year"] = merged_df['date'].dt.year
merged_df["month"] = merged_df['date'].dt.month


# In[54]:


merged_df


# In[59]:


z = merged_df.groupby(['year', 'month', 'branch_id'])


# In[64]:


z.head()


# In[65]:


f = {
        'employee_id' : 'nunique'
}
v1 = z.agg(f)
v2 = z.agg(lambda x: x.drop_duplicates('employee_id', keep='first').salary.sum())


# In[66]:


v2

