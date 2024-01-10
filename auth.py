from flask import Blueprint, jsonify, url_for, redirect, render_template, request, flash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt, create_refresh_token
from flask_login import login_user, login_required, logout_user, current_user
from db import db
from models import User, RefreshTokenTable
import argon2
import uuid
import time

ph = argon2.PasswordHasher()

auth = Blueprint('auth', __name__)

@auth.get('/login')
async def login():
    return render_template('login.html')

@auth.get('/logout')
@login_required
async def logout():
    logout_user()
    return redirect(url_for('main.main_route'))

# TODO: Make Expiring Refresh Tokens

@auth.get('/token')
@login_required
async def token_show():
    email = current_user.email
    token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    rt_obj = RefreshTokenTable(
            id=str(uuid.uuid4()),
            token = refresh_token,
            timestamp = time.time()
        )
    db.session.add(rt_obj)
    db.session.commit()
    return jsonify(access_token=token, refresh_token=refresh_token), 200

@auth.post('/refresh')
@jwt_required(refresh=True)
async def refresh():
    current_user = get_jwt_identity()
    token = request.form.get('refresh_token')
    rt_obj = RefreshTokenTable.query.filter_by(token=token).first()
    if rt_obj == None: return jsonify('Refresh Token Expired'), 403
    rtoken = create_refresh_token(identity=current_user)
    rt = RefreshTokenTable(id=str(uuid.uuid4()), token=rtoken, timestamp=time.time())
    db.session.delete(rt_obj)
    db.session.add(rt)
    db.session.commit()
    ret = {
        'access_token': create_access_token(identity=current_user),
        'refresh_token': rtoken
    }
    return jsonify(ret), 200

@auth.get('/protected')
@jwt_required()
def protected():
    username = get_jwt_identity()
    return jsonify(logged_in_as=username), 200

@auth.post('/login')
async def login_logic():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('User Does not Exist')
        return rediect(url_for('auth.login'))
    try:
        pres = ph.verify(user.password, password)
    except argon2.exceptions.VerifyMismatchError:
        pres = False
    if not pres:
        flash('Incorrect Password')
        return redirect(url_for('auth.login'))
    login_user(user)
    return redirect(url_for('main.main_route'))

@auth.post('/register')
async def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    password_hash = ph.hash(password)
    id = str(uuid.uuid4())
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Error: User Exists')
        return redirect(url_for('auth.login'))
    new_user = User(id=id, email=email, name=name, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    flash('User Created Successfully')
    return redirect(url_for('auth.login'))
