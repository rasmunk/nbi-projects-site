from os import urandom
from projects import app, mail
from projects.models import Project, User
from projects.forms import ProjectForm, AuthRequestForm, LoginForm, PasswordResetForm
from nbi_base.forms import TagsSearchForm
from flask import render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from projects.helpers import generate_confirmation_token, confirm_token
from bcrypt import hashpw
import datetime


# Routes
@app.route("/")
@app.route("/projects", methods=['GET'])
def projects():
    form = TagsSearchForm()
    objects = Project.get_all()
    return render_template('projects.html', objects=objects, form=form)


@app.route('/show/<id>', methods=['GET'])
def show(id):
    form = ProjectForm()
    object = Project.get(id)
    owner = False
    if owner:
        for attr in object.__dict__:
            if attr != '_id':
                form[attr].data = object.__dict__[attr]

    return render_template('project.html', object=object, owner=owner, form=form)


@app.route('/create_project', methods=['GET', 'POST'])
@login_required
def create():
    form = ProjectForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit():
        f = form.image.data
        filename = str(secure_filename(f.filename))
        f.save(app.config['UPLOAD_FOLDER'] + "/" + filename)

        project_data = {key: field.data for key, field in form.__dict__.items() if
                        hasattr(field, 'data') and key != 'csrf_token' and key != 'image'}
        project_data['image'] = filename
        project = Project(**project_data)
        project.save()
        url = url_for('show', id=project._id, _external=True)
        flash("Your submission has been received, your metadata can be found at: " + url, 'success')
        return redirect(url)
    return render_template('create_project.html', form=form)


@app.route('/update/<id>', methods=['POST'])
@login_required
def update(id):
    object = Project.get(id)
    form = ProjectForm(CombinedMultiDict((request.files, request.form)))
    if form.validate_on_submit() and object is not None:
        for attr in object.__dict__:
            if attr != '_id':
                object.__dict__[attr] = form[attr].data

        object.save()
        url = url_for('show', id=object._id, _external=True)
        flash("Update Success, your data can be found at: " + url, 'success')
        return redirect(url)
    return render_template('project.html', object=object, form=form)


# Sends approval emails to every app.config['ADMINS']
@app.route('/request_auth', methods=['POST'])
def request_auth():
    form = AuthRequestForm(request.form)
    if form.validate_on_submit():
        # Send confirmation token
        if User.get_with_first('email', form.email.data) is None:
            token = generate_confirmation_token(email=form.email.data)
            confirm_url = url_for('approve_auth', token=token, _external=True)
            html = render_template('email/activate_user.html', email=form.email.data, confirm_url=confirm_url)
            msg = Message(subject=form.email.data + " requests eScience Projects access", html=html,
                          recipients=app.config['ADMINS'], sender=app.config['MAIL_USERNAME'])
            mail.send(msg)
            return jsonify(data={'success': 'Request successfully submitted, awaiting admin approval'})
        else:
            response = jsonify(data={'danger': 'That email has already been granted access'})
            response.status_code = 400
            return response
    response = jsonify(data={'error': form.errors})
    response.status_code = 400
    return response


# Accepts approval from admin's
@app.route('/approve_auth/<token>')
def approve_auth(token):
    email = confirm_token(token)
    if email is False:
        flash('Confirmation failed, either it is invalid or expired.', 'danger')
    else:
        user = User.get_with_first('email', email)
        if user is not None:
            flash('That email has already been registered')
        else:
            # Setup
            user = User(email=email, password=hashpw(urandom(24), bytes(app.config['SECURITY_PASSWORD_SALT'], 'utf-8')),
                        is_active=False, is_authenticated=False, is_anonymous=False, confirmed_on=datetime.datetime.now())
            user.save()

            token = generate_confirmation_token(email=email)
            reset_url = url_for('reset_password', token=token, _external=True)
            html = render_template('email/reset_password.html', email=email, reset_password_url=reset_url)
            msg = Message(subject='eScience Projects Account approval', html=html, recipients=[email],
                          sender=app.config['MAIL_USERNAME'])
            mail.send(msg)
            flash("The account: " + email + " has been approved and created", 'success')
    return redirect(url_for('projects'))


@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    email = confirm_token(token)
    if email is False:
        flash('Attempted password reset failed, the request is either invalid or expired', 'danger')
    else:
        form = PasswordResetForm(request.form)
        form.email.data = email
        if form.validate_on_submit():
            user = User.get_with_first('email', email)
            user.is_active = True
            user.is_authenticated = True
            user.is_anonymous = False
            user.email = email
            user.password = hashpw(bytes(form.password.data, 'utf-8'),
                                   bytes(app.config['SECURITY_PASSWORD_SALT'], 'utf-8'))
            user.save()
            flash('Your password has now been updated')
            return redirect(url_for('projects', _external=True))
        return render_template('reset_password_form.html', form=form)
    return redirect(url_for('projects', _external=True))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        valid_user = User.valid_user(form.email.data, form.password.data)
        if valid_user is not None:
            flash('Logged in successfully.', 'success')
            login_user(valid_user)
        else:
            flash('Invalid Credentials', 'danger')
        return redirect(url_for('projects', _external=True))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('projects'))


## TODO -> refactor with fair search forms in common views instead.
@app.route('/search', methods=['GET'])
def tag_external_search():
    form = TagsSearchForm(request.args, csrf_enabled=False)
    objects = {}
    # The return form should contain a csrf_token
    return_form = TagsSearchForm()
    return_form.tag = form.tag
    if form.validate():
        objects = Project.get_with_search('tags', form.tag.data)
        return render_template('projects.html', objects=objects, form=return_form)
    return render_template('projects.html', objects=objects, form=return_form, error=form.errors)


## TODO -> refactor with fair search forms in common views instead.
@app.route('/search', methods=['POST'])
def tag_native_search():
    form = TagsSearchForm(request.form)
    if form.validate_on_submit():
        result = {}
        tag = request.form['tag']
        tag_matches = Project.get_with_search('tags', tag)
        if len(tag_matches) > 0:
            result = [object.serialize() for object in tag_matches]
        return jsonify(data=result)

    response = jsonify(data=form.errors)
    response.status_code = 400
    return response


@app.route('/static/<filename>')
def projects_static(filename):
    return send_from_directory(app.config['PROJECTS_STATIC_FOLDER'], filename)


@app.route('/static/images/<filename>')
def projects_images(filename):
    return send_from_directory(app.config['PROJECTS_STATIC_FOLDER'] + "/images/", filename)
