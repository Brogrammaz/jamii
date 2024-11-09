import bcrypt
from flask import make_response, request, jsonify

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def response_with_error(errors, status_code):
    """
    Create a formatted JSON response for errors.
    """
    return make_response(jsonify({"errors": errors}), status_code)

def validate_request_json(expected_keys):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({"msg": "Missing JSON in request"}), 400
            data = request.get_json()
            missing_keys = [key for key in expected_keys if key not in data]
            if missing_keys:
                return jsonify({"msg": f"Missing keys in request JSON: {', '.join(missing_keys)}"}), 400
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

def response_with_error(message, status_code):
    response = jsonify({"msg": message})
    response.status_code = status_code
    return response