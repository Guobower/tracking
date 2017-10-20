# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from .odooclient import client
import json

_logger = logging.getLogger(__name__)
lista=[]
class trackController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #localhost:8069/track/login?BD=odoo11&N=admin&P=admin


    @http.route('/track/login', type='http', auth="none",methods=['GET'])
    def loginlxtrack(self, **kw):
        odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=request.params['BD'], port=8069, debug=True)
        odoo.ServerInfo()
        odoo.Authenticate(request.params['N'], request.params['P'])
        print(odoo.Authenticate(request.params['N'], request.params['P']))
        if odoo.Authenticate(request.params['N'], request.params['P']) is not False:
            db = request.params['BD']
            pwd = request.params['P']
            user = request.params['N']
            lista.append(db)
            lista.append(user)
            lista.append(pwd)
            return http.local_redirect('/track/SYNC', keep_hash=True)
        else:
            return "ERRROR"
        return 0

    @http.route('/track/SYNC', type='http', auth='none', methods=['GET'])
    def track_web(self, debug=False, **k):
        print(lista[0])
        print(lista[1])
        print(lista[2])
        print('CAT_CL' in request.params)

        odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=lista[0], port=8069, debug=True)
        odoo.ServerInfo()
        odoo.Authenticate(lista[1], lista[2])
        print(odoo.Authenticate(lista[1], lista[2]))
        if odoo.Authenticate(lista[1], lista[2]) is not False or None :
            json_list = {
                'clientes': [],
                'clientes_dirs': [],
                'productos': [],
                'estados': [],
            }
            valsproduct = {}
            vals = {}
            valscld = {}
            valsstate = {}
            valspaises = {}
            insertcliente = ''
            ####################CLIENTES#####################################
            if 'CAT_CL' in request.params:
                fecha_inicio = request.params['CAT_CL'] + '.0'
                print("fecha inicio %s" % fecha_inicio)
                cont = odoo.SearchCount('res.partner',
                                        [('write_date', '>=', fecha_inicio)])

                partners = odoo.SearchRead('res.partner',[('write_date', '>=', fecha_inicio)],
                                            ['name', 'display_name', 'website', 'function', 'phone', 'mobile', 'email', 'active'])
                data = str(request.params['CAT_CL'] + ' ' )+str(cont)

                for p in partners:
                    if str(p['active']) == False:
                        activo = 0
                    else:
                        activo = 1

                    insertcliente = insertcliente  + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES((select id from cliente where id_servidor='" + str(p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(p['display_name']) + "','" + str(p['website']) + "','" + str(p['function']) + "','" + str(p['phone']) + "','" + str(p['mobile']) + "','','" + str(p['email']) + "','"+str(1)+"','" + str(activo) + "');"
                vals = {
                    data: insertcliente
                }

            else:
                cont = odoo.SearchCount('res.partner',[])

                partners = odoo.SearchRead('res.partner', [],
                                           ['name', 'display_name', 'website', 'function', 'phone', 'mobile', 'email',
                                            'active'])
                data = str(cont)

                for p in partners:
                    if str(p['active']) == False:
                        activo = 0
                    else:
                        activo = 1

                    insertcliente = insertcliente + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES((select id from cliente where id_servidor='" + str(p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(p['display_name']) + "','" + str(p['website']) + "','" + str(p['function']) + "','" + str(p['phone']) + "','" + str(p['mobile']) + "','','" + str(p['email']) + "','" + str(1) + "','" + str(activo) + "');"
                vals = {
                    data: insertcliente
                }

            json_list['clientes'].append(vals)
            json_list['clientes_dirs'].append(valscld)
            json_list['productos'].append(valsproduct)
            json_list['estados'].append(valsstate)
            # json_list['paises'].append(valspaises)
        return json.dumps(json_list)

