import pandas as pd
import sqlite3

import sqlite3

try:
    conn = sqlite3.connect('my_books.db')
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)

cursor = conn.cursor()

#1st client request
query = 'SELECT DISTINCT\
        p.Name AS name \
    FROM BookTags AS bt \
    INNER JOIN Tags AS t ON \
        bt.BookID = t.ID \
    INNER JOIN Books AS B ON \
        bt.BookID = b.ID \
    INNER JOIN BookAuthors AS ba ON \
        b.ID = ba.BookID \
    INNER JOIN Persons AS p ON \
        ba.PersonID = p.ID \
    WHERE t.Name LIKE "%عاشقانه%" \
    ORDER BY SUM(b.DataRating) OVER(PARTITION BY P.Name) DESC \
    LIMIT 5;'

df1 = pd.read_sql(query, conn)

df1.to_csv('first_client_request.csv')

# 2nd client request
query = 'WITH tmp_table \
    AS ( \
    SELECT \
        ID, \
        Title title, \
        NTILE(4) OVER (ORDER BY DataRating DESC) rate_quartile, \
        DataRating rating, \
        Price price, \
        NTILE(5) OVER (ORDER BY Price) price_ntile \
    FROM Books \
    INNER JOIN Price ON \
        Books.ID = Price.BookID \
    ) \
SELECT \
    title, \
    rating, \
    price \
FROM tmp_table \
WHERE rate_quartile = 1 AND price_ntile = 1;'

df2 = pd.read_sql(query, conn)

df2.to_csv('second_client_request.csv')

# Writer request
query = 'SELECT \
    p.ID publisher_id, \
    p.Name publisher_name, \
    SUM(b.DataRating) sum \
FROM Tags t \
INNER JOIN BookTags bt ON \
    t.ID = bt.TagID \
INNER JOIN Books b ON \
    bt.BookID =b.ID \
INNER JOIN BookPublishers bp ON \
    bt.BookID = bp.BookID \
INNER JOIN Publishers P ON \
    bp.PublisherID = P.ID \
WHERE t.Name LIKE "%تاریخ%" \
GROUP BY p.ID \
ORDER BY SUM(b.DataRating) DESC \
LIMIT 5;'

df3 = pd.read_sql(query, conn)

df3.to_csv('writer_request.csv')