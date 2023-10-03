import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus


def my_create_engine():
    # Enter the following values to connect to the database
    user = "root"
    password = ""
    host = "localhost"
    port = 3306
    database = "my_books"
    try:    
        engine = create_engine(
            url="mysql+pymysql://{0}:%s@{1}/{2}".format(user, host, database)
            % quote_plus(password)
        )
        return engine
    except:
        st.write("Err in create_engine function")


@st.cache_data
def authors_data():
    engine = my_create_engine()
    query = "SELECT Name FROM my_books.Persons WHERE ID IN (SELECT PersonID FROM my_books.BookAuthors);"
    df = pd.read_sql(query, engine)
    df = df.sort_values(by='Name', ascending=True)
    my_list = [None]
    my_list += df["Name"].tolist()
    return my_list


@st.cache_data
def publishers_data():
    engine = my_create_engine()
    query = "SELECT Name FROM my_books.Publishers;"
    df = pd.read_sql(query, engine)
    df = df.sort_values(by='Name', ascending=True)
    my_list = [None]
    my_list += df["Name"].tolist()
    return my_list


@st.cache_data
def tags_data():
    engine = my_create_engine()
    query = "SELECT Name FROM my_books.Tags;"
    df = pd.read_sql(query, engine)
    df = df.sort_values(by='Name', ascending=True)
    my_list = [None]
    my_list += df["Name"].tolist()
    return my_list


def create_df():
    engine = my_create_engine()
    query = """
        SELECT bi.URL, b.ID, Title, EnglishTitle,
        pa.Name AS Author, 
        pp.Name AS Publisher,
        b.GregorianPublishYear,
        b.PersianPublishYear,
        b.TitleRating, b.DataRating
        FROM my_books.Books AS b
        JOIN my_books.booksinfo AS bi ON b.ID = bi.BookID
        JOIN my_books.BookAuthors AS ba ON b.ID = ba.BookID
        JOIN my_books.Persons AS pa ON ba.PersonID = pa.ID
        JOIN my_books.BookPublishers AS bp ON b.ID = bp.BookID
        JOIN my_books.Publishers AS pp ON bp.PublisherID = pp.ID
    """
    df = pd.read_sql(query, engine)
    return df


st.set_page_config(page_title="Part II")
st.title("Part II: Advanced Search")

authors = authors_data()
publishers = publishers_data()
tags = tags_data()

col1, col2 = st.columns(2)
with col1:
    persian_title = st.text_input("Persian title of the book")
with col2:
    english_title = st.text_input("English title of the book")

col1, col2 = st.columns(2)
with col1:
    from_year = st.number_input("from year of publication", value=2000)
    from_solar_year = st.number_input("from the solar year of publication", value=1378)
with col2:
    to_year = st.number_input("to the year of publication", value=2023)
    to_solar_year = st.number_input("to the solar year of publication", value=1402)

# choose_stars = st.multiselect("Choose from Actors", value)
choose_author = st.selectbox("Choose an Author", authors)
choose_publisher = st.selectbox("Choose an Publisher", publishers)
choose_tag = st.selectbox("Choose an Tag", tags)

col1, col2 = st.columns(2)
with col1:
    from_rate = st.number_input("from rate of book", value=1.0, step=.1, format="%f")
with col2:
    to_rate = st.number_input("to rate of book", value=5.0, step=.1, format="%f")

st.write("")

if st.button("Search", use_container_width=True):
    df = create_df()
    
    if choose_author:
        df = df[df["Author"] == choose_author]
    else:
        df = df.drop_duplicates(subset="Author", keep="first").reset_index(drop=True)
        df = df.drop("Author", axis=1)

    # if choose_tag:

    if choose_publisher:
        df = df[df["Publisher"] == choose_publisher]
    else:
        df = df.drop_duplicates(subset="Publisher", keep="first").reset_index(drop=True)
        df = df.drop("Publisher", axis=1)

    if persian_title and english_title:
        df = df[(df['Title'].str.contains(persian_title)) | (df['EnglishTitle'].str.contains(english_title))]
    elif persian_title:
        df = df['Title'].str.contains(persian_title)
    elif english_title:
        df = df['EnglishTitle'].str.contains(english_title)

    df = df[(df['TitleRating'] >= from_rate) & (df['TitleRating'] <= to_rate) | 
            (df['DataRating'] >= from_rate) & (df['DataRating'] <= to_rate)]

    df = df[(df['GregorianPublishYear'] >= from_year) & (df['GregorianPublishYear'] <= to_year) & 
            (df['PersianPublishYear'] >= from_solar_year) & (df['PersianPublishYear'] <= to_solar_year)]

    st.dataframe(df)