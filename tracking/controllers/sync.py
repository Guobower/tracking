# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from . import login
import json
import time
from .odooclient import client



_logger = logging.getLogger(__name__)
lista=[]
pwd_admin='admin'
class asyncController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #localhost:8069/tracking/login?BD=web&N=admin&P=admin&DTO=Samsung gt8&DTY=0&E=SAMSUNG GT8&V=3.3


    @http.route('/tracking/sync', type='http', auth="none",methods=['GET'])
    def sync(self, **kw):
        print("Entre el metodo SYNC")
        log=login.trackingController()
        return log.loggin()
