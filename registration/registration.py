from flask import Blueprint, request, jsonify, make_response
from flask_bcrypt import Bcrypt
from flask import current_app as app
from models.models import db as main_db, Users, user_schema
import jwt
import datetime
register = Blueprint('register', __name__,)

bcrypt = Bcrypt()


@register.route('/register', methods=['POST'])
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


@register.route('/login', methods=['POST'])
def login():

   user_name = request.json['user_name']
   password = request.json['password']

   if not user_name or not password:
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login Required'})
   user = Users.query.filter_by(user_name= user_name).first()

   if not user:
        return jsonify({"message": "user does not exist"})

   if bcrypt.check_password_hash(user.user_password, password):
        token = jwt.encode(
            {'user_name': user.user_name, 'admin': user.admin, 'exp': datetime.datetime.utcnow() +
             datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

   return jsonify({"message": "invalid credentials"})
