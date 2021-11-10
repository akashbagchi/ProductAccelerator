from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists', category='error')
            return redirect(url_for("auth.login"))
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) <2:
            flash('First Name must be at least 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('E-mail sent!', category='success')
            return redirect(url_for('views.home'))

    return render_template("home.html")

@views.route('/about')
def about():
    return render_template("about.html")