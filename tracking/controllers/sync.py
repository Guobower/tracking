# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from . import login
import json
import time
from .odooclient import client
import werkzeug
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wrappers
_logger = logging.getLogger(__name__)

def login(self, usuario):
    return usuario
class nayeController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #localhost:8069/naye?n=1


    @http.route('/naye', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        r = request.httprequest
        response = werkzeug.utils.redirect('/', 302)
        response = r.app.get_response(r, response, explicit_session=False)
        werkzeug.exceptions.abort(response)
        return response

    @http.route('/to', type='http', auth="none", methods=['GET'])
    def sync(self, **kw):
        print(request.session)
        return kw.get('amor')

    @http.route('/efren', type='http', auth="none")
    def efren(self, s_action=None, db=None, **kw):
        self.sync(self,request.params)

    @http.route('/xmarts', type='http', auth='public', methods=['POST'], website=True,csrf = False)
    def callback(self, **post):
        print(post)
        x = post.get('p')
        return "hola soy naye"+x
