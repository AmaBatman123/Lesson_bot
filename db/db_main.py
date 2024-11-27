import sqlite3
from itertools import product

from db import queries
import aiosqlite

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def sql_create():
    if db:
        print('Database connected')
    cursor.execute(queries.CREATE_TABLE_STORE)
    cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    cursor.execute(queries.CREATE_TABLE_COLLECTION)

    # Запись стадий FSM_Store
#===========================================================================

async def sql_insert_store(name, product_id, size, category, price, info_product, collection, photo):
    cursor.execute(queries.INSERT_STORE, (
        name, product_id, size, category, price, info_product,collection, photo
    ))
    db.commit()

async def sql_insert_products(product_id, category, info_product):
    cursor.execute(queries.INSERT_PRODUCTS, (
        product_id, category, info_product
    ))
    db.commit()

async def sql_insert_collection(product_id, collection):
    cursor.execute(queries.INSERT_COLLECTION, (
        product_id, collection
    ))
    db.commit()

    # CRUD - Read
#===========================================================================

async def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = aiosqlite.Row
    return conn

async def fetch_all_products():
    conn = await get_db_connection()
    products = conn.execute("""
        SELECT  * from store s
        INNER JOIN products_details pd on s.product_id = pd.product_id
    """).fetchall()
    conn.close()
    return products

    # CRUD - Delete
#===========================================================================

async def delete_products(product_id):
    conn = await get_db_connection()
    conn.execute('DELETE FROM STORE WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()

    # CRUD - Update
#===========================================================================

async def update_product_field(product_id, field_name, new_value):
    store_table = ["name", "size", "category", "price", "photo"]
    store_detail = ["category", "info_product"]

    conn = await get_db_connection()
    try:
        if field_name in store_table:
            query = f'UPDATE STORE SET {field_name} = ? WHERE product_id = ?'
        elif field_name in store_detail:
            query = f'UPDATE store_details SET {field_name} = ? WHERE product_id = ?'
        else:
            raise ValueError(f"Не такого поля {field_name}")

        conn.execute(query, (new_value, product_id))

        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Ошибка - {e}")
    finally:
        conn.close()

