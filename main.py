from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5},
]


class ProductUpdate(BaseModel):
    code: str
    name: str
    price: int = Field(gt=0)
    stock: int = Field(ge=0)


def get_product_by_id(id: int):
    for product in products:
        if id == product["id"]:
            return product

    return None


def is_code_exites(code: str):
    for product in products:
        if code == product["code"]:
            return True

    return False


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):
    found_product = get_product_by_id(product_id)
    if not found_product:
        return {"detail": "Product not found"}
    if is_code_exites(product.code):
        return {"detail": "Product code already exists"}

    found_product["code"] = product.code
    found_product["name"] = product.name
    found_product["price"] = product.price
    found_product["stock"] = product.stock
    return {"detail": "Product update sucessfully"}
