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

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return db_user

@app.delete("/users/{user.id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User not found")
    db.delete(db_user)
    db.commit()

@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    # Check if the user exists
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    db_user.username = user.username
    db.commit()
    return {"message": "User updated successfully"}

##Beer(C.R.U.D)
@app.post("/beers/", status_code=status.HTTP_201_CREATED)
async def create_beer(beer: BeerBase, db: db_dependency):
    db_beer = models.Beer(**beer.model_dump())
    db.add(db_beer)
    db.commit()

@app.get("/beers/{beer_id}", status_code=status.HTTP_200_OK)
async def get_beers(beer_id: int, db: db_dependency):
    db_beer = db.query(models.Beer).filter(models.Beer.id == beer_id).first()
    if not db_beer:
        raise HTTPException(status_code=404, detail=f"Beer item {beer_id} not found")
    return db_beer

@app.delete("/beers/{beer_id}", status_code=status.HTTP_200_OK)
async def delete_beer(beer_id: int, db: db_dependency):
    db_beer = db.query(models.Beer).filter(models.Beer.id == beer_id).first()
    if not db_beer:
        raise HTTPException(status_code=404, detail=f"Beer item {beer_id} not found")
    db.delete(db_beer)
    db.commit()
    return {"message": "Beer deleted successfully"}

@app.put("/beers/{sport_id}", status_code=status.HTTP_200_OK)
async def update_beer(beer_id: int, beer: BeerBase, db: db_dependency):
    db_beer = db.query(models.Beer).filter(models.Beer.id == beer_id).first()
    if not db_beer:
        raise HTTPException(status_code=404, detail=f"Beer item {beer_id} not found")
    db_beer.style = beer.style
    db_beer.alcohol = beer.alcohol
    db_beer.cereal = beer.cereal
    db.commit()
    return {"message": "Updated successfully"}