from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from db import db

main = Blueprint('main', __name__)

@main.route('/')
#@login_required
async def main_route():
    return jsonify({
        'status': 'Working',
        'user': {
            'name': current_user.name if not current_user.is_anonymous else 'Anonymous'
        }
    })
