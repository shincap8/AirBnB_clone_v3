#!/usr/bin/python3
""" Amenity """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET", "POST"],
                 strict_slashes=False)
def list_amenities():
    """ Amenities' list """
    if request.method == "GET":
        amenities = storage.all("Amenity")
        amenities_dict = []
        for amenity in amenities.values():
            amenities_dict.append(amenity.to_dict())
        return jsonify(amenities_dict)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.method == "GET":
        return jsonify(amenity.to_dict())
    if request.method == "DELETE":
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
                    and hasattr(amenity, key):
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
