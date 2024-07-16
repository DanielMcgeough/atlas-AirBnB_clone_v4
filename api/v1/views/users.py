#!/usr/bin/python3

"""
Creates a new view for User object that handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    all_users = storage.all('User').values()
    return jsonify([user.to_dict() for user in all_users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200

