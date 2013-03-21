# -*- coding: utf-8 -*-
from jinja2 import Environment
from jinja2 import PackageLoader


def render_template(template_name, **env):
    env = Environment(loader=PackageLoader('dopplerganger', 'templates'))
    template = env.get_template(template_name)

    return template.render(**env)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
