# -*- coding: utf-8 -*-
"""Labsheet_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1I5B6KluPWEg2JBZCvFe6PtggzTSqsfaz
"""

import pandas as pd
import numpy as np
from functools import reduce

df = pd.read_csv('/content/BL-Flickr-Images-Book (2).csv')
df.head()

to_drop = ['Edition Statement',
           'Corporate Author',
           'Corporate Contributors',
           'Former owner',
           'Engraver',
           'Contributors',
           'Issuance type',
           'Shelfmarks']

df.drop(to_drop, inplace = True, axis = 1)
df.head()

df.set_index('Identifier', inplace = True)
df.head()

df['Date of Publication'].head(25)

unwanted_characters = ['[', ',', '-']

def clean_dates(item):
    dop= str(item.loc['Date of Publication'])

    if dop == 'nan' or dop[0] == '[':
        return np.NaN

    for character in unwanted_characters:
        if character in dop:
            character_index = dop.find(character)
            dop = dop[:character_index]

    return dop

df['Date of Publication'] = df.apply(clean_dates, axis = 1)

df.head()

#alternate way of cleaning Date of Publication
#run cell to see output
unwanted_characters = ['[', ',', '-']

def clean_dates(dop):
    dop = str(dop)
    if dop.startswith('[') or dop == 'nan':
        return 'NaN'
    for character in unwanted_characters:
        if character in dop:
            character_index = dop.find(character)
            dop = dop[:character_index]
    return dop

df['Date of Publication'] = df['Date of Publication'].apply(clean_dates)
df.head()

def clean_author_names(author):

    author = str(author)

    if author == 'nan':
        return 'NaN'

    author = author.split(',')

    if len(author) == 1:
        name = filter(lambda x: x.isalpha(), author[0])
        return reduce(lambda x, y: x + y, name)

    last_name, first_name = author[0], author[1]

    first_name = first_name[:first_name.find('-')] if '-' in first_name else first_name

    if first_name.endswith(('.', '.|')):
        parts = first_name.split('.')

        if len(parts) > 1:
            first_occurence = first_name.find('.')
            final_occurence = first_name.find('.', first_occurence + 1)
            first_name = first_name[:final_occurence]
        else:
            first_name = first_name[:first_name.find('.')]

    last_name = last_name.capitalize()

    return f'{first_name} {last_name}'


df['Author'] = df['Author'].apply(clean_author_names)

def clean_title(title):

    if title == 'nan':
        return 'NaN'
    if 'by' in title:
        title = title[:title.find('by')]
    elif 'By' in title:
        title = title[:title.find('By')]

    if '[' in title:
        title = title[:title.find('[')]

    title = title[:-2]

    title = list(map(str.capitalize, title.split()))
    return ' '.join(title)

df['Title'] = df['Title'].apply(clean_title)
df.head()

#4157862 and 4159587
df.loc[4159587]

pub = df['Place of Publication']
df['Place of Publication'] = np.where(pub.str.contains('London'), 'London',
    np.where(pub.str.contains('Oxford'), 'Oxford',
        np.where(pub.eq('Newcastle upon Tyne'),
            'Newcastle-upon-Tyne', df['Place of Publication'])))