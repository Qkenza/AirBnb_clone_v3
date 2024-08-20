#!/usr/bin/python3
"""define module states that handles all default RESTFul API actions"""
from models import storage
from models.state import State
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from api.v1.views import app_views


# app = Flask(__name__)
# app_views = Blueprint('app_views', __name__)


@app_views.route('/api/v1/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states object"""
    all_states = storage.all(State).values()
    new_list = []
    for state in all_states:
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route('/api/v1/states/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """get state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete state from engine storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/states', methods=['POST'], strict_slashes=False)
def create_state():
    """update state from engine storage"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/api/v1/states/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at ', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
