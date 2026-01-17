import config
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import product
from sqlalchemy.orm import Session
import db_model

app = FastAPI()

# Correctly add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
db_model.Base.metadata.create_all(bind=config.engine)


@app.get("/")
def greet():
    return "Hello, World!"


products = [
    product(
        id=1,
        name="Laptop",
        price=999.99,
        in_stock=True,
        description="A high-performance laptop",
    ),
    product(
        id=2,
        name="Smartphone",
        price=499.99,
        in_stock=True,
        description="A latest model smartphone",
    ),
    product(
        id=3,
        name="Headphones",
        price=199.99,
        in_stock=False,
        description="Noise-cancelling headphones",
    ),
]


def get_db():
    db = config.session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = config.session()
    count = db.query(db_model.product).count()
    # Add initial products to the database
    if count == 0:
        for prod in products:
            # convert Pydantic model instance to dict correctly
            db.add(db_model.product(**prod.model_dump()))
    db.commit()


init_db()


@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(db_model.product).all()
    return db_products


@app.get("/product/{product_id}")
def get_user_by_id(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(db_model.product).filter(db_model.product.id == product_id).first()
    )
    if product:
        return product
    return "product not found"


@app.post("/products")
def create_product(new_product: product, db: Session = Depends(get_db)):
    # convert incoming Pydantic model to dict
    db_product = db_model.product(**new_product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.put("/products/")
def update_product(id: int, product: product, db: Session = Depends(get_db)):
    db_product = db.query(db_model.product).filter(db_model.product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.price = product.price
        db_product.in_stock = product.in_stock
        db_product.description = product.description
        db.commit()
        db.refresh(db_product)
        return db_product
    return "product not found"


@app.delete("/products")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(db_model.product).filter(db_model.product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "product deleted"
    return "product not found"
