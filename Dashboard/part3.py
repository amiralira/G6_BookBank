import mysql.connector
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345roshanak',
    'database': 'my_books'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


# Function to get the most popular book tags
def get_popular_tags():
    query = '''
    SELECT t.Name AS Tag, COUNT(bt.TagID) AS TagCount
    FROM Tags AS t
    INNER JOIN BookTags AS bt ON t.ID = bt.TagID
    GROUP BY Tag
    ORDER BY TagCount DESC
    LIMIT 10;  -- You can adjust the limit to show more or fewer tags
    '''
    return pd.read_sql_query(query, conn)

# Load data
books = pd.read_sql('SELECT * FROM Books', conn) 
price = pd.read_sql('SELECT * FROM Price', conn) 

# Streamlit UI
st.title('Book Analytics Dashboard')

# Analysis 1: Price Distribution by Book Type
st.subheader('Price Distribution by Book Type')
books_price = pd.merge(books, price, left_on='ID', right_on='BookID')
price_distribution = px.box(books_price, x='CoverType', y='Price', labels={'Price': 'Book Price'})
st.plotly_chart(price_distribution)

# Analysis 2: Publication Year Trends
st.subheader('Publication Year Trends')
# Group by GregorianPublishYear and count the number of books in each year
year_counts = books['GregorianPublishYear'].value_counts().reset_index()
year_counts.columns = ['GregorianPublishYear', 'NumberOfBooks']
year_trends = px.line(year_counts, x='GregorianPublishYear', y='NumberOfBooks', title='Publication Year Trends')
year_trends.update_xaxes(title='Gregorian Publish Year')
year_trends.update_yaxes(title='Number of Books')
st.plotly_chart(year_trends)

# Analysis 3: Author vs. Translator Contributions
st.subheader('Author vs. Translator Contributions')
contributions = {
    'Authors': len(books['ID'].unique()),
    'Translators': len(pd.read_sql('SELECT DISTINCT PersonID FROM BookTranslators', conn))
}
contributions_chart = px.pie(
    values=list(contributions.values()), 
    names=list(contributions.keys()), 
    title='Author vs. Translator Contributions'
)
st.plotly_chart(contributions_chart)



# Analysis 4: Get the most popular book tags
popular_tags = get_popular_tags()

# Display the bar chart
if not popular_tags.empty:
    st.subheader('Top 10 Popular Book Tags')
    fig_tags = px.bar(
        popular_tags,
        x='TagCount',
        y='Tag',
        orientation='h',
        labels={'TagCount': 'Tag Count', 'Tag': 'Book Tag'},
        title='Top 10 Popular Book Tags'
    )
    st.plotly_chart(fig_tags)
else:
    st.info("No data available for the 'Top Authors by Number of Books Authored' chart.")

conn.close()











