#!/usr/bin/python3
""" Index """
from flask import Flask, jsonify, request
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=["GET"], strict_slashes=False)
def hello():
    """Hello"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=["GET"])
def stats():
    """Storage Stats"""
    classes = {"Amenity": "amenities", "City": "cities", "State": "states",
               "Place": "places", "Review": "reviews", "User": "users"}
    response = {}
    for key, value in classes.items():
        response[value] = storage.count(key)
    return jsonify(response)
