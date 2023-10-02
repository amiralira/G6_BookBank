import pandas as pd
from scipy import stats
import numpy as np

df_books = pd.read_csv('price.csv')
df_translated = pd.read_csv('translator.csv')
df = pd.read_csv('books.csv')

#books that are translated
merged_df = pd.merge(df_books, df_translated, on ='BookID')

#books that are not translated
filtered_df = df_books[~df_books['BookID'].isin(df_translated['BookID'])]

#ttest for hypothesis 1 :
translated_books = merged_df['Price']
non_translated_books = filtered_df['Price']
t1 = stats.ttest_ind(translated_books, non_translated_books)

df['CoverType'] = df['CoverType'].apply(str)
df['Title'] = df['Title'].apply(str)
df_hard = df[df['CoverType'].str.contains('جلد سخت')]
df_soft = df[df['CoverType'].str.contains('شومیز')]
df_h = df_hard.rename(columns = {'ID' : 'BookID', 'Title' : 'hard'})
df_s = df_soft.rename(columns = {'ID' : 'BookID', 'Title' : 'soft'})

merged_h = pd.merge(df_books, df_h, on ='BookID')
merged_s = pd.merge(df_books, df_s, on ='BookID')
merged_hard = merged_h[merged_h['Title'].isin(merged_s['Title'])]
merged_soft = merged_s[merged_s['Title'].isin(merged_h['Title'])]

#ttest for hypothesis 2 :
hard_price = merged_hard['Price']
soft_price = merged_soft['Price']
t2 = stats.ttest_ind(hard_price, soft_price)

