from datetime import datetime
from datetime import timedelta
from datetime import timezone

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
)
from flask import jsonify


from challenge.model import UserModel, TokenBlocklist
from challenge.resource.schemas import UserSchema
from lib.access_level_decorator import admin_required

blp = Blueprint("users", __name__, description="Operation on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="Username already exists")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        user.save()
        return {"message": "User created successfully."}, 201


@blp.route("/users/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        user.delete()
        return {"message": "User deleted"}, 200


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(
                identity=user.id,
                fresh=True,
                additional_claims={"is_administrator": True},
            )
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(401, message="invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(
            identity=current_user,
            fresh=False,
            additional_claims={"is_administrator": True},
        )
        return {"access_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @admin_required()
    def post(self):
        jti = get_jwt()["jti"]
        now = datetime.now(timezone.utc)
        TokenBlocklist(jti=jti, created_at=now).save()
        return jsonify(msg="JWT revoked")
