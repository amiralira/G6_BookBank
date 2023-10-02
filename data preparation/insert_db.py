import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Text, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from book_data_preparation import df_table_books, df_table_price, df_table_books_info, df_table_book_publishers, \
    df_table_publishers, df_table_book_authors, df_table_book_translators, df_table_book_illustrators, \
    df_table_book_editors, df_table_book_speakers, df_table_book_tags, df_table_tags, df_table_persons



db_file = 'my_books.db'

engine = create_engine(f'sqlite:///{db_file}', echo=True)
print(df_table_books.to_sql(name='Books', con=engine, if_exists='append'))
print(df_table_price.to_sql(name='Price', con=engine, if_exists='append'))
print(df_table_books_info.to_sql(name='BooksInfo', con=engine, if_exists='append'))
print(df_table_book_publishers.to_sql(name='BookPublishers', con=engine,if_exists='append'))
print(df_table_publishers.to_sql(name='Publishers', con=engine,if_exists='append'))
print(df_table_book_authors.to_sql(name='BookAuthors', con=engine, if_exists='append'))
print(df_table_book_translators.to_sql(name='BookTranslators', con=engine,if_exists='append'))
print(df_table_book_illustrators.to_sql(name='BookIllustrators', con=engine,if_exists='append'))
print(df_table_book_editors.to_sql(name='BookEditors', con=engine,if_exists='append'))
print(df_table_book_speakers.to_sql(name='BookSpeakers', con=engine,if_exists='append'))
print(df_table_book_tags.to_sql(name='BookTags', con=engine,if_exists='append'))
print(df_table_tags.to_sql(name='Tags', con=engine,if_exists='append'))
print(df_table_persons.to_sql(name='Persons', con=engine,if_exists='append'))
exit()


Base = declarative_base()

class Book(Base):
    __tablename__ = 'Books'

    ID = Column(Integer, primary_key=True)
    Title = Column(String(127))
    EngTitle = Column(String(127))
    Rating = Column(Float(3))
    ISBN = Column(String(15))
    ChatE = Column(String(9))
    PageCount = Column(Integer)
    SolarHijriPublishYear = Column(Integer)
    GregorianPublishYear = Column(Integer)
    CoverType = Column(String(31))
    Series = Column(Integer)
    Inventory = Column(Boolean)

    # Relationships
    publishers = relationship('Publisher', secondary='BookPublisher', back_populates='books')
    tags = relationship('Tag', secondary='BookTag', back_populates='books')
    prices = relationship('Price', back_populates='book')
    books_info = relationship('BooksInfo', back_populates='book')
    book_authors = relationship('BookAuthor', back_populates='book')
    book_translators = relationship('BookTranslator', back_populates='book')

class Price(Base):
    __tablename__ = 'Price'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    BookID = Column(Integer, ForeignKey('Books.ID'))
    Price = Column(Integer)
    DiscountPercentage = Column(Integer)
    Date = Column(Date)

    # Relationships
    book = relationship('Book', back_populates='prices')

class BooksInfo(Base):
    __tablename__ = 'BooksInfo'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    BookID = Column(Integer, ForeignKey('Books.ID'))
    Summary = Column(Text(16383))
    ImgUrl = Column(String(127))

    # Relationships
    book = relationship('Book', back_populates='books_info')

class Tags(Base):
    __tablename__ = 'Tags'

    ID = Column(Integer, primary_key=True)
    Name = Column(String(63))
    EngName = Column(String(31))

    # Relationships
    books = relationship('Book', secondary='BookTag', back_populates='tags')

class BookTags(Base):
    __tablename__ = 'BookTags'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    BookID = Column(Integer, ForeignKey('Books.ID'))
    TagID = Column(Integer, ForeignKey('Tags.ID'))

class Publishers(Base):
    __tablename__ = 'Publishers'

    ID = Column(Integer, primary_key=True)
    Name = Column(String(63))
    Description = Column(Text(16383))

    # Relationships
    books = relationship('Book', secondary='BookPublisher', back_populates='publishers')

class BookPublisher(Base):
    __tablename__ = 'BookPublisher'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    BookID = Column(Integer, ForeignKey('Books.ID'))
    PublisherID = Column(Integer, ForeignKey('Publishers.ID'))

class Persons(Base):
    __tablename__ = 'Persons'

    ID = Column(Integer, primary_key=True)
    Name = Column(String(127))

    # Relationships
    info = relationship('PersonInfo', uselist=False, back_populates='person')

class PersonInfo(Base):
    __tablename__ = 'PersonsInfo'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    PersonID = Column(Integer, ForeignKey('Persons.ID'))
    Description = Column(Text(16383))
    ImgUrl = Column(String(127))

    # Relationships
    person = relationship('Person', back_populates='info')

class BookAuthors(Base):
    __tablename__ = 'BookAuthors'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    BookID = Column(Integer, ForeignKey('Books.ID'))
    PersonID = Column(Integer, ForeignKey('Persons.ID'))

class BookTranslators(Base):
    __tablename__ = 'BookTranslators'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    BookID = Column(Integer, ForeignKey('Books.ID'))
    PersonID = Column(Integer, ForeignKey('Persons.ID'))




Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


def insert_dataframe_data(session, df, model):
    records = df.to_dict(orient='records')
    session.bulk_insert_mappings(model, records)
    session.commit()



dataframes_and_models = [
    (df_table_books, Book),
    (df_table_price, Price),
    (df_table_books_info, BooksInfo),
    (df_table_book_publishers, BookPublisher),
    (df_table_publishers, Publishers),
    (df_table_book_authors, BookAuthors),
    (df_table_book_translators, BookTranslators),
    (df_table_book_illustrators, BookIllustrators),
    (df_table_book_editors, BookEditors),
    (df_table_book_speakers, BookSpeakers),
    (df_table_book_tags, BookTags),
    (df_table_tags, Tags),
    (df_table_persons, Persons),
]


for df, model_class in dataframes_and_models:
    insert_dataframe_data(session, df, model_class)

                   
session.commit()
session.close()

print("Data inserted into the database successfully.")
