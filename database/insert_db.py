import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("/home/rooshanak/Downloads/all_product_details(p0).csv")
engine = create_engine('sqlite:///mydatabase.db', echo=False)

# Define a list of table names where you want to insert the data
table_names = [
        "Books",
        "Price",
        "BooksInfo",
        "Tags",
        "BookTags",
        "Publishers",
        "BookPublisher",
        "Persons",
        "PersonsInfo",
        "BookAuthors",
        "BookTranslators",
        "BookSpeakers",
        "BookEditors",
        "BookIllustrators",   
]

for table_name in table_names:
    df.to_sql(table_name, engine, if_exists='append', index=False)
