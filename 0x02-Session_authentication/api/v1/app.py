#!/usr/bin/env python3
"""
the app file
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
AUTH_TYPE = os.getenv("AUTH_TYPE")


if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

if AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def checker():
    """
    doc doc doc
    """
    if auth is None:
        pass
    req_auth = auth.require_auth(request.path,
                                 ['/api/v1/status/',
                                  '/api/v1/unauthorized/',
                                  '/api/v1/forbidden/'])
    if req_auth is True:
        pass

    if auth.authorization_header(request) is None:
        abort(401, description="Unauthorized")
    if auth.current_user(request) is None:
        abort(403, description="Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """ handeling not found
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error) -> str:
    """_not_allowed handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
