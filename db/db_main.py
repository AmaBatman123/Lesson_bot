import sqlite3
from db import queries

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def sql_create():
    if db:
        print('Database connected')
    cursor.execute(queries.CREATE_TABLE_STORE)
    cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    cursor.execute(queries.CREATE_TABLE_COLLECTION)

async def sql_insert_store(name, productid, size, category, price, info_product, collection, photo):
    cursor.execute(queries.INSERT_STORE, (
        name, productid, size, category, price, info_product,collection, photo
    ))
    db.commit()

async def sql_insert_products(productid, category, info_product):
    cursor.execute(queries.INSERT_PRODUCTS, (
        productid, category, info_product
    ))
    db.commit()

async def sql_insert_collection(product_id, collection):
    cursor.execute(queries.INSERT_COLLECTION, (
        product_id, collection
    ))
    db.commit()