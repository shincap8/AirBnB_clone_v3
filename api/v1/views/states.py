#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET", "POST"], strict_slashes=False)
def list_states():
    """list states"""
    if request.method == "GET":
        states = storage.all("State")
        states_dict = []
        for state in states.values():
            states_dict.append(state.to_dict())
        return jsonify(states_dict)
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        if "name" not in data:
            abort(400, "Missing name")
        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["GET", "DELETE", "PUT"], strict_slashes=False)
def state(state_id):
    """State"""
    state = storage.get("State", state_id)
    if state is None:
        abort (404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        storage.delete(state)
        storage.save()
        return jsonify({})
    if request.method == "PUT":
        data = request.get_json()
        if data is None:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key != "id" and key != "created_at" and key != "updated_at" and hasattr(state, key):
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
