import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
# Connect to the my_books.db database
conn = sqlite3.connect('my_books.db')

# Get the tables
books = pd.read_sql('SELECT * FROM Books', conn) #column names: index	ID	Title	EnglishTitle	AnotherName	TitleRating	DataRating	ISBN	GhatE	PageCount	PersianPublishYear	GregorianPublishYear	CoverType	Series	NumberBookCovers
price = pd.read_sql('SELECT * FROM Price', conn) #column names: index	BookID	Price	DiscountPercentage	Exists	EarliestDeliveryDate
books_info = pd.read_sql('SELECT * FROM BooksInfo', conn)#column names: 	index	BookID	URL	Summary
book_publishers = pd.read_sql('SELECT * FROM BookPublishers', conn) #column names: index	BookID	PublisherID
publishers = pd.read_sql('SELECT * FROM Publishers', conn)#column names: index	ID	Name	URL
book_authors = pd.read_sql('SELECT * FROM BookAuthors', conn)#column names: index	BookID	PersonID
book_translators = pd.read_sql('SELECT * FROM BookTranslators', conn)#column names: index	BookID	PersonID
book_illustrators = pd.read_sql('SELECT * FROM BookIllustrators', conn)#column names: book_illustrators
book_editors = pd.read_sql('SELECT * FROM BookEditors', conn)#column names:  index	BookID	PersonID
book_speakers = pd.read_sql('SELECT * FROM BookSpeakers', conn)#column names:  index	BookID	PersonID
book_tags = pd.read_sql('SELECT * FROM BookTags', conn)#column names: index	BookID	TagID
tags = pd.read_sql('SELECT * FROM Tags', conn)#column names:   	index	ID	Name	URL
persons = pd.read_sql('SELECT * FROM Persons', conn)#column names:  	index	ID	Name	URL

def get_books_by_year():
    query = '''
    SELECT GregorianPublishYear AS Year, COUNT(*) AS NumberOfBooks
    FROM Books
    GROUP BY GregorianPublishYear
    ORDER BY Year;
    '''
    return pd.read_sql_query(query, conn)
def get_top_publishers():
    query = '''
    SELECT p.Name, COUNT(b.PublisherID) AS BooksPublished
    FROM Publishers AS p
    LEFT JOIN BookPublishers AS b ON p.ID = b.PublisherID
    GROUP BY p.Name
    ORDER BY BooksPublished DESC
    LIMIT 10;
    '''
    return pd.read_sql_query(query, conn)

# Streamlit UI
st.title('Book Publishers Dashboard')

# Load data
publishers_data = get_top_publishers()

# Display top 10 publishers chart using Plotly
st.subheader('Top 10 Publishers')
fig = px.bar(
    publishers_data,
    x='BooksPublished',
    y='Name',
    orientation='h',
    title='Top 10 Publishers by Number of Books Published'
)

# Add text labels to each bar
fig.update_traces(texttemplate='%{x}', textposition='outside')

fig.update_layout(xaxis_title='Number of Books Published', yaxis_title='Publisher Name')
st.plotly_chart(fig)




# Group books by publisher and count the number of books
books_by_publisher = book_publishers.groupby('PublisherID').size().reset_index(name='BookCount')
books_by_publisher = pd.merge(books_by_publisher, publishers, left_on='PublisherID', right_on='ID')

# Create a bar chart
fig = px.bar(
    books_by_publisher,
    x='Name',
    y='BookCount',
    labels={'Name': 'Publisher', 'BookCount': 'Number of Books/Publications'},
    title='Number of Books/Publications by Publisher'
)

# Customize the chart (optional)
fig.update_layout(xaxis_title='Publisher', yaxis_title='Number of Books/Publications')

# Display the chart
st.plotly_chart(fig)

# Number of books/publications chart
st.subheader('Number of Books/Publications by Type')
fig_books = px.bar(
    books['CoverType'].value_counts(),
    x=books['CoverType'].value_counts().index,
    y=books['CoverType'].value_counts().values,
    labels={'x': 'Cover Type', 'y': 'Number of Books'},
    title='Number of Books/Publications by Type'
)
st.plotly_chart(fig_books)

# Number of books by year of publication chart
st.subheader('Number of Books by Year of Publication')
books_by_year = get_books_by_year()
if not books_by_year.empty:
    fig_years = px.line(
        books_by_year,
        x='Year',
        y='NumberOfBooks',
        labels={'Year': 'Publication Year', 'NumberOfBooks': 'Number of Books'},
        title='Number of Books by Year of Publication'
    )
    st.plotly_chart(fig_years)
else:
    st.info("No data available for the 'Number of Books by Year of Publication' chart.")


# Close the database connection
conn.close()