import numpy as np
import pandas as pd
import ast
import hashlib


def parse_dict(row):
    try:
        return ast.literal_eval(row)
    except (SyntaxError, ValueError):
        return None


def update_column(row, col_roles, column_name):
    try:
        if not pd.isna(row[column_name]):
            unique_items = {}
            for item in row[col_roles]:
                unique_items[item["id"]] = item
            unique_items = list(unique_items.values())
            my_list = []
            full_name = row[column_name]
            for item in unique_items:
                if item["name"] in full_name:
                    full_name = full_name.replace(item["name"], "")
                    my_list.append(item)
            if my_list == [] or full_name != "":
                my_list.append(
                    {
                        "id": np.nan,
                        "name": full_name,
                        "url": np.nan,
                    }
                )
            return my_list
    except:
        print("err in row\n", row)
    return row[column_name]


def connecting_relationships_optimized(df, col_name_ref):
    df_temp = pd.json_normalize(df[col_name_ref]).reset_index(drop=True)
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, df_temp], axis=1)
    df.drop(col_name_ref, axis=1, inplace=True)
    return df.reset_index(drop=True)


def hash_id(row):
    if pd.isna(row["id"]):
        return hashlib.md5(row["name"].encode("utf-8")).hexdigest()
    else:
        return row["id"]


df_p0 = pd.read_csv("all_product_details(p0).csv", low_memory=False)
df_p1 = pd.read_csv("all_product_details(p1).csv", low_memory=False)
df_p2 = pd.read_csv("all_product_details(p2).csv", low_memory=False)
df_p3 = pd.read_csv("all_product_details(p3).csv", low_memory=False)
df_p4 = pd.read_csv("all_product_details(p4).csv", low_memory=False)
df_p5 = pd.read_csv("all_product_details(p5).csv", low_memory=False)
df_p6 = pd.read_csv("all_product_details(p6).csv", low_memory=False)
df_p7 = pd.read_csv("all_product_details(p7).csv", low_memory=False)
df_p8 = pd.read_csv("all_product_details(p8).csv", low_memory=False)
df_p9 = pd.read_csv("all_product_details(p9).csv", low_memory=False)
df_err = pd.read_csv("all_product_details(err).csv", low_memory=False)

df = pd.concat(
    [
        df_p0,
        df_p1,
        df_p2,
        df_p3,
        df_p4,
        df_p5,
        df_p6,
        df_p7,
        df_p8,
        df_p9,
        df_err,
    ],
    ignore_index=True,
)

df_book = df.dropna(subset=["کد کتاب :"])
df_book["کد کتاب :"] = df_book["کد کتاب :"].astype(int)
df_book["تعداد صفحه:"] = (
    pd.to_numeric(
        df_book["تعداد صفحه:"],
        errors="coerce",
    )
    .fillna(-1)
    .astype(int)
)
df_book["سال انتشار شمسی:"] = (
    pd.to_numeric(
        df_book["سال انتشار شمسی:"],
        errors="coerce",
    )
    .fillna(-1)
    .astype(int)
)
df_book["سال انتشار میلادی:"] = (
    pd.to_numeric(
        df_book["سال انتشار میلادی:"],
        errors="coerce",
    )
    .fillna(-1)
    .astype(int)
)
df_book["سری چاپ:"] = (
    pd.to_numeric(
        df_book["سری چاپ:"],
        errors="coerce",
    )
    .fillna(-1)
    .astype(int)
)
df_book["تعداد جلد:"] = (
    pd.to_numeric(
        df_book["تعداد جلد:"],
        errors="coerce",
    )
    .fillna(-1)
    .astype(int)
)
df_book["price"] = df_book["price"].str.replace(",", "").astype(int)
df_book["discount"] = df_book["discount"].str.rstrip(" % تخفیف")
df_book["discount"] = df_book["discount"].fillna(-1).astype(int)

df_book = df_book.drop_duplicates(subset="کد کتاب :", keep="first")
df_book = df_book.dropna(axis=1, how="all")

my_columns = df_book.columns
col_roles = my_columns[15]
col_publisher = my_columns[16]
col_author = my_columns[17]
col_tags = my_columns[18]
col_translator = my_columns[22]
col_illustrator = my_columns[31]
col_editor = my_columns[32]
col_speaker = my_columns[33]
roles = [col_translator, col_illustrator, col_editor, col_speaker]

df_book[col_roles] = df_book[col_roles].apply(lambda x: ast.literal_eval(x))
df_book[col_tags] = df_book[col_tags].apply(lambda x: ast.literal_eval(x))
df_book[col_publisher] = df_book[col_publisher].apply(parse_dict)
df_book[col_author] = df_book[col_author].apply(parse_dict)

for role in roles:
    df_book[role] = df_book.apply(
        lambda row: update_column(row, col_roles, role), axis=1
    )

# ------------------------------------------------------------------
# Publisher DataFrame
df_publisher = df_book[["کد کتاب :", col_publisher]]
df_publisher = connecting_relationships_optimized(df_publisher, col_publisher)
#
df_publisher = df_publisher.dropna(subset=["name"])

# ------------------------------------------------------------------
# Author DataFrame
df_author = df_book[["کد کتاب :", col_author]]
df_author = connecting_relationships_optimized(df_author, col_author)
#
df_author = df_author.dropna(subset=["name"]).reset_index(drop=True)

# ------------------------------------------------------------------
# Tags DataFrame
df_tags = df_book[["کد کتاب :", col_tags]]
df_tags = df_tags.explode(col_tags, ignore_index=True)
df_tags = connecting_relationships_optimized(df_tags, col_tags)
#
df_tags = df_tags.dropna(subset=["name"]).reset_index(drop=True)

# ------------------------------------------------------------------
# Translator DataFrame
df_translator = df_book[["کد کتاب :", col_translator]]
df_translator = df_translator.explode(col_translator, ignore_index=True)
df_translator = connecting_relationships_optimized(df_translator, col_translator)
df_translator = df_translator.dropna(subset=["name"]).reset_index(drop=True)
df_translator["id"] = df_translator.apply(hash_id, axis=1)

# ------------------------------------------------------------------
# Illustrator DataFrame
df_illustrator = df_book[["کد کتاب :", col_illustrator]]
df_illustrator = df_illustrator.explode(col_illustrator, ignore_index=True)
df_illustrator = connecting_relationships_optimized(df_illustrator, col_illustrator)
df_illustrator = df_illustrator.dropna(subset=["name"]).reset_index(drop=True)
df_illustrator["id"] = df_illustrator.apply(hash_id, axis=1)

# ------------------------------------------------------------------
# Editor DataFrame
df_editor = df_book[["کد کتاب :", col_editor]]
df_editor = df_editor.explode(col_editor, ignore_index=True)
df_editor = connecting_relationships_optimized(df_editor, col_editor)
df_editor = df_editor.dropna(subset=["name"]).reset_index(drop=True)
df_editor["id"] = df_editor.apply(hash_id, axis=1)

# ------------------------------------------------------------------
# Speaker DataFrame
df_speaker = df_book[["کد کتاب :", col_speaker]]
df_speaker = df_speaker.explode(col_speaker, ignore_index=True)
df_speaker = connecting_relationships_optimized(df_speaker, col_speaker)
df_speaker = df_speaker.dropna(subset=["name"]).reset_index(drop=True)
df_speaker["id"] = df_speaker.apply(hash_id, axis=1)
df_speaker

# ----------------------------------------------------------------------------------------------------------
# Building a DataFrame of Database Tables

# Books Database
df_table_books = df_book[
    [
        "کد کتاب :",
        "name",
        "eng_name",
        "title",
        "title_rating",
        "data_rating",
        "شابک:",
        "قطع:",
        "تعداد صفحه:",
        "سال انتشار شمسی:",
        "سال انتشار میلادی:",
        "نوع جلد:",
        "سری چاپ:",
        "تعداد جلد:",
    ]
]
df_table_books.columns = [
    "ID",
    "Title",
    "EnglishTitle",
    "AnotherName",
    "TitleRating",
    "DataRating",
    "ISBN",
    "GhatE",
    "PageCount",
    "PersianPublishYear",
    "GregorianPublishYear",
    "CoverType",
    "Series",
    "NumberBookCovers",
]

# Price Database
df_table_price = df_book[
    [
        "کد کتاب :",
        "price",
        "discount",
        "exists",
        "زودترین زمان ارسال:",
    ]
]
df_table_price.columns = [
    "BookID",
    "Price",
    "DiscountPercentage",
    "HasExists",
    "EarliestDeliveryDate",
]
# df_table_price["Exists"] = df_table_price["Exists"].astype(bool)

# BooksInfo Database
df_table_books_info = df_book[
    [
        "کد کتاب :",
        "url",
        "description",
    ]
]
df_table_books_info.columns = ["BookID", "URL", "Summary"]

# BookPublishers Database
df_table_book_publishers = df_publisher[["کد کتاب :", "id"]]
df_table_book_publishers.columns = ["BookID", "PublisherID"]

# Publishers Database
df_table_publishers = df_publisher[["id", "name", "url"]]
df_table_publishers = df_table_publishers.drop_duplicates(
    subset="id", keep="first"
).reset_index(drop=True)
df_table_publishers.columns = ["ID", "Name", "URL"]

# BookAuthors Database
df_table_book_authors = df_author[["کد کتاب :", "id"]]
df_table_book_authors.columns = ["BookID", "PersonID"]

# BookTranslators Database
df_table_book_translators = df_translator[["کد کتاب :", "id"]]
df_table_book_translators.columns = ["BookID", "PersonID"]

# BookIllustrators Database
df_table_book_illustrators = df_illustrator[["کد کتاب :", "id"]]
df_table_book_illustrators.columns = ["BookID", "PersonID"]

# BookEditors Database
df_table_book_editors = df_editor[["کد کتاب :", "id"]]
df_table_book_editors.columns = ["BookID", "PersonID"]

# BookSpeakers Database
df_table_book_speakers = df_speaker[["کد کتاب :", "id"]]
df_table_book_speakers.columns = ["BookID", "PersonID"]

# BookTags Database
df_table_book_tags = df_tags[["کد کتاب :", "id"]]
df_table_book_tags.columns = ["BookID", "TagID"]

# Tags Database
df_table_tags = df_tags[["id", "name", "url"]]
df_table_tags = df_table_tags.drop_duplicates(subset="id", keep="first").reset_index(
    drop=True
)
df_table_tags.columns = ["ID", "Name", "URL"]

# Persons Database
df_table_persons = pd.concat(
    [
        df_author,
        df_translator,
        df_illustrator,
        df_editor,
        df_speaker,
    ],
    ignore_index=True,
)
df_table_persons = df_table_persons[["id", "name", "url"]]
df_table_persons = df_table_persons.drop_duplicates(
    subset="id", keep="first"
).reset_index(drop=True)
df_table_persons.columns = ["ID", "Name", "URL"]


# my DataFrames: df_publisher, df_author, df_tags, df_translator, df_illustrator, df_editor, df_speaker

# my Database DataFrames:
# df_table_books, df_table_price, df_table_books_info, df_table_book_publishers, df_table_publishers,
# df_table_book_authors, df_table_book_translators, df_table_book_illustrators, df_table_book_editors,
# df_table_book_speakers, df_table_book_tags, df_table_tags, df_table_persons