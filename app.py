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
    username = session.get('user')
    is_admin = session.get('is_admin')
    return render_template('dashboard.html', books=books, username=username, is_admin=is_admin)


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
            session['user'] = user.username
            session['email'] = user.email
            session['is_admin'] = user.is_admin
            login_user(user)
            flash('Logged in successfully.')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('welcome_user')

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


@app.route('/view_books', methods=['GET'])
@login_required
def books():
    books = Book.query.all()
    is_admin = session.get('is_admin')
    return render_template('books.html', books=books, is_admin=is_admin)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    username = session.get('user')
    email = session.get('email')
    is_admin = session.get('is_admin')
    return render_template('profile.html', username=username, is_admin=is_admin, email=email)


@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = RegistrationForm(is_update=True)

    username = session.get('user')
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('welcome_user'))

    if request.method == 'GET':  # Populate form only on GET request
        form.email.data = user.email
        form.username.data = user.username

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data)

        db.session.commit()
        session['user'] = user.username
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))

    form.email.data = user.email
    form.username.data = user.username
    return render_template('edit_profile.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
