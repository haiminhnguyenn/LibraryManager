import logging

from app import db
from ...models.borrow_record import BorrowRecord
from ...models.user import User
from ...models.book import Book


def get_all_borrow_records_of_user(user_id):
    """ Fetch all borrow records of a user. """
    try:
        borrow_records = BorrowRecord.query.filter_by(user_id=user_id).all()
        return [record.as_dict() for record in borrow_records]
    except Exception as e:
        logging.error(f"Error while fetching all borrow records of a user: {str(e)}")
        raise
    
    
def get_borrow_record_by_id(borrow_record_id):
    """ Fetch a borrow record by its id. """
    try:
        borrow_record = BorrowRecord.query.get(borrow_record_id)
        if not borrow_record:
            return None
        return borrow_record
    except Exception as e:
        logging.error(f"Error while fetching borrow record by id: {str(e)}")
        raise
    
    
def list_borrow_records():
    """ Fetch all borrow records from the database. """
    try:
        borrow_records = BorrowRecord.query.all()
        return [record.as_dict() for record in borrow_records]
    except Exception as e:
        logging.error(f"Error while fetching all borrow records: {str(e)}")
        raise
    
    
def save_new_borrow_record(user_id, book_id, quantity, borrow_date, due_date):
    """ Save a new borrow record to the database. """
    try:
        new_borrow_record = BorrowRecord(user_id, book_id, quantity, borrow_date, due_date)
        db.session.add(new_borrow_record)
        db.session.commit()
        return new_borrow_record
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while saving new borrow record: {str(e)}")
        raise
    
    
def update_borrow_record_info(borrow_record, return_date):
    """ Update a borrow record in the database. """
    try:
        borrow_record.return_date = return_date
        if return_date <= borrow_record.due_date:
            borrow_record.status = "returned-ontime"
        else:
            borrow_record.status = "returned-late"   
        db.session.commit()
        return borrow_record
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while updating borrow record: {str(e)}")
        raise
    
    
def search_borrow_records_by_query(query):
    """ Search borrow records by a query string. """
    try:
        search_results = []
        user_filters = (
            User.name.ilike(f"%{query}%") |
            User.email.ilike(f"%{query}%")
        )
        users = db.session.query(User).filter(user_filters).all()
        if users:
            for user in users:
                borrow_records_for_user_query = BorrowRecord.query.filter_by(user_id=user.id).all()
                for record_for_user_query in borrow_records_for_user_query:
                    search_results.append(record_for_user_query.as_dict())
        
        book_filters = Book.title.ilike(f"%{query}%")
        books = db.session.query(Book).filter(book_filters).all()
        if books:
            for book in books:
                borrow_records_for_book_query = BorrowRecord.query.filter_by(book_id=book.id).all()
                for record_for_book_query in borrow_records_for_book_query:
                    search_results.append(record_for_book_query.as_dict())
                    
        return search_results

    except Exception as e:
        logging.error(f"Error while searching borrow records by query: {str(e)}")
        raise