from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from db import db

main = Blueprint('main', __name__)

@main.route('/')
#@login_required
async def main_route():
    return render_template('index.html', user=current_user)
