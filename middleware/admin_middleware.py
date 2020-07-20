from flask import jsonify, request

from models.models import Users
import jwt
from functools import wraps
from settings import DevelopmentConfig
# Token middle-ware

secret = DevelopmentConfig.SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "token is missing"})
        try:
            data = jwt.decode(token, secret)
            current_user = Users.query.filter_by(user_name=data['user_name']).first()
        except:
                return jsonify({"message":"token is invalid"}), 401
        return f(current_user, *args, **kwargs)
    return decorated
