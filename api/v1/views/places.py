#!/usr/bin/python3
""" API actions for Place objects """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    print(f"Retrieving places for city_id: {city_id}")
    city = storage.get(City, city_id)
    if not city:
        print("City not found")
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    print(f"Retrieving place with place_id: {place_id}")
    place = storage.get(Place, place_id)
    if not place:
        print("Place not found")
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    print(f"Deleting place with place_id: {place_id}")
    place = storage.get(Place, place_id)
    if not place:
        print("Place not found")
        abort(404)
    place.delete()
    storage.save()
    print(f"Place {place_id} deleted successfully")
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    print(f"Creating place in city with city_id: {city_id}")
    city = storage.get(City, city_id)
    if not city:
        print("City not found")
        abort(404)
    data = request.get_json()
    if not data:
        print("Not a JSON")
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        print("Missing user_id")
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        print("User not found")
        abort(404)
    if 'name' not in data:
        print("Missing name")
        abort(400, "Missing name")

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    print(f"Place created with data: {data}")
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    print(f"Updating place with place_id: {place_id}")
    place = storage.get(Place, place_id)
    if not place:
        print("Place not found")
        abort(404)
    data = request.get_json()
    if not data:
        print("Not a JSON")
        abort(400, "Not a JSON")

    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            print(f"Updating {key} to {value}")
            setattr(place, key, value)
    place.save()
    print(f"Place {place_id} updated with data: {data}")
    return jsonify(place.to_dict()), 200
