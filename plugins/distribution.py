# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

import pkg_resources
import os, yaml, json
from flask import Blueprint
from flask_appbuilder import expose, BaseView as AppBuilderBaseView

# Importing base classes that we need to derive
from airflow.hooks.base import BaseHook
from airflow.providers.amazon.aws.transfers.gcs_to_s3 import GCSToS3Operator

# Will show up in Connections screen in a future version
class PluginHook(BaseHook):
    pass


# Will show up under airflow.macros.test_plugin.plugin_macro
# and in templates through {{ macros.test_plugin.plugin_macro }}
def plugin_macro():
    pass


# Creating a flask blueprint to integrate the templates and static folder
bp = Blueprint(
    "test_plugin",
    __name__,
    template_folder="templates",  # registers airflow/plugins/templates as a Jinja template folder
    static_folder="static",
    static_url_path="/static/test_plugin",
)

def extended_make_tree(path):
    tree = dict(name=os.path.basename(path), children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(extended_make_tree(fn))
            else:
                with open(fn, "r") as stream:
                    try:
                        yaml_object = yaml.safe_load(stream)
                        pipeline = json.dumps(yaml_object, indent=2, sort_keys=True, default=str)
                        tree['children'].append(dict(name=name, pipeline=yaml_object))
                    except yaml.YAMLError as exc:
                        print(exc)
    return tree

# Creating a flask admin BaseView
class Infrastructure(AppBuilderBaseView):
    default_view = "test"

    @expose('/')
    def test(self):
        dists = [str(d) for d in pkg_resources.working_set]
        # in this example, put your test_plugin/test.html template at airflow/plugins/templates/test_plugin/test.html
        return self.render_template("distribution.html", dists=dists)

class DagsTree(AppBuilderBaseView):
    default_view = "test"
    
    @expose('/')
    def test(self):
        path = os.path.expanduser(u'/opt/airflow/dags/pipelines')
        tree = extended_make_tree(path)
        # in this example, put your test_plugin/test.html template at airflow/plugins/templates/test_plugin/test.html
        return self.render_template("dirtree.html", tree=tree)

# Creating a flask appbuilder BaseView
class TestAppBuilderBaseNoMenuView(AppBuilderBaseView):
    default_view = "test"

    @expose("/")
    def test(self):
        return self.render_template("test_plugin/test.html", content="Hello galaxy!")


v_appbuilder_view = Infrastructure()
v_appbuilder_package = {
    "name": "python packages",
    "category": "Infrastructure",
    "view": v_appbuilder_view,
}

v_appbuilder_view_infra_dags_tree = DagsTree()
v_appbuilder_package_infra_dags_tree = {
    "name": "Dags Tree",
    "category": "Infrastructure",
    "view": v_appbuilder_view_infra_dags_tree,
}

# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "test_plugin"
    hooks = [PluginHook]
    macros = [plugin_macro]
    flask_blueprints = [bp]
    appbuilder_views = [v_appbuilder_package, v_appbuilder_package_infra_dags_tree]