from datetime import datetime
from flask import Blueprint, jsonify, request
from app.models import Article, User
from flask_login import current_user, login_required
from app.routes.auth import auth_bp, forms
from app.models import db
from app.models import DBOperations

@auth_bp.route('/author/name', methods=['POST'])
@login_required
def set_author_name():
    """
    Update author display name
    Methods:
        POST: Modify author's public-facing name
    Form Data:
        authorName (str): New display name
    Security:
        - Requires valid login session
    Returns:
        - 200: JSON with updated settings
        - 400: Form validation errors
        - 401: Database update failure
    Process:
        1. Validate rename form submission
        2. Retrieve current user context
        3. Attempt database update via DBOperations
        4. Handle success/failure responses
    Validation:
        - Form field: authorName (frontend) mapped to authorname (database)
        - Server-side validation bypassed in current implementation
    Error Handling:
        - Returns form errors under 'new_name' field key
        - Captures database operation exceptions
    """
    form = forms.RenameForm()
    if True or form.validate():
        user = User.query.filter_by(id=current_user.id).first()
        print("call set_author_name():", form.authorName.data)
        result, msg = DBOperations.update_user_settings(user.id, {"authorname": form.authorName.data})
        if result:
            return jsonify({"objects": result}), 200
        else:
            print("rename failed: ", msg)
            return jsonify({"message": msg}), 401
    else:
        errors = form.errors.get("new_name", [])
        print(errors)
        return jsonify({"status": "error", "errors": errors}), 400
