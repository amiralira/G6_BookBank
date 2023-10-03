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

# مقدار p-value بسیار کوچکتر از سطح معناداری 0.05 است. بنابراین، می‌توان نتیجه گرفت که نوع جلد تأثیر قابل توجه‌ای در قیمت کتاب دارد.
# 1. ممکن است در بازار کتاب، جلد سخت به عنوان یک عامل ارزشمند شناخته شده است و ممکن است خریداران بیشتری آماده باشند برای پرداخت قیمت بالاتری برای کتاب‌های با جلد سخت.
# 2. توجیه دیگر برای تفاوت قیمت بین کتاب‌های با جلد سخت و نرم این است که جلد سخت معمولاً هزینه تولید بیشتری دارد. به عنوان مثال، استفاده از جلد سخت ممکن است نیاز به استفاده از مواد با کیفیت بالاتر و فرآیندهای تولید پیچیده‌تری داشته باشد که هزینه بیشتری را ایجاد می‌کند. بنابراین، این هزینه بالاتر می‌تواند به قیمت بالاتر کتاب‌های با جلد سخت منجر شود.
# 3. یک توجیه دیگر ممکن است در ارتباط با مقاومت و طول عمر جلد سخت باشد. جلد سخت معمولاً مقاومت بیشتری در برابر سایش، شکستگی و آسیب‌های دیگر دارد. این مقاومت بالاتر می‌تواند منجر به طول عمر بیشتر کتاب‌های با جلد سخت شود و خریداران ممکن است تمایل داشته باشند برای خرید کتابی که مقاومت و طول عمر بیشتری دارد، قیمت بالاتری را پرداخت کنند.

