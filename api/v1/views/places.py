#!/usr/bin/python3
""" API actions for Place objects """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
import logging

logging.basicConfig(level=logging.DEBUG)


@app_views.route(
        '/cities/<city_id>/places',
        methods=['GET'],
        strict_slashes=False)
def get_places(city_id):
    """ Retrieves the list of all Place objects of a City """
    logging.debug(f"Retrieving places for city_id: {city_id}")
    city = storage.get(City, city_id)
    if not city:
        logging.error("City not found")
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Retrieves a Place object """
    logging.debug(f"Retrieving place with place_id: {place_id}")
    place = storage.get(Place, place_id)
    if not place:
        logging.error("Place not found")
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    logging.debug(f"Deleting place with place_id: {place_id}")
    place = storage.get(Place, place_id)
    if not place:
        logging.error("Place not found")
        abort(404)
    place.delete()
    storage.save()
    logging.debug(f"Place with place_id: {place_id} deleted successfully")
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    Creates a new place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)  # No valid user
    data['city_id'] = city_id
    place = Place(**data)
    storage.save()
    place_json = place.to_dict()
    return jsonify(place_json), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a specific place by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    if not request.is_json:
        abort(400, description="Not a JSON")
    
    data = request.get_json()

    if not data:
        # Retrieve all Place objects if the JSON body is empty
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []

    if states or cities:
        # Retrieve all places for given states
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
        
        # Retrieve all places for given cities
        for city_id in cities:
            city = storage.get(City, city_id)
            if city and city not in [c.id for c in places]:  # Avoid duplicates
                places.extend(city.places)
    else:
        # Retrieve all places if no states or cities are provided
        places = storage.all(Place).values()

    # Filter places by amenities if provided
    if amenities:
        places = [place for place in places if all(amenity_id in [amenity.id for amenity in place.amenities] for amenity_id in amenities)]

    # Convert to dict
    place_list = [place.to_dict() for place in places]

    return jsonify(place_list)

