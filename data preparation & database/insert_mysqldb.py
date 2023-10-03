import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
from book_data_preparation import df_table_books, df_table_price, df_table_books_info, df_table_book_publishers, \
    df_table_publishers, df_table_book_authors, df_table_book_translators, df_table_book_illustrators, \
    df_table_book_editors, df_table_book_speakers, df_table_book_tags, df_table_tags, df_table_persons


# Enter the following values to connect to the database
user = "root"
password = "khb!1mes2@K-pAsS3#zorie$"
host = "localhost"
port = 3306
database = "my_books"


def connect_database(my_db, my_cursor, host, user, password, database_name):
    try:
        my_db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database_name,
        )
        my_cursor = my_db.cursor()
        return my_db, my_cursor
    except:
        print("Error in connect_database function")


def disconnect_database(my_db, my_cursor):
    try:
        my_cursor.close()
        my_db.close()
        return my_db, my_cursor
    except:
        print("Error in disconnect_database function")


my_db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
)
my_cursor = my_db.cursor()
my_cursor.execute("CREATE DATABASE " + database)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)

create_books_table_query = """
CREATE TABLE Books (
    ID INT,
    Title VARCHAR(127),
    EnglishTitle VARCHAR(250),
    AnotherName VARCHAR(250),
    TitleRating FLOAT(3),
    DataRating FLOAT(3),
    ISBN VARCHAR(50),
    GhatE VARCHAR(20),
    PageCount INT,
    PersianPublishYear INT,
    GregorianPublishYear INT,
    CoverType VARCHAR(31),
    Series INT,
    NumberBookCovers INT,
    CONSTRAINT PK_Books PRIMARY KEY (ID)
)
"""

# 
create_price_table_query = """
CREATE TABLE Price (
    ID INT AUTO_INCREMENT,
    BookID INT,
    Price INT,
    DiscountPercentage INT,
    HasExists TINYINT,
    EarliestDeliveryDate VARCHAR(9),
    CONSTRAINT PK_Price PRIMARY KEY (ID),
    CONSTRAINT FK_Price_Books FOREIGN KEY (BookID) REFERENCES Books(ID)
)
"""

create_books_info_table_query = """
CREATE TABLE BooksInfo (
    ID INT AUTO_INCREMENT,
    BookID INT,
    URL TEXT,
    Summary TEXT(16383),
    CONSTRAINT PK_BooksInfo PRIMARY KEY (ID),
    CONSTRAINT FK_BooksInfo_Books FOREIGN KEY (BookID) REFERENCES Books (ID)
)
"""

create_book_publisher_table_query = """
CREATE TABLE BookPublishers (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PublisherID VARCHAR(100),
    CONSTRAINT PK_BookPublishers PRIMARY KEY (ID),
    CONSTRAINT FK_BookPublishers_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookPublishers_Publishers FOREIGN KEY (PublisherID) REFERENCES Publishers (ID)
)
"""

create_publishers_table_query = """ 
CREATE TABLE Publishers (
    ID VARCHAR(100),
    Name VARCHAR(63),
    URL TEXT,
    CONSTRAINT PK_Publishers PRIMARY KEY (ID)
)
"""

create_book_authors_table_query = """
CREATE TABLE BookAuthors (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID VARCHAR(100),
    CONSTRAINT PK_BookAuthors PRIMARY KEY (ID),
    CONSTRAINT FK_BookAuthors_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookAuthors_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
)
"""

create_book_translators_table_query = """
CREATE TABLE BookTranslators (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID VARCHAR(100),
    CONSTRAINT PK_BookTranslators PRIMARY KEY (ID),
    CONSTRAINT FK_BookTranslators_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookTranslators_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
)
"""

create_book_illustrators_table_query = """
CREATE TABLE BookIllustrators (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID VARCHAR(100),
    CONSTRAINT PK_BookIllustrators PRIMARY KEY (ID),
    CONSTRAINT FK_BookIllustrators_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookIllustrators_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
)
"""

create_book_editors_table_query = """
CREATE TABLE BookEditors (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID VARCHAR(100),
    CONSTRAINT PK_BookEditors PRIMARY KEY (ID),
    CONSTRAINT FK_BookEditors_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookEditors_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
)
"""

create_book_speakers_table_query = """
CREATE TABLE BookSpeakers (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID VARCHAR(100),
    CONSTRAINT PK_BookSpeakers PRIMARY KEY (ID),
    CONSTRAINT FK_BookSpeakers_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookSpeakers_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
)
"""

create_book_tags_table_query = """
CREATE TABLE BookTags (
    ID INT AUTO_INCREMENT,
    BookID INT,
    TagID VARCHAR(100),
    CONSTRAINT PK_BookTags PRIMARY KEY (ID),
    CONSTRAINT FK_BookTags_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookTags_Tags FOREIGN KEY (TagID) REFERENCES Tags (ID)
)
"""

create_tags_table_query = """
CREATE TABLE Tags (
    ID VARCHAR(100),
    Name VARCHAR(63),
    URL TEXT,
    CONSTRAINT PK_Tags PRIMARY KEY (ID)
)
"""

create_persons_table_query = """
CREATE TABLE Persons (
    ID VARCHAR(100),
    Name VARCHAR(63),
    URL TEXT,
    CONSTRAINT PK_Persons PRIMARY KEY (ID)
)
"""

# cursor.execute("SELECT * FROM test.movie")
my_db, my_cursor = connect_database(my_db, my_cursor, host, user, password, database)
my_cursor.execute(create_books_table_query)
my_cursor.execute(create_price_table_query)
my_cursor.execute(create_persons_table_query)
my_cursor.execute(create_publishers_table_query)
my_cursor.execute(create_tags_table_query)
my_cursor.execute(create_books_info_table_query)
my_cursor.execute(create_book_publisher_table_query)
my_cursor.execute(create_book_authors_table_query)
my_cursor.execute(create_book_translators_table_query)
my_cursor.execute(create_book_illustrators_table_query)
my_cursor.execute(create_book_editors_table_query)
my_cursor.execute(create_book_speakers_table_query)
my_cursor.execute(create_book_tags_table_query)
my_db.commit()
my_db, my_cursor = disconnect_database(my_db, my_cursor)


engine = create_engine(
    url="mysql+pymysql://{0}:%s@{1}/{2}".format(user, host, database)
    % quote_plus(password)
)

df_table_books.to_sql(name="Books", con=engine, if_exists="append", index=False)
df_table_price.to_sql(name="Price", con=engine, if_exists="append", index=False)
df_table_books_info.to_sql(name="BooksInfo", con=engine, if_exists="append", index=False)
df_table_tags.to_sql(name="Tags", con=engine, if_exists="append", index=False)
df_table_persons.to_sql(name="Persons", con=engine, if_exists="append", index=False)
df_table_publishers.to_sql(name="Publishers", con=engine, if_exists="append", index=False)
df_table_book_publishers.to_sql(name="BookPublishers", con=engine, if_exists="append", index=False)
df_table_book_authors.to_sql(name="BookAuthors", con=engine, if_exists="append", index=False)
df_table_book_translators.to_sql(name="BookTranslators", con=engine, if_exists="append", index=False)
df_table_book_illustrators.to_sql(name="BookIllustrators", con=engine, if_exists="append", index=False)
df_table_book_editors.to_sql(name="BookEditors", con=engine, if_exists="append", index=False)
df_table_book_speakers.to_sql(name="BookSpeakers", con=engine, if_exists="append", index=False)
df_table_book_tags.to_sql(name="BookTags", con=engine, if_exists="append", index=False)