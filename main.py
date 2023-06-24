from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from .database import database, users, profile

app = FastAPI()

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str
    profile_picture: Optional[str] = None


#db connection
@app.on_event("startup")
async def startup():
    await database.connect()


#close db connection
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

#Register User With Submitted Data
@app.post("/register")
async def register_user(user: UserCreate):
    query = users.insert().values(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        phone=user.phone,
    )

    user_id = await database.execute(query)

    if user.profile_picture:
        query = profile.insert().values(
            user_id=user_id,
            profile_picture=user.profile_picture,
        )
        await database.execute(query)

    return {"message": "User registered successfully"}


#Getting the UserData
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)

    if user:
        query = profile.select().where(profile.c.user_id == user_id)
        profile_data = await database.fetch_one(query)

        user_data = {
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "profile_picture": profile_data.profile_picture if profile_data else None,
        }

        return user_data

    return {"message": "User not found"}