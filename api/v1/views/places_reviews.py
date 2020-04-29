#!/usr/bin/python3
""" Reviews """
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"],
                 strict_slashes=False)
def list_reviews(place_id):
    """ Reviews' list """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        reviews = storage.all("Review")
        reviews_dict = []
        for review in reviews.values():
            if reviews.place_id == place_id:
                reviews_dict.append(reviews.to_dict())
        return jsonify(cities_dict)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "user_id" not in data:
            abort(400, "Missing user_id")
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        if "text" not in data:
            abort(400, "Missing text")
        data["place_id"] = place_id
        new_review = Review(**data)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"],
                 strict_slashes=False)
def review(review_id):
    """ Review """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    if request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at"\
             and key != "user_id" and key != "place_id"\
             and hasattr(review, key):
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
