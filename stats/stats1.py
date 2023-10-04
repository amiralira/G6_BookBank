import pandas as pd
import sqlite3
# import mysql.connector

try:
    conn = sqlite3.connect('my_books.db')
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

# user = ""
# password = ""
# host = ""
# port = 
# database = ""

# try:
#     conn = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password,
#             database=database_name,
#     )
# except:
# print("Error in connect_database function")

cursor = conn.cursor()

#1st client's request
query = '''SELECT DISTINCT
        p.Name AS name 
    FROM BookTags AS bt 
    INNER JOIN Tags AS t ON
        bt.BookID = t.ID
    INNER JOIN Books AS B ON
        bt.BookID = b.ID
    INNER JOIN BookAuthors AS ba ON
        b.ID = ba.BookID
    INNER JOIN Persons AS p ON
        ba.PersonID = p.ID
    WHERE t.Name LIKE "%عاشقانه%"  AND b.DataRating >= 0 AND b.DataRating <= 5
    ORDER BY SUM(b.DataRating) OVER(PARTITION BY P.Name) DESC
    LIMIT 5;'''


# query = '''SELECT DISTINCT
#         p.Name AS name 
#     FROM BookTags AS bt 
#     INNER JOIN Tags AS t ON 
#         bt.BookID = t.ID 
#     INNER JOIN Books AS B ON 
#         bt.BookID = b.ID 
#     INNER JOIN BookAuthors AS ba ON 
#         b.ID = ba.BookID 
#     INNER JOIN Persons AS p ON 
#         ba.PersonID = p.ID 
#     WHERE t.Name LIKE "%عاشقانه%"  AND b.DataRating >= 0 AND b.DataRating <= 5
#     ORDER BY SUM((b.DataRating/2.5-1)*(0.5 + 0.5*b.Series) + 0.5) OVER(PARTITION BY p.Name) DESC 
#     LIMIT 5;'''

df1 = pd.read_sql(query, conn)

# sqlite
# 1. سومونک کید 
# 2. جوزف بویدن
# 3. لسلی کانر
# 4. ژوزه ساراماگو
# 5. پیر پژو

# mysql
# 1. سومونک کید 
# 2. پیر پژو
# 3. جوزف بویدن
# 4. ژوزه ساراماگو
# 5. لسلی کانر


# sum of data rating is not a very good criterion, sum of (data rating/2.5 - 1) * (0.5 + Series) plus number of books multiplied by 0.5 could be a better criterion which leads to a different result
# sqlite
# 1. سومونک کید
# 2. لسلی کانر
# 3. جوزف بویدن
# 4. ژوزه ساراماگو
# 5. هرتا مولر

# mysql
# 1. سومونک کید
# 2. لسلی کانر
# 3. جوزف بویدن
# 4. ژوزه ساراماگو
# 5. لسلی کانر


df1.to_csv('first_client_request.csv')

# 2nd client's request
query = '''WITH tmp_table 
    AS ( 
    SELECT 
        ID, 
        Title title, 
        NTILE(4) OVER (ORDER BY DataRating DESC) rate_quartile, 
        DataRating rating, 
        Price price, 
        NTILE(5) OVER (ORDER BY Price) price_ntile 
    FROM Books 
    INNER JOIN Price ON 
        Books.ID = Price.BookID 
    WHERE Price."Exists" = 1
    ) 
SELECT 
    title, 
    rating, 
    price 
FROM tmp_table 
WHERE rate_quartile = 1 AND price_ntile = 1 ;'''

# for MySQL
# query = '''WITH tmp_table 
#     AS ( 
#     SELECT 
#         ID, 
#         Title title, 
#         NTILE(4) OVER (ORDER BY DataRating DESC) rate_quartile, 
#         DataRating rating, 
#         Price price, 
#         NTILE(5) OVER (ORDER BY Price) price_ntile 
#     FROM Books 
#     INNER JOIN Price ON 
#         Books.ID = Price.BookID 
#     WHERE Price.HasExists" = 1
#     ) 
# SELECT 
#     title, 
#     rating, 
#     price 
# FROM tmp_table 
# WHERE rate_quartile = 1 AND price_ntile = 1 ;'''

df2 = pd.read_sql(query, conn)

df2.to_csv('second_client_request.csv')

# Writer's request
query = '''SELECT 
    p.ID publisher_id, 
    p.Name publisher_name, 
    SUM(b.DataRating) sum 
FROM Tags t 
INNER JOIN BookTags bt ON 
    t.ID = bt.TagID 
INNER JOIN Books b ON 
    bt.BookID =b.ID 
INNER JOIN BookPublishers bp ON 
    bt.BookID = bp.BookID 
INNER JOIN Publishers P ON 
    bp.PublisherID = P.ID 
WHERE t.Name LIKE "%تاریخ%" 
GROUP BY p.ID 
ORDER BY SUM(b.DataRating) DESC 
LIMIT 5;'''

# query = '''SELECT 
#     p.ID publisher_id, 
#     p.Name publisher_name, 
#     SUM(b.DataRating) sum 
# FROM Tags t 
# INNER JOIN BookTags bt ON 
#     t.ID = bt.TagID 
# INNER JOIN Books b ON 
#     bt.BookID =b.ID 
# INNER JOIN BookPublishers bp ON 
#     bt.BookID = bp.BookID 
# INNER JOIN Publishers P ON 
#     bp.PublisherID = P.ID 
# WHERE t.Name LIKE "%تاریخ%" 
# GROUP BY p.ID 
# ORDER BY SUM((b.DataRating/2.5-1)*b.Series + 1) DESC 
# LIMIT 5;'''

df3 = pd.read_sql(query, conn)

# sqlite
# 1. ققنوس   
# 2. علم
# 3. نگاه
# 4. علمی و فرهنگی
# 5. سوره مهر

# mysql
# 1. ققنوس   
# 2. علم
# 3. نگاه
# 4. علمی و فرهنگی
# 5. سوره مهر

# sum of data rating is not a very good criterion, sum of (data rating/2.5 - 1) * series plus number of books could be a better criterion which leads to a different result

# sqlite
# 1. امید فردا
# 2. فرهنگستان هنر
# 3. بازتاب نگار
# 4. ققنوس
# 5. نشر نی

# mysql
# 1. امید فردا
# 2. فرهنگستان هنر
# 3. بازتاب نگار
# 4. ققنوس
# 5. نشر نی


df3.to_csv('writer_request.csv')