import sqlite3
from pathlib import Path

# Database location
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


DB_PATH = DATA_DIR / "grocerypos.db"


# Connect to database
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Sales table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL NOT NULL,
            discount REAL NOT NULL DEFAULT 0,
            sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Sales Items
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            product_id INTEGER,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales(id)
        )
    """)

    conn.commit()
    conn.close()


def add_product(name, price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    conn.close()

    return products


def update_product(product_id, name, price, stock):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE products
        SET name = ?, price = ?, stock = ?
        WHERE id = ?    
        """,
        (name, price, stock, product_id)
    )

    conn.commit()
    conn.close()


def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    conn.commit()
    conn.close()


def create_sale(cart, products, total, discount):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")

        # check stock availability before recording the sale
        for product_id, quantity in cart.items():

            cursor.execute(
                "SELECT stock FROM products WHERE id = ?",
                (product_id,)
            )

            result = cursor.fetchone()

            if result is None or result[0] < quantity:
                raise ValueError("Insufficient stock for one or more products.")


        # Create the main sale record 
        cursor.execute(
            "INSERT INTO sales (total, discount) VALUES (?, ?)",
            (total, discount)
        )

        sale_id = cursor.lastrowid

        # Record each product and deduct its stock
        for product_id, quantity in cart.items():

            product = products[product_id]

            cursor.execute(
                """
                INSERT INTO sale_items
                (sale_id, product_id, product_name, price, quantity)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    sale_id,
                    product_id,
                    product["name"],
                    product["price"],
                    quantity
                )
            )

            cursor.execute(
                """
                UPDATE products
                SET stock = stock - ?
                WHERE id = ?
                """,
                (quantity, product_id)
            )

        conn.commit()
        return sale_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    