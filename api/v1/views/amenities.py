#!/usr/bin/python3
"""
Creates a new view for Amenity objects that handles all default RESTFul API actions
"""

from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views

