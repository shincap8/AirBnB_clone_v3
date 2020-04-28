#!/usr/bin/python3
""" Amenity """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET", "POST"],
                 strict_slashes=False)
def list_users():
    """ Users' list """
    if request.method == "GET":
        users = storage.all("User")
        users_dict = []
        for user in users.values():
            users_dict.append(user.to_dict())
        return jsonify(users_dict)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "email" not in data:
            abort(400, "Missing email")
        if "password" not in data:
            abort(400, "Missing password")
        new_user = User(**data)
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def user(user_id):
    """ User """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.method == "GET":
        return jsonify(user.to_dict())
    if request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and key != "email" and hasattr(user, key):
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
