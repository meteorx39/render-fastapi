from pymysql.connections import Connection
from datetime import date

# 讀取全部
def get_all_products(db: Connection):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, title, price, stock, arrival_date FROM products")
        return cursor.fetchall()

# 讀取單一
def get_one_product(db: Connection, product_id: int):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, title, price, stock, arrival_date FROM products WHERE id = %s", (product_id,))
        return cursor.fetchone()

# 新增產品
def create_product(db: Connection, title: str, price: float, stock: int, arrival_date: date):
    sql = "INSERT INTO products (title, price, stock, arrival_date) VALUES (%s, %s, %s, %s)"
    with db.cursor() as cursor:
        cursor.execute(sql, (title, price, stock, arrival_date))
        db.commit()
        return cursor.lastrowid

# 更新產品
def update_product(db: Connection, product_id: int, title: str, price: float, stock: int, arrival_date: date):
    sql = """
        UPDATE products 
        SET title = %s, price = %s, stock = %s, arrival_date = %s 
        WHERE id = %s
    """
    with db.cursor() as cursor:
        cursor.execute(sql, (title, price, stock, arrival_date, product_id))
        db.commit()
        return cursor.rowcount

# 刪除產品
def delete_product(db: Connection, product_id: int):
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
        db.commit()
        return cursor.rowcount