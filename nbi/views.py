from flask import render_template, request
from flask_login import login_required, current_user
from nbi import nbi_blueprint
from projects_base.base.forms import TagsSearchForm
from projects.models import Project
from nbi.forms import NBIProjectForm
from nbi.conf import config


@nbi_blueprint.route('/')
@nbi_blueprint.route('/projects/', defaults={'attr': None}, methods=['GET'])
@nbi_blueprint.route('/projects/<attr>', methods=['GET'])
def projects(attr):
    area_choices = NBIProjectForm.area.kwargs.get('choices')
    areas = [area for category_id, area in area_choices]
    form = TagsSearchForm()
    if not attr:
        entities = Project.get_all()
    else:
        entities = Project.get_with_attr('area', attr)
    tags = Project.get_top_with('tags', num=10)
    return render_template('nbi/projects.html',
                           title=config.get('PROJECTS', 'title'),
                           grid_header="{}".format(
                               config.get('PROJECTS', 'title')),
                           tags=list(tags.keys()),
                           areas=areas, objects=entities, form=form)


@nbi_blueprint.route('/projects/', defaults={'attr': None}, methods=['POST'])
@nbi_blueprint.route('/projects/<attr>/<value>', methods=['POST'])
def projects(attr, value):
    area_choices = NBIProjectForm.area.kwargs.get('choices')
    areas = [area for category_id, area in area_choices]
    form = TagsSearchForm()
    entities = Project.get_with_search('area', attr)
    tags = Project.get_top_with('tags', entities, num=10)
    return render_template('nbi/projects.html',
                           title=config.get('PROJECTS', 'title'),
                           grid_header="{}".format(
                               config.get('PROJECTS', 'title')),
                           tags=list(tags.keys()),
                           areas=areas, objects=entities, form=form)


@nbi_blueprint.route('/my_projects', methods=['GET'])
@login_required
def my_projects():
    area_choices = NBIProjectForm.area.kwargs.get('choices')
    areas = [area for category_id, area in area_choices]
    form = TagsSearchForm()
    entities = [project for project in Project.get_all()
                if project._id in current_user.projects]
    return render_template('nbi/projects.html', areas=areas,
                           objects=entities, form=form)
