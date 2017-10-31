# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from .odooclient import client
import json
import time
import logging
import xmlrpc.client
import xmlrpc.server

_logger = logging.getLogger(__name__)
lista=[]
pwd_admin='admin'
class trackingController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #localhost:8069/tracking/login?BD=embotella&N=admin&P=admin&DTO=Samsung gt8&DTY=0&E=SAMSUNG GT8&V=3.3

    @http.route('/tracking/login', type='http', auth="none",methods=['GET'])
    def loggin(self, redirect=None,**kw):
        #################### DIRECCION CLIENTES############################
        fecha_cld = str(request.params['CAT_CLD']) + '.0'
        partnercld_ids = partner_model.search([('write_date', '>=', fecha_cld)])
        contcld = str(len(partnercld_ids))
        datacld = str(request.params['CAT_CLD'] + ' ' + contcld)
        if partnercld_ids:
            insertclientecld = ""
            print(partnercld_ids)
            for pcl in partnercld_ids:
                print("valor de fecha clientes direcciones" + p.write_date)
                if str(pcl.active) == False:
                    activodir = 0
                else:
                    activodir = 1
                if pcl.parent_id:
                    pclid = pcl.parent_id.id
                else:
                    pclid = pcl.id
                insertclientecld = insertclientecld + "INSERT OR REPLACE INTO cliente_direccion(id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES((select  id from cliente_direccion where id_servidor ='" + str(
                    pcl.id) + "'),'" + str(pcl.id) + "', (select id from cliente where id_servidor ='" + str(
                    pclid) + "'),'" + str(pclid) + "','" + str(pcl.type) + "','" + str(
                    pcl.street) + "',''," + "'','" + str(pcl.city) + "','" + str(pcl.state_id.id) + "','" + str(
                    pcl.zip) + "','" + str(pcl.country_id.id) + "','','" + str(pcl.email) + "','" + str(
                    pcl.phone) + "','" + str(pcl.mobile) + "','','" + str(activodir) + "');"

            valscld = {
                datacld: insertclientecld
            }
        #####################PRODUCTOS###########################
        product_model = request.env['product.template']
        fechap_inicio = str(request.params['CAT_P']) + '.0'
        product_ids = product_model.search([('write_date', '>=', fechap_inicio)])
        contp = str(len(product_ids))
        dataproduct = str(request.params['CAT_P'] + ' ' + contp)
        if product_ids:
            insertproduct = ""
            print(product_ids)
            for pr in product_ids:
                print("valor de fecha product" + pr.write_date)
                if str(pr.active) == False:
                    activoproduct = 0
                else:
                    activoproduct = 1
                insertproduct = insertproduct + "INSERT OR REPLACE INTO producto(id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES('" + str(
                    pr.id) + "','" + str(pr.default_code) + "','" + str(pr.name) + "','" + str(
                    pr.description) + "','" + str(pr.list_price) + "','" + str(pr.uom_id.name) + "', '" + str(
                    activoproduct) + "');"
            valsproduct = {
                dataproduct: insertproduct
            }
        #####################Estados###########################
        estado_model = request.env['res.country.state']
        fechastate_inicio = str(request.params['CAT_ES']) + '.0'
        state_ids = estado_model.search([('write_date', '>=', fechastate_inicio)])
        contstate = str(len(state_ids))
        datastate = str(request.params['CAT_ES'] + ' ' + contstate)
        if state_ids:
            insertstate = ""
            print(state_ids)
            for state in state_ids:
                # print("valor de fecha state" + pr.write_date)
                insertstate = insertstate + "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES('" + str(
                    state.id) + "','" + str(state.country_id.id) + "','" + str(state.name) + "','" + str(True) + "');"

            valsstate = {
                datastate: insertstate
            }
        #####################Paises###########################
        # paises_model = request.env['res.country']
        # fechapaises_inicio = str(request.params['CAT_PA']) + '.0'
        # paises_ids = estado_model.search([('write_date', '>=', fechapaises_inicio)])
        # contpaises = str(len(state_ids))
        # datapaises= str(request.params['CAT_PA'] + ' ' + contpaises)
        # if paises_ids:
        #    insertpaises = ""
        #    for pais in paises_ids:
        #        print("valor de fecha pais" + pr.write_date)
        #        insertpaises = insertpaises + "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES(" + str(pais.id) +",'" + str(pais.name) + "'," + str(True) + ");"

        #    valspaises = {
        #        datapaises: insertpaises
        #    }

        # json_list['paises'].append(valspaises)
        return request.params['BD'],request.params['P'],request.params['N']








