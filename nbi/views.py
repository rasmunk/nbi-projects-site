from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from nbi import nbi_blueprint, csrf
from projects_base.base.forms import TagsSearchForm
from projects.models import Project
from nbi.forms import NBIProjectForm, NBIProjectSearchForm
from nbi.conf import config


@nbi_blueprint.route('/')
@nbi_blueprint.route('/projects', methods=['GET'])
def projects():
    area_choices = NBIProjectForm.area.kwargs.get('choices')
    form = TagsSearchForm()
    entities = Project.get_all()
    tags = Project.get_top_with('tags')
    return render_template('nbi/projects.html',
                           title=config.get('PROJECTS', 'title'),
                           grid_header="{}".format(
                               config.get('PROJECTS', 'title')),
                           tags=list(tags.keys()),
                           areas=area_choices, objects=entities, form=form)


@nbi_blueprint.route('/projects', methods=['POST'])
def projects_post():
    form = NBIProjectSearchForm(request.form)
    if form.validate():
        if form.__contains__('csrf_token'):
            form._fields.pop('csrf_token')
        projects = Project.get_all()
        for key, value in form.data.items():
            if value:
                # Reduce dataset by attribute values
                projects = Project.get_with_attr(key, value,
                                                 collection=projects)
        entities = [entity.serialize() for entity in projects]
        return jsonify(data={'projects': entities})

    response = jsonify(data={'danger': ', '.join(
        [msg for attr, errors in form.errors.items() for msg in errors])})
    response.status_code = 400
    return response


@nbi_blueprint.route('/my_projects', methods=['GET'])
@login_required
def my_projects():
    area_choices = NBIProjectForm.area.kwargs.get('choices')
    form = TagsSearchForm()
    entities = [project for project in Project.get_all()
                if project._id in current_user.projects]
    return render_template('nbi/projects.html',
                           title=config.get('PROJECTS', 'title'),
                           grid_header="{}".format(
                               config.get('PROJECTS', 'title')),
                           areas=area_choices, objects=entities, form=form)


@nbi_blueprint.route('/tag/<tag>', methods=['GET'])
def tag_search(tag):
    area_choices = NBIProjectForm.area.kwargs.get('choices')
    form = TagsSearchForm(data={'tag': tag}, csrf_enabled=False)
    entities = {}
    tags = Project.get_top_with('tags')
    if form.validate():
        entities = Project.get_with_search('tags', form.tag.data)

    # Create new form that has csrf -> enable that tag searches can be done
    # via the returned form
    form = TagsSearchForm(data={'tag': tag})
    return render_template('nbi/projects.html',
                           title=config.get('PROJECTS', 'title'),
                           grid_header="{}".format(
                               config.get('PROJECTS', 'title')),
                           tags=list(tags.keys()),
                           areas=area_choices, objects=entities, form=form)
