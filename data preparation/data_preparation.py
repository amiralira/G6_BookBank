import numpy as np
import pandas as pd
import json
import ast
import hashlib


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


def parse_dict(row):
    try:
        return ast.literal_eval(row)
    except (SyntaxError, ValueError):
        return None


def hash_id(row):
    if pd.isna(row["id"]):
        return hashlib.md5(row["name"].encode("utf-8")).hexdigest()
    else:
        return row["id"]


def list_to_df(df_col):
    my_list = df_col.explode().tolist()
    my_list = [item for item in my_list if item is not np.nan]
    return pd.DataFrame(my_list)


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

df_publisher = pd.DataFrame(df_book[col_publisher].apply(pd.Series))
#
df_publisher = df_publisher.dropna(subset=["name"])
df_publisher = df_publisher.drop_duplicates(subset="id", keep="first").reset_index(
    drop=True
)

df_author = pd.DataFrame(df_book[col_author].apply(pd.Series))
#
df_author = df_author.dropna(subset=["name"])
df_author = df_author.drop_duplicates(subset="id", keep="first").reset_index(drop=True)


df_tags = list_to_df(df_book[col_tags])
df_tags = df_tags.drop_duplicates(subset="id", keep="first").reset_index(drop=True)

df_translator = list_to_df(df_book[col_translator])
df_translator["id"] = df_translator.apply(hash_id, axis=1)
df_translator = df_translator.drop_duplicates(subset="id", keep="first").reset_index(
    drop=True
)

df_illustrator = list_to_df(df_book[col_illustrator])
df_illustrator["id"] = df_illustrator.apply(hash_id, axis=1)
df_illustrator = df_illustrator.drop_duplicates(subset="id", keep="first").reset_index(
    drop=True
)

df_editor = list_to_df(df_book[col_editor])
df_editor["id"] = df_editor.apply(hash_id, axis=1)
df_editor = df_editor.drop_duplicates(subset="id", keep="first").reset_index(drop=True)

df_speaker = list_to_df(df_book[col_speaker])
df_speaker["id"] = df_speaker.apply(hash_id, axis=1)
df_speaker = df_speaker.drop_duplicates(subset="id", keep="first").reset_index(
    drop=True
)