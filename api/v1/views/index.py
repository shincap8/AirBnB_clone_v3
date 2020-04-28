#!/usr/bin/python3
from flask import Flask, jsonify, request
from api.v1.views import app_views


@app_views.route('/status', methods=["GET"])
def hello():
    return jsonify({"status": "OK"})
