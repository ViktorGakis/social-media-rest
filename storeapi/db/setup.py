from contextlib import asynccontextmanager

import databases
import sqlalchemy
from fastapi import FastAPI

from ..config import config

metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
)

engine = sqlalchemy.create_engine(
    config.DATABASE_URL,
    # make the process multithreaded
    connect_args={"check_same_thread": False},
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Practically db connects awaits(required process) and disconnects.

    This idea is based on the startup and shutdown events but this is the modern recommended way of doing it.
    """
    await database.connect()
    yield
    await database.disconnect()