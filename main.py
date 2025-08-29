from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

class BeerBase(BaseModel):
    style: str
    alcohol: float
    cereal: str

class TeaBase(BaseModel):
    style: str
    healthy: bool

class ProductBase(BaseModel):
    name: str
    price: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# Posts (CRUD)
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)   # ensures db_post has its ID and is attached to session
    return db_post

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    return db_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post not found")
    db.delete(db_post)
    db.commit()
    return {"message":"Post deleted successfully"}


@app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(post_id: int, post: PostBase, db: db_dependency):
    # Check if the post exists
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.user_id = post.user_id
    db.commit()
    return {"message": "Post updated successfully"}


# Users (CRUD)
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User not found")
    db.delete(db_user)
    db.commit()
    return {"message":"User deleted successfully"}

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    db_user.username = user.username
    db.commit()
    return {"message": "User updated successfully"}



@app.post("/beers/", status_code=status.HTTP_201_CREATED)
async def create_beer(beer: BeerBase, db: db_dependency):
    db_beers = models.Beer(**beer.model_dump())
    db.add(db_beers)
    db.commit()
    db.refresh(db_beers)
    return db_beers


@app.get("/beers/{beer_id}", status_code=status.HTTP_200_OK)
async def get_beers(beer_id: int, db: db_dependency):
    db_beer = db.query(models.Beer).filter(models.Beer.id == beer_id).first()
    if not db_beer:
        raise HTTPException(status_code=404, detail=f"Item {beer_id} not found")
    return db_beer



@app.delete("/beers/{beer_id}", status_code=status.HTTP_200_OK)
async def delete_beer(beer_id: int, db: db_dependency):
    db_beer = db.query(models.Beer).filter(models.Beer.id == beer_id).first()
    if not db_beer:
        raise HTTPException(status_code=404, detail=f"Item {beer_id} not found")
    db.delete(db_beer)
    db.commit()
    return {"message":"Item deleted successfully"}


@app.put("/beers/{beer_id}", status_code=status.HTTP_200_OK)
async def update_beer(beer: BeerBase, beer_id: int, db: db_dependency):
    db_beer = db.query(models.Beer).filter(models.Beer.id == beer_id).first()
    if not db_beer:
        raise HTTPException(status_code=404, detail=f"Item {beer_id} not found")
    
    db_beer.style = beer.style
    db_beer.alcohol = beer.alcohol
    db_beer.cereal = beer.cereal
    db.commit()

    return {"message":"Item updated successfully"}


@app.post("/teas/", status_code=status.HTTP_201_CREATED)
async def create_tea(tea: TeaBase, db: db_dependency):
    db_tea = models.Tea(**tea.model_dump())
    db.add(db_tea)
    db.commit()
    db.refresh(db_tea)
    return db_tea


@app.get("/teas/{tea_id}", status_code=status.HTTP_200_OK)
async def get_teas(tea_id: int, db: db_dependency):
    db_tea = db.query(models.Tea).filter(models.Tea.id == tea_id).first()
    if not db_tea:
        raise HTTPException(status_code=404, detail=f"Item {tea_id} not found")
    return db_tea


@app.delete("/teas/{tea_id}", status_code=status.HTTP_200_OK)
async def delete_tea(tea_id: int, db: db_dependency):
    db_tea = db.query(models.Tea).filter(models.Tea.id == tea_id).first()
    if not db_tea:
        raise HTTPException(status_code=404, detail=f"Item {tea_id} not found")
    db.delete(db_tea)
    db.commit()
    return {"message":"Item deleted successfully"}


@app.put("/teas/{tea_id}", status_code=status.HTTP_200_OK)
async def update_tea(tea: TeaBase, tea_id: int, db: db_dependency):
    db_tea = db.query(models.Tea).filter(models.Tea.id == tea_id).first()
    if not db_tea:
        raise HTTPException(status_code=404, detail=f"Item {tea_id} not found")
    
    db_tea.style = tea.style
    db_tea.healthy = tea.healthy
    db.commit()
    return {"message":"Item updated successfully"}



@app.post("/products/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductBase, db: db_dependency):
    db_product = models.Product(** product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
async def get_products(product_id: int, db: db_dependency):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Item {product_id} not found")
    return db_product



@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, db: db_dependency):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Item {product_id} not found")
    db.delete(db_product)
    db.commit()
    return {"message":"Item deleted successfully"}



@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product: ProductBase, product_id: int, db: db_dependency):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail=f"Item {product_id} not found")
    
    db_product.name = product.name
    db_product.price = product.price
    db.commit()
    return {"message":"Item updated successfully"}