DROP DATABASE IF EXISTS books_db;
CREATE DATABASE IF NOT EXISTS books_db;

USE books_db;

DROP TABLE IF EXISTS BookAuthors;
DROP TABLE IF EXISTS BookTranslators;
DROP TABLE IF EXISTS PersonsInfo;
DROP TABLE IF EXISTS BooksInfo;
DROP TABLE IF EXISTS BookTags;
DROP TABLE IF EXISTS BookPublisher;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Publishers;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Persons;
DROP TABLE IF EXISTS Books;


CREATE TABLE Books (
    ID INT,
    Title VARCHAR(127),
    EngTitle VARCHAR(127),
    Rating FLOAT(3),
    ISBN VARCHAR(15),
    ChatE VARCHAR(9),
    PageCount INT,
    SolarHijriPublishYear YEAR,
    GregorianPublishYear YEAR,
    CoverType VARCHAR(31),
    Series INT,
    Inventory BOOL,
    CONSTRAINT PK_Books PRIMARY KEY (ID)
);

CREATE TABLE Price (
    ID INT AUTO_INCREMENT,
    BookID INT,
    Price INT,
    DiscountPercentage INT,
    Date DATE,
    CONSTRAINT PK_Price PRIMARY KEY (ID),
    CONSTRAINT FK_Price_Books FOREIGN KEY (BookID) REFERENCES Books(ID)
);

CREATE TABLE BooksInfo (
    ID INT AUTO_INCREMENT,
    BookID INT,
    Summary TEXT(16383),
    ImgUrl VARCHAR(127),
    CONSTRAINT PK_BooksInfo PRIMARY KEY (ID),
    CONSTRAINT FK_BooksInfo_Books FOREIGN KEY (BookID) REFERENCES Books (ID)
);


CREATE TABLE Tags (
    ID INT,
    Name VARCHAR(63),
    EngName VARCHAR(31),
    CONSTRAINT PK_Tags PRIMARY KEY (ID)
);


CREATE TABLE BookTags (
    ID INT AUTO_INCREMENT,
    BookID INT,
    TagID INT,
    CONSTRAINT PK_BookTags PRIMARY KEY (ID),
    CONSTRAINT FK_BookTags_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookTags_Tags FOREIGN KEY (TagID) REFERENCES Tags (ID)
);


CREATE TABLE Publishers (
    ID INT,
    Name VARCHAR(63),
    Description TEXT(16383),
    CONSTRAINT PK_Publishers PRIMARY KEY (ID)
);


CREATE TABLE BookPublisher (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PublisherID INT,
    CONSTRAINT PK_BookPublisher PRIMARY KEY (ID),
    CONSTRAINT FK_BookPublisher_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookPublisher_Publishers FOREIGN KEY (PublisherID) REFERENCES Publishers (ID)
);


CREATE TABLE Persons (
    ID INT,
    Name VARCHAR(127),
    CONSTRAINT PK_Persons PRIMARY KEY (ID)
);

CREATE TABLE PersonsInfo (
    ID INT AUTO_INCREMENT,
    PersonID INT,
    Description TEXT(16383),
    ImgUrl VARCHAR(127),
    CONSTRAINT PK_PersonsInfo PRIMARY KEY (ID),
    CONSTRAINT FK_PersonsInfo_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
);

CREATE TABLE BookAuthors (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID INT,
    CONSTRAINT PK_BookAuthors PRIMARY KEY (ID),
    CONSTRAINT FK_BookAuthors_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookAuthors_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
);


CREATE TABLE BookTranslators (
    ID INT AUTO_INCREMENT,
    BookID INT,
    PersonID INT,
    CONSTRAINT PK_BookTranslators PRIMARY KEY (ID),
    CONSTRAINT FK_BookTranslators_Books FOREIGN KEY (BookID) REFERENCES Books (ID),
    CONSTRAINT FK_BookTranslators_Persons FOREIGN KEY (PersonID) REFERENCES Persons (ID)
);