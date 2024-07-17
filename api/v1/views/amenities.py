# #!/usr/bin/python3
# """
# Creates a new view for Amenity objects that handles all default RESTFul API actions
# """

# from flask import jsonify, request, abort
# from models import storage
# from api.v1.views import app_views


# @app_views.route('/amenities', methods=['GET'], strict_slashes=False)
# def get_all_amenities():
#     """Retrieves the list of all Amenity objects"""
#     all_amenities = storage.all('Amenity').values()
#     return jsonify([amenity.to_dict() for amenity in all_amenities])


# @app_views.route('/amenities/<amenity_id>',
#                  methods=['GET'], strict_slashes=False)
# def get_amenity(amenity_id):
#     """Retrieves a Amenity object"""
#     amenity = storage.get('Amenity', amenity_id)
#     if amenity is None:
#         abort(404)
#     return jsonify(amenity.to_dict())


# @app_views.route('/amenities/<amenity_id>',
#                  methods=['DELETE'], strict_slashes=False)
# def delete_amenity(amenity_id):
#     """Deletes a Amenity object"""
#     amenity = storage.get('Amenity', amenity_id)
#     if amenity is None:
#         abort(404)
#     storage.delete(amenity)
#     return jsonify({}), 200


# @app_views.route('/amenities', methods=['POST'], strict_slashes=False)
# def create_amenity():
#     """Creates a Amenity"""
#     data = request.get_json()
#     if data is None:
#         abort(400, description='Not a JSON')
#     if 'name' not in data:
#         abort(400, description='Missing name')
#     new_amenity = storage.new('Amenity', **data)
#     storage.save()
#     return jsonify(new_amenity.to_dict()), 201


# @app_views.route('/amenities/<amenity_id>',
#                  methods=['PUT'], strict_slashes=False)
# def update_amenity(amenity_id):
#     """Updates a Amenity object"""
#     amenity = storage.get('Amenity', amenity_id)
#     if amenity is None:
#         abort(404)
#     data = request.get_json()
#     if data is None:
#         abort(400, description='Not a JSON')
#     for key, value in data.items():
#         if key not in ['id', 'created_at', 'updated_at']:
#             setattr(amenity, key, value)
#     storage.save()
#     return jsonify(amenity.to_dict()), 200

#!/usr/bin/python3
"""
This file contains the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ get amenities by id """
    all_list = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ delete amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_obj_amenity():
    """ create new instance """
    if not request.is_json:
        return (jsonify({"error": "Not a JSON"}), 400)
    data = request.get_json()
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def post_amenity(amenity_id):
    """  """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
