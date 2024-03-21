# -*- coding: utf-8 -*-
"""Labsheet_5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P7ZqW14jPgu5YKneqESRpksMUQokIU4b
"""

import pandas as pd

df = pd.read_csv('/content/train.csv')
df

df.dtypes

df.describe()

df.isna().sum()

age_mean_value=df['Age'].mean()
df['Age']=df['Age'].fillna(age_mean_value)

df.drop("Cabin",axis=1,inplace=True)

df.head()

filtered_age = df[df.Age>40]
filtered_age

# let's sort the column Name in ascending order
sorted_passengers = df.sort_values('Name',ascending=True,kind ='heapsort')

sorted_passengers.head(10)

merged_df = pd.merge(df.head(2),df.tail(2),how='outer',indicator=True)
merged_df

group_df = df.groupby('Name')

group_df