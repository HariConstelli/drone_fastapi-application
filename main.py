from fastapi import FastAPI,HTTPException,Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind= engine)


class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

class DroneBase(BaseModel):
    dronetype: str
    target_longitude: float
    target_latitude: float
    radius_km : int
    altitude_meters : int
    duration_minutes: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_posts(post: PostBase, db: db_dependency): # type: ignore
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db: db_dependency): # type: ignore
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    else:
        db.delete(db_post)
        db.commit()
        return 'Post deleted successfully'

@app.post("/drone_data", status_code=status.HTTP_201_CREATED)
async def create_drone_data(data: DroneBase, db: db_dependency): # type: ignore
    try:
        db_drone = models.Drone(**data.dict())
        if db_drone is None:
            raise HTTPException(status_code = '404', detail = "Drone data not found")
        else:
            db.add(db_drone)
            db.commit()
            return {"details": 'Drone data created successfully',
                    "data" : db_drone,
                    "status_code": 200}
    except Exception as e:
        return {"details": f"Exception occured {e}"}

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db:db_dependency): # type: ignore
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        HTTPException(status_code=404, detail='Post not found')
    return post

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db:db_dependency): # type: ignore
    try:
        db_user = models.User(**user.dict())
        if db_user is None:
            raise HTTPException(status_code=404, details = "User data Invalid")
        db.add(db_user)
        db.commit()
        return {"details":f"User with {db_user.username} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail= f"Error occured as {e}")

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db:db_dependency): # type: ignore
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not found")
    
    return user