import logging

from app import db
from ...models.book import Book
from ...models.favorite import Favorite


def list_books():
    """ Fetch all books from the database. """
    try:
        books_list = Book.query.all()
        return [book.as_dict() for book in books_list]
    except Exception as e:
        logging.error(f"Error while fetching all books: {str(e)}")
        raise


def get_book_by_id(book_id):
    """ Fetch a book by its id. """
    try:
        book = Book.query.get(book_id)
        if not book:
            return None
        return book
    except Exception as e:
        logging.error(f"Error while fetching book by id: {str(e)}")
        raise
    
    
def save_new_book(title, author, image_url, description, price, quantity):
    """ Save a new book to the database. """
    try:
        new_book = Book(title, author, image_url, description, price, quantity)
        db.session.add(new_book)
        db.session.commit()
        return new_book
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while saving new book: {str(e)}")
        raise
    
    
def update_book_info(book, data):
    """ Update a book in the database. """
    try:
        for key, value in data.items():
            setattr(book, key, value)
        
        db.session.commit()
        return book
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while updating book: {str(e)}")
        raise
    
    
def delete_book_from_db(book):
    """ Delete a book from the database. """
    try:
        db.session.delete(book)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while deleting book: {str(e)}")
        raise
    
    
def search_books_by_query(query):
    """ Search books by a query string. """
    try:
        filters = (
            Book.title.ilike(f"%{query}%") |
            Book.author.ilike(f"%{query}%") |
            Book.description.ilike(f"%{query}%")
        )
        search_query = db.session.query(Book).filter(filters)
        books = search_query.all()
        books_data = [book.as_dict() for book in books]
        return books_data
    
    except Exception as e:
        logging.error(f"Error while searching books by query: {str(e)}")
        raise
    
    
def list_favorite_books(user_id):
    """ Fetch all favorite books for a user. """
    try:
        favorite_books = db.session.execute(
            db.select(Book)
            .join(Favorite, Favorite.book_id == Book.id)
            .where(Favorite.user_id == user_id)
        ).scalars().all()
        
        return [book.as_dict() for book in favorite_books]
    
    except Exception as e:
        logging.error(f"Error while fetching favorite books: {str(e)}")
        raise
    
    
def add_book_to_favorites(user_id, book_id):
    """ Add book to user's favorites. """
    try:
        new_favorite = Favorite(user_id, book_id)
        db.session.add(new_favorite)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while adding book to favorites: {str(e)}")
        raise
    
    
def remove_favorite_book(user_id, book_id):
    """ Remove a book from the user's favorites. """
    try:
        favorite_book = Favorite.query.filter_by(user_id=user_id, book_id=book_id).first()
        if not favorite_book:
            return False
        
        db.session.delete(favorite_book)
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while removing favorite book: {str(e)}")
        raise