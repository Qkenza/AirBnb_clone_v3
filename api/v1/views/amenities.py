#!/usr/bin/python3
"""define module states that handles all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from api.v1.views import app_views


@app_views.route('/api/v1/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """get all amenities object"""
    all_amenities = storage.all(Amenity).values()
    new_list = []
    for amenity in all_amenities:
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route('/api/v1/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    """get amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/api/v1/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """delete state from engine storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """update amenities from engine storage"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    data = request.get_json()
    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/api/v1/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update amenity by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at ', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
