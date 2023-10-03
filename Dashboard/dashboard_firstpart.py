import pandas as pd
import mysql.connector
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px


# Create the connection to database
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345roshanak',
    'database': 'my_books'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

books = pd.read_sql('SELECT * FROM Books', conn) 
price = pd.read_sql('SELECT * FROM Price', conn) 
books_info = pd.read_sql('SELECT * FROM BooksInfo', conn)
book_publishers = pd.read_sql('SELECT * FROM BookPublishers', conn) 
publishers = pd.read_sql('SELECT * FROM Publishers', conn)
book_authors = pd.read_sql('SELECT * FROM BookAuthors', conn)
book_translators = pd.read_sql('SELECT * FROM BookTranslators', conn)
book_illustrators = pd.read_sql('SELECT * FROM BookIllustrators', conn)
book_editors = pd.read_sql('SELECT * FROM BookEditors', conn)
book_speakers = pd.read_sql('SELECT * FROM BookSpeakers', conn)
book_tags = pd.read_sql('SELECT * FROM BookTags', conn)
tags = pd.read_sql('SELECT * FROM Tags', conn)
persons = pd.read_sql('SELECT * FROM Persons', conn)


# section 1 
def get_books_per_tags():
    query = '''
    SELECT T.Name AS TagName, COUNT(BT.BookID) AS BookCount
    FROM Tags AS T
    LEFT JOIN BookTags AS BT ON T.ID = BT.TagID
    GROUP BY T.Name
    order by BookCount desc;
    '''
    return pd.read_sql_query(query, conn)


# section 2
def get_top_publishers():
    query = '''
    SELECT P.Name AS PublisherName, COUNT(*) AS TotalBooks
    FROM Publishers AS P
    INNER JOIN BookPublishers AS BP ON P.ID = BP.PublisherID
    GROUP BY P.Name
    ORDER BY TotalBooks DESC
    LIMIT 10;
    '''
    return pd.read_sql_query(query, conn)


# section 3
def get_books_publish_year():
    query = '''
    SELECT PersianPublishYear AS Persian_Publish_Year, GregorianPublishYear AS Eng_publish_year, COUNT(*) AS TotalBooks
    FROM Books
    WHERE PersianPublishYear != -1 OR GregorianPublishYear != -1
    GROUP BY Persian_Publish_Year, Eng_publish_year
    ORDER BY TotalBooks DESC;
    '''
    return pd.read_sql_query(query, conn)


# section 4
def get_top_writers():
    query = '''
    SELECT P.Name AS AuthorName, COUNT(BA.BookID) AS Total_Books
    FROM Persons AS P
    JOIN BookAuthors AS BA ON P.ID = BA.PersonID
    GROUP BY AuthorName
    ORDER BY Total_Books DESC
    LIMIT 10;
    '''
    return pd.read_sql_query(query, conn)


# section 5
def get_top_translator():
    query = '''
    SELECT P.Name AS TranslatorName, COUNT(BT.BookID) AS TotalTranslatedBooks
    FROM Persons AS P
    Inner JOIN BookTranslators AS BT ON P.ID = BT.PersonID
    GROUP BY P.Name
    ORDER BY TotalTranslatedBooks DESC
    LIMIT 10;
    '''
    return pd.read_sql_query(query, conn)


# section 6
def get_books_pagecount():
    query = '''
    SELECT B.PageCount as Pages, B.PersianPublishYear As PersianPublishYear, B.GregorianPublishYear AS EngPublishYear
    FROM Books AS B
    WHERE B.PageCount <> -1
    ORDER BY Pages DESC ;
    '''
    return pd.read_sql_query(query, conn)


# section 7
def get_price_per_year():
    query = '''
    SELECT B.PersianPublishYear AS PersianPublishYear, B.GregorianPublishYear AS EngPublishYear, P.Price AS Price_without_Discount
    FROM Books AS B
    JOIN Price AS P ON B.ID = P.BookID
    ORDER BY Price_without_Discount DESC ;
    '''
    return pd.read_sql_query(query, conn)


# section 8
def get_price_per_rate():
    query = '''
    SELECT B.DataRating AS Rating, P.Price AS BookPrice
    FROM Books AS B
    JOIN Price AS P ON B.id = P.BookID
    order by BookPrice DESC ;
    '''
    return pd.read_sql_query(query, conn)


# section 9
def get_books_formats():
    query = '''
    SELECT GhatE AS Format, COUNT(*) AS TotalBooks
    FROM Books
    GROUP BY Format
    order by TotalBooks DESC;
    '''
    return pd.read_sql_query(query, conn)



st.title('Book Publishers Dashboard')

# section 1 display
book_tags = get_books_per_tags()
st.subheader('1. Books per Tags')
fig = px.bar(
    book_tags,
    x='BookCount',
    y='TagName',
    orientation='h',
    title='Count of Books per Tags'
)

fig.update_traces(texttemplate='%{x}', textposition='outside')

fig.update_layout(xaxis_title='Number of Books', yaxis_title='Tags Name')
st.plotly_chart(fig)


# section 2 display
top_publisher = get_top_publishers()

st.subheader('2. Top 10 Publishers')
fig = px.bar(
    top_publisher,
    x='TotalBooks',
    y='PublisherName',
    orientation='h',
    title='Top 10 Publishers by Number of Books Published'
)

fig.update_traces(texttemplate='%{x}', textposition='outside')

fig.update_layout(xaxis_title='Number of Books Published', yaxis_title='Publisher Name')
st.plotly_chart(fig)


# section 3 display
publish_year = get_books_publish_year()

st.subheader('3. Books Published Year')
fig = px.bar(
    publish_year,
    x='Persian_Publish_Year',
    y='TotalBooks',
    title='Number of Books by Publisher'
)


fig.update_layout(xaxis_title='Year', yaxis_title='Number of Books')
st.plotly_chart(fig)

# section 4 display
writers = get_top_writers()


if not writers.empty:
    st.subheader('4. Top 10 Authors by Count of Books')
    fig_authors = px.bar(
        writers,
        x='Total_Books',
        y='AuthorName',
        orientation='h',
        labels={'NumberOfBooks': 'Number of Books', 'Author': 'Author Name'},
        title='Top 10 Authors by Number of Books Authored'
    )
    fig.update_traces(texttemplate='%{x}', textposition='outside')
    st.plotly_chart(fig_authors)
else:
    st.info("No data available for the 'Top Authors by Number of Books Authored' chart.")

# section 5 display
translator = get_top_translator()

if not translator.empty:
    st.subheader('5. Top 10 Translators by Number of Books Translated')
    fig_translators = px.bar(
        translator,
        x='TotalTranslatedBooks',
        y='TranslatorName',
        orientation='h',
        labels={'NumberOfBooksTranslated': 'Number of Books Translated', 'Translator': 'Translator Name'},
        title='Top 10 Translators by Number of Books Translated'
    )
    st.plotly_chart(fig_translators)
    fig.update_traces(texttemplate='%{x}', textposition='outside')

else:
    st.info("No data available for the 'Top Translators by Number of Books Translated' chart.")


# section 6 display
page_count = get_books_pagecount ()

if not page_count.empty:
    st.subheader('6. Scatter Chart: Number of Pages vs. Persian Publish Year')
    fig_scatter = px.scatter(
        page_count, 
        x='Pages',
        y='PersianPublishYear',
        title='Scatter Chart: Number of Pages vs. Persian Publish Year'
    )

    st.plotly_chart(fig_scatter)

else:
    st.info("No data available for the scatter chart.")


# section 7 display
price_year = get_price_per_year()

if not price_year.empty:
    st.subheader('7. Scatter Chart: Price without Discount vs. Persian Publish Year')
    fig_scatter = px.scatter(
        price_year, 
        x='Price_without_Discount',
        y='PersianPublishYear',
        title='Scatter Chart: Number of Pages vs. Persian Publish Year'
    )
    st.plotly_chart(fig_scatter)
    
else:
    st.info("No data available for the scatter chart.")


# section 8 display
price_rate = get_price_per_rate ()

if not price_rate.empty:
    st.subheader('8. Scatter Chart: Price vs. Books Rating')
    fig_scatter = px.scatter(
        price_rate, 
        x='BookPrice',
        y='Rating',
        title='Scatter Chart: Number of Pages vs. Persian Publish Year'
    )
    st.plotly_chart(fig_scatter)
    
else:
    st.info("No data available for the scatter chart.")



# section 9 display
books_format = get_books_formats ()
st.subheader('9. Number of Publications by GhatE')

fig_books = px.bar(
    books_format,
    x='Format',
    y='TotalBooks',
    labels={'x': 'GhatE', 'y': 'Number of Books'},
    title='Number of Books by GhatE'
)

fig.update_layout(xaxis_title='Number of Books', yaxis_title='Format')
st.plotly_chart(fig_books)

conn.close()
