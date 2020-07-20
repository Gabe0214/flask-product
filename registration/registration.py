from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask import current_app as app
from models.models import db as main_db, Users, user_schema

register = Blueprint('register', __name__,)

bcrypt = Bcrypt()


@register.route('/', methods=['POST'])
def registration():
    user_name = request.json['user_name']
    user_email = request.json['user_email']
    user_password = request.json['user_password']
    admin = False
    pw_hash = bcrypt.generate_password_hash(user_password)

    new_user = Users(user_name, user_email, pw_hash, admin)

    main_db.session.add(new_user)
    main_db.session.commit()
    return user_schema.jsonify(new_user)
