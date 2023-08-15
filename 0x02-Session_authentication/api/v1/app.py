#!/usr/bin/env python3
"""
these is a route for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None


if os.environ.get('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request():
    """
    request to check for authentication and authorization.
    """
    if not auth:
        return
    paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    request.current_user = auth.current_user(request)

    if not auth.require_auth(request.path, paths):
        return

    if not auth.authorization_header(request):
        abort(401)

    if not request.current_user:
        abort(403)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler whene no resource is located
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorized request handler which return jsonify error
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Forbidden handler which return jsonify error
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)