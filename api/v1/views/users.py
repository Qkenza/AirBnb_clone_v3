#!/usr/bin/python3
"""define module users that handles all default RESTFul API actions"""
from models import storage
from models.user import User
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from api.v1.views import app_views


@app_views.route('/api/v1/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get all users object"""
    all_users = storage.all(User).values()
    new_list = []
    for user in all_users:
        new_list.append(user.to_dict())
    return jsonify(new_list)


@app_views.route('/api/v1/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user_id(user_id):
    """get user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/api/v1/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """delete user from engine storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def create_user():
    """update users from engine storage"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'email' not in request.get_json():
        abort(400, description='Missing email')
    if 'password' not in request.get_json():
        abort(400, description='Missing password')
    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/api/v1/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_users(user_id):
    """update user by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at ', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
