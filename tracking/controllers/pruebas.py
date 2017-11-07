# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from openerp.http import Response
from .odooclient import client
import json
import time

_logger = logging.getLogger(__name__)
lista=[]
xl =dict()
pwd_admin='pascualadmin'
class naye(http.Controller):
    @http.route('/naye', type='http',auth='none', methods=['POST'], website=True,csrf = False)
    def index(self, **post):
        _logger.info('CONNECTION SUCCESSFUL')
        _logger.info(post)
        name = post.get('name', False)
        email = post.get('email', False)
        _logger.info(name)
        _logger.info(email)
        if  name is False:
            Response.status = '400 Bad Request'
        else:
            datos = {
                'usuario': name
            }
            data_json=json.dumps(datos)
            if __name__ == '__main__':
                r = request(url='/nayeli', json=data_json)
        return '{"response": "OK"}'


    @http.route('/nayeli', type='http', auth='none', methods=['POST'], website=True, csrf=False)
    def index2(self, **args):
        print(Response.response(url='/nayeli'))

        return args