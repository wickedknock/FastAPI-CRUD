from sqlalchemy import CHAR, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column("id", Integer, primary_key=True, nullable=False)
    title = Column("title", String, nullable=False)
    content = Column("content", String, nullable=False)
    published = Column("published", Boolean, nullable=False,
                       server_default='True')
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column("owner_id", Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    # def __init__(self, id, title, content, published):
    #     self.id = id
    #     self.title = title
    #     self.content = content
    #     self.published = published
    #     self.created_at = created

    # def __repr__(self):
    #     return f"({self.id}) {self.title},{self.content}, {self.published} ,{self.created_at}"


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", TIMESTAMP(
        timezone=True), nullable=False, server_default=text('now()'))


class Votes(Base):
    __tablename__ = "votes"

    post_id = Column("post_id", Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column("user_id", Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
