from flask import Blueprint, request, jsonify
from models.models import Users, users_schema, user_schema, db
from middleware.admin_middleware import token_required

admin_route = Blueprint('admin_route', __name__, url_prefix='/admin')


@admin_route.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"message": "You do not have admin privileges to access this route"})

    users = Users.query.all()
    result = users_schema.dump(users)
    return jsonify(result)


# Grant admin permission to user
@admin_route.route('/user/<user_id>', methods=['PUT'])
def admin_verify(user_id):
    user = Users.query.get(user_id)

    if not user:
        return jsonify({"msg": "User does not exist"})
    else:
        user.admin = True
        db.session.commit()
        return user_schema.jsonify(user)

