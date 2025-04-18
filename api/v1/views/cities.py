#!/usr/bin/python3
"""
Creates new view for City obj that handles the restful API
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves a list of all cities in certain state
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieves a specific city by its ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a specific city by its ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    Creates a new city and stores it.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    city = City(**data)
    setattr(city, 'state_id', state.id)
    storage.save()
    city_json = city.to_dict()
    return jsonify(city_json), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    Updates a specific city by its ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
