# -*- coding: utf-8 -*-

##Copied without change from flask_restplus
## copy was required so I have access to the Apidoc class
## a downside to the copy is I now have to import my own templates and static

from __future__ import unicode_literals

from flask import url_for, Blueprint, render_template


class Apidoc(Blueprint):
    '''
    Allow to know if the blueprint has already been registered
    until https://github.com/mitsuhiko/flask/pull/1301 is merged
    '''
    def __init__(self, *args, **kwargs):
        self.registered = False
        super(Apidoc, self).__init__(*args, **kwargs)

    def register(self, *args, **kwargs):
        super(Apidoc, self).register(*args, **kwargs)
        self.registered = True


apidoc = Apidoc('restplus_doc', __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/swaggerui',
)


@apidoc.add_app_template_global
def swagger_static(filename):
    return url_for('restplus_doc.static', filename=filename)


def ui_for(api):
    '''Render a SwaggerUI for a given API'''
    return render_template('swagger-ui.html', title=api.title,
                           specs_url=api.specs_url)
