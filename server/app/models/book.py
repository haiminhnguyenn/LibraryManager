import uuid

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class Book(db.Model):
    
    __tablename__ = "books"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    
    
    def __init__(self, title, author, image_url, description, price):
        self.title = title
        self.author = author
        self.image_url = image_url
        self.description = description
        self.price = price
    
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}