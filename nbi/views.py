from flask import render_template
from nbi import nbi_blueprint
from projects_base.base.forms import TagsSearchForm
from projects.models import Project
from nbi.conf import config


@nbi_blueprint.route('/')
@nbi_blueprint.route('/nbi_projects', methods=['GET'])
def projects():
    form = TagsSearchForm()
    entities = Project.get_all()
    tags = Project.get_top_with('tags', num=10)
    return render_template('nbi/projects.html',
                           title=config.get('PROJECTS', 'title'),
                           grid_header="{} {}".format(
                               config.get('PROJECTS', 'title'), "Projects"),
                           tags=list(tags.keys()),
                           objects=entities, form=form)
