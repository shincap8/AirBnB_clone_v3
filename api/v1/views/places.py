#!/usr/bin/python3
""" Places """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=["GET", "POST"],
                 strict_slashes=False)
def list_places(city_id):
    """ Places' list """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        places = storage.all("Place")
        places_dict = []
        for place in places.values():
            if place.city_id == city_id:
                places_dict.append(place.to_dict())
        return jsonify(places_dict)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        user = storage.get("User", data["user_id"])
        if user is None:
            abort(404)
        if "name" not in data:
            abort(400, "Missing name")
        data["city_id"] = city_id
        new_place = Place(**data)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def place(place_id):
    """ Place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        return jsonify(place.to_dict())
    if request.method == "DELETE":
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and key != "city_id" and key != "user_id"\
                    and hasattr(place, key):
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
