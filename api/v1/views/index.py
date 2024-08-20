#!/usr/bin/python3
"""Index file to connect to API."""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/api/v1/stats', strict_slashes=False)
def get_stats():
    """Retrive the number of each object by type."""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)


@app_views.route('/api/v1/status', strict_slashes=False)
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})
