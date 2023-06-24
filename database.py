import databases
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey

DATABASE_URL = "postgresql://username:password@localhost/mydatabase"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

users = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(100)),
    Column("email", String(100), unique=True),
    Column("password", String(100)),
    Column("phone", String(20), unique=True),
)

profile = sqlalchemy.Table(
    "profile",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), unique=True),
    Column("profile_picture", String(100)),
)