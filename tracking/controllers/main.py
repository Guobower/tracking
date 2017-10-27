# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from .odooclient import client
import json
import time

_logger = logging.getLogger(__name__)
lista=[]
pwd_admin='admin'
class trackController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #localhost:8069/track/login?BD=web&N=admin&P=admin&DTO=Samsung gt8&DTY=0&E=SAMSUNG GT8&V=3.3


    @http.route('/track/login', type='http', auth="none",methods=['GET'])
    def loginlxtrack(self, **kw):
        print(request.params)
        if 'BD' in request.params and 'N' in request.params and 'P' in request.params:
            odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=request.params['BD'], port=8069,
                                 debug=True)
            odoo.ServerInfo()
            print("hola")
            odoo.Authenticate('admin', 'admin')
            # print(odoo.Authenticate(request.params['N'], request.params['P']))
            if odoo.IsAuthenticated() is True:
                db = request.params['BD']
                pwd = request.params['P']
                user = request.params['N']
                employee_user = odoo.SearchCount('hr.employee',
                                                 [('active', '=', True), ('name', '=', user), ('password', '=', pwd)])
                if employee_user == 0:
                    return '{"​ error​ ":"DATA"}'
                else:
                    lista.append(db)
                    lista.append(user)
                    lista.append(pwd)
                    employee = odoo.SearchRead('hr.employee',
                                               [('active', '=', True), ('name', '=', user), ('password', '=', pwd)],
                                               ['id', 'name'])
                    for e in employee:
                        print(str(e['name']))
                        json_exitoso = {
                            'resultado': {
                                "id_usuario": str(e['id']),
                                "nombre_usuario": str(e['name']),
                                "id_session_app": "1",
                                "rastreo_frecuencia": "15",
                                "rastreo_hora_inicio": time.strftime("%H:%M:%S"),
                                "rastreo_hora_termino​":time.strftime("%H:%M:%S"),
                                "rastreo_lunes": "1",
                                "rastreo_martes": "1",
                                "rastreo_miercoles": "1",
                                "rastreo_jueves": "1",
                                "rastreo_viernes": "1",
                                "rastreo_sabado": "1",
                                "rastreo_domingo": "1",
                                "abrir_candado_posicion_manual": "11",
                                "abrir_candado_logout": "",
                                "abrir_candado_gastos_ordenes": "",
                                "abrir_candado_gastos_generales": "",
                                "abrir_candado_eliminar_xml_local_gastos": "",
                                "abrir_candado_impresion": "1",
                                "abrir_candado_autorizar_cliente": "1",
                                "abrir_candado_modulo_alta_ordenes": "1",
                                "abrir_candado_modulo_alta_clientes": "1",
                                "abrir_candado_gps_obligatorio": "1",
                                "incluir_catalogo": "1",
                                "limite_size_fotos": "320",
                                "limite_size_fotos_layout": "320",
                                "abrir_candado_datos_obligatorios": "1"
                            }
                        }
                    return json.dumps(json_exitoso)

            else:
                return '{"​ error​ ":"DB"}'
        else:
            return '{"​ error​ ": "INVALID"}'

    @http.route('/track/SYNC', type='http', auth='none', methods=['GET'])
    def track_web(self, debug=False, **k):
        print(lista[0])
        print(lista[1])
        print(lista[2])
        print('CAT_CL' in request.params)
        print(lista)

        odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=lista[0], port=8069, debug=True)
        odoo.ServerInfo()
        odoo.Authenticate('admin', pwd_admin)
        if odoo.Authenticate('admin', pwd_admin) is not False or None :
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

