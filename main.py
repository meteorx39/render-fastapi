from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import date
from database import get_db
import crud
from pymysql.connections import Connection

app = FastAPI()

# 定義 Schema：這必須跟資料庫欄位一模一樣
class ProductSchema(BaseModel):
    title: str
    price: float
    stock: int
    arrival_date: date

# 讀取產品
@app.get("/products")
def read_all(db: Connection = Depends(get_db)):
    return crud.get_all_products(db)

@app.get("/products/{product_id}")
def read_one(product_id: int, db: Connection = Depends(get_db)):
    product = crud.get_one_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="找不到該產品")
    return product

# 新增產品
@app.post("/products")
def add_product(product: ProductSchema, db: Connection = Depends(get_db)):
    # 將解碼後的 Pydantic 資料轉交給 CRUD 執行
    new_id = crud.create_product(
        db, 
        title=product.title, 
        price=product.price, 
        stock=product.stock, 
        arrival_date=product.arrival_date
    )
    return {"message": "產品新增成功", "id": new_id}

# 更新產品
@app.put("/products/{product_id}")
def edit_product(product_id: int, product: ProductSchema, db: Connection = Depends(get_db)):
    updated_rows = crud.update_product(
        db, 
        product_id=product_id,
        title=product.title, 
        price=product.price, 
        stock=product.stock, 
        arrival_date=product.arrival_date
    )
    if updated_rows == 0:
        raise HTTPException(status_code=404, detail="產品不存在，無法更新")
    return {"message": "產品更新成功"}

# 刪除產品
@app.delete("/products/{product_id}")
def remove_product(product_id: int, db: Connection = Depends(get_db)):
    deleted_rows = crud.delete_product(db, product_id)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="產品不存在，無法刪除")
    return {"message": f"ID {product_id} 已成功刪除"}