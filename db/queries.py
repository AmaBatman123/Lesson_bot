
CREATE_TABLE_STORE = """
    CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    product_id INTEGER,
    size TEXT,
    category TEXT,
    price INTEGER,
    info_product TEXT,
    collection TEXT,
    photo 
)"""

INSERT_STORE = """
    INSERT INTO store (name, product_id, size, category, price, info_product, collection, photo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
"""

CREATE_TABLE_PRODUCTS = """
CREATE TABLE IF NOT EXISTS products_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    infoproduct TEXT NOT NULL
)"""

INSERT_PRODUCTS = """
    INSERT INTO products_details (product_id, category, infoproduct)
    VALUES (?, ?, ?)
"""

CREATE_TABLE_COLLECTION = """
    CREATE TABLE IF NOT EXISTS collections_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    collection TEXT NOT NULL)
"""

INSERT_COLLECTION = """
    INSERT INTO collections_products (product_id, collection)
    VALUES (?, ?)
"""