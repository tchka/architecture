from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: template name
    :param folder: template folder
    :param kwargs: template params
    :return:
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    tmpl = env.get_template(template_name)
    return tmpl.render(**kwargs)
