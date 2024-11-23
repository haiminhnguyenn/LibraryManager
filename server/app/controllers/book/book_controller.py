from flask import request, jsonify

from . import book_api
from ...services.book.book_service import (
    list_books, get_book_by_id, save_new_book, update_book_info
)
from ...utils.decorators import JWT_required, admin_required


@book_api.route('/')
@JWT_required
def get_all_books():
    try:
        books_data = list_books()
        return jsonify({
            "success": True,
            "message": "Successfully fetched all books.",
            "books": books_data
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error.",
            "message": str(e)
        }), 500


@book_api.route('/<book_id>')
@JWT_required
def get_book(book_id):
    try:
        book_data = get_book_by_id(book_id)
        return jsonify({
            "success": True,
            "message": "Successfully fetched book.",
            "book": book_data
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error.",
            "message": str(e)
        }), 500
        
        
@book_api.route('/', methods=['POST'])
@JWT_required
@admin_required
def add_book():
    try:
        data = request.get_json()
        if data is None:
            raise ValueError("Invalid JSON data.")
        
        REQUIRED_FIELDS = {"title", "author", "image_url", "description", "price"}
        missing_fields = {field for field in REQUIRED_FIELDS if data.get(field) is None}
        
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
            
        new_book = save_new_book(data["title"], data["author"], data["image_url"], data["description"], data["price"])
        return jsonify({
            "success": True,
            "message": "Successfully added new book.",
            "new_book": new_book.as_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            "error": "Invalid data.",
            "message": str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error.",
            "message": str(e)
        }), 500


@book_api.route('/<book_id>', methods=['PUT'])
@JWT_required
@admin_required
def update_book(book_id):
    try:
        book = get_book_by_id(book_id)
        if not book:
            return jsonify({
                "success": False,
                "message": "Book not found."
            }), 404
            
        data = request.get_json()
        if data is None:
            raise ValueError("Invalid JSON data.")
        
        ALLOW_FIELDS = {"title", "author", "image_url", "description", "price"}
        unknown_fields = {field for field in data if field not in ALLOW_FIELDS}
        if unknown_fields:
            return jsonify({
                "success": False,
                "message": f"Unknown fields: {', '.join(unknown_fields)}"
            }), 400
            
        updated_book = update_book_info(book, data)
        return jsonify({
            "success": True,
            "message": "Successfully updated book.",
            "updated_book": updated_book.as_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            "error": "Invalid data.",
            "message": str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            "error": "Internal server error.",
            "message": str(e)
        }), 500