from datetime import datetime

from flask import request, jsonify
from flasgger.utils import swag_from

from . import borrowing_api
from ...services.borrowing.borrowing_service import BorrowingService
from ...services.user.user_service import UserService
from ...services.book.book_service import BookService
from ...utils.decorators import JWT_required, admin_required

 
@borrowing_api.route("/borrowing", methods=["GET"])
@JWT_required
@admin_required
@swag_from("../../apidocs/borrowing/get_all_borrow_records.yaml", endpoint="borrowing_api.get_all_borrow_records", methods=["GET"])
def get_all_borrow_records(user):
    borrowing_service = BorrowingService()
    borrow_records = borrowing_service.list_borrow_records()  
    return jsonify({
        "success": True,
        "message": "Successfully fetched all borrow records.",
        "borrow_records": borrow_records
    }), 200
        

@borrowing_api.route("/user/<id>/borrowing", methods=["GET"])
@JWT_required
@swag_from("../../apidocs/borrowing/list_borrow_records_of_user.yaml", endpoint="borrowing_api.list_borrow_records_of_user", methods=["GET"])
def list_borrow_records_of_user(user, id):
    if user.role != "admin" and user.id != id:
        return jsonify({
            "success": False,
            "message": "You are not authorized to access this resource."
        }), 403
        
    user_service = UserService()
    target_user = user_service.get_user_byId(id)
    if not target_user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    if user_service.is_admin(target_user):
        return jsonify({
            "success": False,
            "message": "Admins cannot borrow books."
        }), 400

    borrowing_service = BorrowingService()
    borrow_records = borrowing_service.get_all_borrow_records_of_user(id)
    return jsonify({
        "success": True,
        "message": "Successfully fetched all borrow records of the user.",
        "user_id": id,
        "borrow_records": borrow_records
    }), 200
        
          
@borrowing_api.route("/borrowing", methods=["POST"])
@JWT_required
@admin_required
@swag_from("../../apidocs/borrowing/create_borrow_record.yaml", endpoint="borrowing_api.create_borrow_record", methods=["POST"])
def create_borrow_record(user):
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON data."
        }), 400
    
    REQUIRED_FIELDS = {"user_id", "book_id", "quantity", "borrow_date", "due_date"}
    missing_fields = {field for field in REQUIRED_FIELDS if data.get(field) is None}
    if missing_fields:
        return jsonify({
            "error": "Missing required fields.",
            "message": f"Missing fields: {missing_fields}"
        }), 400
        
    user_service = UserService()
    target_user = user_service.get_user_byId(data["user_id"])
    if not target_user:
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404
    
    if user_service.is_admin(target_user):
        return jsonify({
            "success": False,
            "message": "Admins cannot borrow books."
        }), 400

    borrowing_service = BorrowingService()
    new_borrow_record = borrowing_service.save_new_borrow_record(data["user_id"], data["book_id"], data["quantity"], data["borrow_date"], data["due_date"])
    if not new_borrow_record:
        return jsonify({
            "success": False,
            "message": "Book not found."
        }), 404

    return jsonify({
        "success": True,
        "message": "Successfully saved new borrow record.",
        "borrow_record": new_borrow_record.as_dict()
    }), 201


@borrowing_api.route("/borrowing/<borrow_record_id>/return", methods=["PUT"])
@JWT_required
@admin_required
@swag_from("../../apidocs/borrowing/update_borrow_record.yaml", endpoint="borrowing_api.update_borrow_record", methods=["PUT"])
def update_borrow_record(user, borrow_record_id):
    borrowing_service = BorrowingService()
    borrow_record = borrowing_service.get_borrow_record_by_id(borrow_record_id)
    if not borrow_record:
        return jsonify({
            "success": False,
            "message": "Borrow record not found"
        }), 404
        
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid JSON data."
        }), 400
    
    return_date = data.get("return_date")
    if not return_date:
        return jsonify({
            "success": False,
            "message": "Missing field: return_date"
        }), 400
        
    try:
        return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid return_date format. Expected format: 'YYYY-MM-DD'"
        }), 400
    
    updated_borrow_record = borrowing_service.update_borrow_record_info(borrow_record, return_date)
    return jsonify({
        "success": True,
        "message": "Successfully updated return date for borrow record.",
        "updated_borrow_record": updated_borrow_record.as_dict()
    }), 200
        
        
@borrowing_api.route("/borrowing/search", methods=["GET"])
@JWT_required
@admin_required
@swag_from("../../apidocs/borrowing/search_borrow_records.yaml", endpoint="borrowing_api.search_borrow_records", methods=["GET"])
def search_borrow_records(user):
    query = request.args.get("query", type=str, default=None)
    if not query:
        return jsonify({
            "success": False,
            "message": "Missing query parameter."
        }), 400
    
    borrowing_service = BorrowingService()
    borrow_record_search_results = borrowing_service.search_borrow_records_by_query(query)
    return jsonify({
        "success": True,
        "message": "Search completed successfully.",
        "total": len(borrow_record_search_results),
        "borrow_records": borrow_record_search_results
    }), 200
