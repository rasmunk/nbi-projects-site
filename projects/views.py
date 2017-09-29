from projects import app
from projects.models import Project
from nbi_base.forms import TagsSearchForm
from projects.forms import ProjectForm
from flask import render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename


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
def update(id):
    object = Project.get(id)
    form = ProjectForm(CombinedMultiDict((request.files, request.form)))
    owner = False
    if owner and form.validate_on_submit() and object is not None:
        for attr in object.__dict__:
            if attr != '_id':
                object.__dict__[attr] = form[attr].data

        object.save()
        url = url_for('show', id=object._id, _external=True)
        flash("Update Success, your data can be found at: " + url, 'success')
        return redirect(url)
    return render_template('project.html', object=object, owner=owner, form=form)


## TODO -> refactor with fair search forms in common views instead.
@app.route('/search', methods=['GET'])
def tag_external_search():
    form = TagsSearchForm(request.args, csrf_enabled=False)
    objects = {}
    # The return form should contain a csrf_token
    return_form = TagsSearchForm()
    return_form.tag = form.tag
    if form.validate():
        objects = Project.get_with('tags', form.tag.data)
        return render_template('projects.html', objects=objects, form=return_form)
    return render_template('projects.html', objects=objects, form=return_form, error=form.errors)

## TODO -> refactor with fair search forms in common views instead.
@app.route('/search', methods=['POST'])
def tag_native_search():
    form = TagsSearchForm(request.form)
    if form.validate_on_submit():
        result = {}
        tag = request.form['tag']
        tag_matches = Project.get_with('tags', tag)
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