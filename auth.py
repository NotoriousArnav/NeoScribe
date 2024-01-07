from flask import Blueprint, jsonify, url_for, redirect, render_template, request, flash
from flask_login import login_user, login_required, logout_user
from db import db
from models import User
import argon2
import uuid

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
    
    return redirect(url_for('auth.login'))
