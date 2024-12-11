from my_project import app, db
from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, login_required, logout_user
from my_project.models import User, Book
from my_project.forms import LoginForm, RegistrationForm, AddForm, DeleteForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os


@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/dashboard')
@login_required
def welcome_user():
    books = Book.query.all()
    username = session.get('username')
    return render_template('dashboard.html', books=books, username=username)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            session['username'] = user.username
            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('dashboard')

            return redirect(next)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
