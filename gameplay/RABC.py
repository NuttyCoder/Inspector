from functools import wraps
from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample user roles (In practice, this would be fetched from a database)
users = {
    'admin': {'role': 'admin'},
    'user1': {'role': 'user'}
}

def requires_role(role):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = request.args.get('user')
            if user in users and users
