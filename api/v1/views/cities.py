#!/usr/bin/python3
""" Cities """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET", "POST"],
                 strict_slashes=False)
def list_cities(state_id):
    """ Cities's list """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == "GET":
        cities = storage.all("City")
        cities_dict = []
        for city in cities.values():
            if city.state_id == state_id:
                cities_dict.append(city.to_dict())
        return jsonify(cities_dict)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        data["state_id"] = state_id
        new_city = City(**data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def city(city_id):
    """ City """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
             and key != "state_id" and hasattr(city, key):
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
