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




def get_scatter_data():
    query = '''
    SELECT b.TitleRating AS BookScore, p.Price
    FROM Books AS b
    INNER JOIN Price AS p ON b.ID = p.BookID
    WHERE b.TitleRating IS NOT NULL AND p.Price IS NOT NULL
    '''
    return pd.read_sql_query(query, conn)


def get_scatter_data():
    query = '''
    SELECT PageCount AS number_of_pages,
           PersianPublishYear AS Persian_Publish_Year
    FROM Books
    WHERE Persian_Publish_Year != -1
    '''
    return pd.read_sql_query(query, conn)

def get_top_translators():
    query = '''
    SELECT p.Name AS Translator, COUNT(bt.BookID) AS NumberOfBooksTranslated
    FROM Persons AS p
    INNER JOIN BookTranslators AS bt ON p.ID = bt.PersonID
    GROUP BY Translator
    ORDER BY NumberOfBooksTranslated DESC
    LIMIT 10;
    '''
    return pd.read_sql_query(query, conn)
def get_top_authors():
    query = '''
    SELECT p.Name AS Author, COUNT(ba.BookID) AS NumberOfBooks
    FROM Persons AS p
    INNER JOIN BookAuthors AS ba ON p.ID = ba.PersonID
    GROUP BY Author
    ORDER BY NumberOfBooks DESC
    LIMIT 10;
    '''
    return pd.read_sql_query(query, conn)


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
st.subheader('Number of Books by Publisher')

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
st.subheader('Number of Publications by GhatE')

st.subheader('Number of Books/Publications by GhatE')
fig_books = px.bar(
    books['GhatE'].value_counts(),
    x=books['GhatE'].value_counts().index,
    y=books['GhatE'].value_counts().values,
    labels={'x': 'GhatE', 'y': 'Number of Books'},
    title='Number of Books/Publications by GhatE'
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













# Get the top 10 authors

top_authors = get_top_authors()

# Display the top 10 authors and the number of books they've authored
if not top_authors.empty:
    st.subheader('Top 10 Authors by Number of Books Authored')
    fig_authors = px.bar(
        top_authors,
        x='NumberOfBooks',
        y='Author',
        orientation='h',
        labels={'NumberOfBooks': 'Number of Books', 'Author': 'Author Name'},
        title='Top 10 Authors by Number of Books Authored'
    )
    st.plotly_chart(fig_authors)
else:
    st.info("No data available for the 'Top Authors by Number of Books Authored' chart.")







# Get the top 10 translators
top_translators = get_top_translators()

# Display the top 10 translators and the number of books they've translated
if not top_translators.empty:
    st.subheader('Top 10 Translators by Number of Books Translated')
    fig_translators = px.bar(
        top_translators,
        x='NumberOfBooksTranslated',
        y='Translator',
        orientation='h',
        labels={'NumberOfBooksTranslated': 'Number of Books Translated', 'Translator': 'Translator Name'},
        title='Top 10 Translators by Number of Books Translated'
    )
    st.plotly_chart(fig_translators)
else:
    st.info("No data available for the 'Top Translators by Number of Books Translated' chart.")



# Get the data for the scatter chart
scatter_data = get_scatter_data()

# Display the scatter chart
if not scatter_data.empty:
    st.subheader('Scatter Chart: Number of Pages vs. Persian Publish Year')
    fig_scatter = px.scatter(
        scatter_data,
        x='number_of_pages',
        y='Persian_Publish_Year',
        labels={'number_of_pages': 'Number of Pages', 'Persian_Publish_Year': 'Persian Publish Year'},
        title='Scatter Chart: Number of Pages vs. Persian Publish Year'
    )
    st.plotly_chart(fig_scatter)
else:
    st.info("No data available for the scatter chart.")


# # Merge the books and price tables
# books_price = pd.merge(books, price, left_on='ID', right_on='BookID')[['ID', 'BookID', 'EnglishTitle', 'Price', 'TitleRating','Title','PageCount']]
# # Create a scatter chart of book score vs. price
# fig = px.scatter(books_price, x='TitleRating', y='Price', color='Title', size='PageCount', hover_name='Title')

# # Display the scatter chart
# st.plotly_chart(fig)








# Close the database connection
conn.close()