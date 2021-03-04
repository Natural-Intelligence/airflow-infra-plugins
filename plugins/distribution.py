# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin
import os
from flask import Blueprint
from flask_admin import BaseView, expose
import pkg_resources

def make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(make_tree(fn))
            else:
                tree['children'].append(dict(name=name))
    return tree

def get_python_packages():
    dists = [str(d) for d in pkg_resources.working_set]
    return dists

# Creating a flask admin BaseView
class distribution(BaseView):

    @expose('/')
    def test(self):
        dists = get_python_packages()
        # in this example, put your test_plugin/test.html template at airflow/plugins/templates/test_plugin/test.html
        return self.render("distribution.html", dists=dists)
distribution = distribution(category="Infrastructure", name="Distribution List")

bp = Blueprint(
    "infrastructure_plugin", __name__,
    template_folder='templates', # registers airflow/plugins/templates as a Jinja template folder
    static_folder='static',
    static_url_path='/static/test_plugin')

class dags(BaseView):

    @expose('/')
    def test(self):
        path = os.path.expanduser(u'/opt/airflow/dags')
        tree = make_tree(path)
        # in this example, put your test_plugin/test.html template at airflow/plugins/templates/test_plugin/test.html
        return self.render("dirtree.html", tree=tree)
dags = dags(category="Infrastructure", name="Tree List")

# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "infrastructure_plugin"
    admin_views = [distribution, dags]
    flask_blueprints = [bp]