# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from .odooclient import client
import json
import time
from datetime import datetime



_logger = logging.getLogger(__name__)
lista=[]
xl =dict()
pwd_admin='pascualadmin'
class trackController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #http://localhost:8069/track/SYNC?CAT_CL=2017-10-13%2016:47:55&CAT_CLD=2017-10-10%2016:47:55&CAT_P=2017-10-13%2016:47:55&CAT_ES=2017-10-13%2016:47:55&CAT_PA=2017-10-13%2016:47:55&CAT_PLP=2017-10-13%2016:47:55&CAT_TA=2017-10-13%2016:47:55&CAT_PLP=2017-10-13%2016:47:55&CAT_CUB=2017-10-13%2016:47:55&CAT_PPRE=2017-10-13%2016:47:55
    #localhost:8069/track/login?BD=web&N=admin&P=admin&DTO=Samsung gt8&DTY=0&E=SAMSUNG GT8&V=3.3


    @http.route('/track/login',type='http', auth='public', methods=['POST'], website=True,csrf = False)
    def loginlxtrack(self, **post):
        print(request.session.uid)
        if 'BD' in post and 'N' in post and 'P' in post:
            print("entro aqui")
            odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=post.get('BD'), port=8069,debug=True)
            odoo.ServerInfo()
            print("hola")
            uid= odoo.Authenticate('admin', pwd_admin)
            # print(odoo.Authenticate(request.params['N'], request.params['P']))
            if odoo.IsAuthenticated() is True:
                db = post.get('BD')
                pwd = post.get('P')
                user = post.get('N')
                xl.update(post)
                print("valor de xl")
                print(xl)
                employee_user = odoo.SearchCount('hr.employee',
                                                 [('active', '=', True), ('name', '=', user), ('password', '=', pwd)])
                if employee_user == 0:
                    return '{"error​":"DATA"}'
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
                                "id_session_app": time.strftime("%H%M%S"),
                                "rastreo_frecuencia": "15",
                                "rastreo_hora_inicio": "07:00",
                                "rastreo_hora_termino":"17:00",
                                "rastreo_lunes": "1",
                                "rastreo_martes": "1",
                                "rastreo_miercoles": "1",
                                "rastreo_jueves": "1",
                                "rastreo_viernes": "1",
                                "rastreo_sabado": "1",
                                "rastreo_domingo": "1",
                                "abrir_candado_posicion_manual": "1",
                                "abrir_candado_logout": "1",
                                "abrir_candado_gastos_ordenes": "1",
                                "abrir_candado_gastos_generales": "1",
                                "abrir_candado_eliminar_xml_local_gastos": "1",
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
                return '{"error":"DB"}'
        else:
            return '{"error": "INVALID"}'

    @http.route('/track/sync', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def track_web(self, **post):
        print("valor sync")
        print(lista)
        odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=xl.get('BD'), port=8069, debug=True)
        odoo.ServerInfo()
        odoo.Authenticate('admin', pwd_admin)
        if odoo.Authenticate('admin', pwd_admin) is not False or None:
            json_datos = {
                'datos': [],
            }
            valsproduct = {}
            vals = {}
            valscld = {}
            valsstate = {}
            valspaises = {}
            valstarifa = {}
            valsplp = {}
            valsmep = {}
            valscub = {}
            valsppre = {}
            valsmo = {}
            valsordenes = {}
            valsorden = {}
            listacliente = []
            listadirecciones = []
            listaproductos = []
            listastate = []
            listapais = []
            listatarifa = []
            listaplp = []
            listamep = []
            listacub = []
            listappre = []
            listamo = []
            insertcliente = ''
            insertcliente_cld = ''
            insertproduct = ''
            insertstate = ''
            insertpais = ''
            inserttarifa = ''
            insertplp = ''
            insertmep = ''
            insertcub = ''
            insertppre = ''
            insertmo = ''
            print(post)
            if 'CAT_CL' in post or 'CAT_CLD' in post or 'CAT_P' in post or 'CAT_ES' in post \
                    or 'CAT_PA' in post or 'CAT_TA' in post or 'CAT_PLP' in post or 'CAT_CUB' in post \
                    or 'CAT_PPRE' in post or 'CAT_MO' in post:
                ####################CLIENTES#####################################
                if post.get('CAT_CL') is None or post.get('CAT_CL') == '':
                    cont = odoo.SearchCount('res.partner',[])
                    print("valor total de registor "+ str(cont))
                    partners = odoo.SearchRead('res.partner', [],
                                               ['name', 'display_name', 'website', 'function', 'phone', 'mobile','email','active'])
                    partnersmx = odoo.SearchRead('res.partner', [],['id', 'write_date'])
                    v1 = True
                    maxpartner = ''
                    for part in partnersmx:
                        if v1 == True:
                            maxpartner = part['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v1 = False
                        else:
                            if part['write_date'] > maxpartner:
                                maxpartner = part['write_date']

                    print("valor maximo de fecha")
                    print(maxpartner)
                    contmax = odoo.SearchCount('res.partner',
                                               [('write_date', '>=', str(maxpartner) + '.0'),
                                                ('write_date', '<=', str(maxpartner) + '.99')])
                    print("contador maximo")
                    print(contmax)
                    new_cat_cl = str(maxpartner) + ' ' + str(contmax)
                    print(new_cat_cl)
                    data = str(post.get('CAT_CL') + ' ') + str(cont)
                    if cont > 0:
                        print("entro al if ")
                        for p in partners:
                            if str(p['active']) == False:
                                activo = 0
                            else:
                                activo = 1
                            if (p['website']) == False: p['website'] = ''
                            if (p['function']) == False: p['function'] = ''
                            if (p['phone']) == False: p['phone'] = ''
                            if (p['mobile']) == False: p['mobile'] = ''
                            if (p['email']) == False: p['email'] = ''

                            insertcliente = "INSERT OR REPLACE INTO cliente (id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES ((select id from cliente where id_servidor='" + str(
                                p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(
                                p['display_name']) + "','" + str(p['website']) + "','" + str(
                                p['function']) + "','" + str(
                                p['phone']) + "','" + str(p['mobile']) + "','','" + str(p['email']) + "','" + str(
                                1) + "','" + str(activo) + "')"
                            listacliente.append(insertcliente)
                        vals = {
                            'update': 'true',
                            'db_clientes_last_mod_date_count': new_cat_cl,
                            'qrys': listacliente
                        }
                    else:
                        print("entro al else")
                        vals = {
                            'update': 'false'
                        }
                else:
                    print("entro al else clientes")
                    if len(post.get('CAT_CL')) > 19:
                        d=post.get('CAT_CL')[0:19]
                        fecha_inicio=d + '.0'
                        print(fecha_inicio)
                        partnersmx = odoo.SearchRead('res.partner', [],
                                                    ['id', 'write_date'])
                        v1 = True
                        maxpartner = ''
                        for part in partnersmx:
                            if v1 == True:
                                maxpartner = part['write_date']
                                #datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v1 = False
                            else:
                                if part['write_date'] > maxpartner:
                                    maxpartner = part['write_date']

                        print("valor maximo de fecha")
                        print(maxpartner)
                        contmax = odoo.SearchCount('res.partner',
                                                [('write_date', '>=', str(maxpartner)+'.0'),('write_date', '<=', str(maxpartner)+'.99')])
                        print("contador maximo")
                        print(contmax)
                        new_cat_cl = str(maxpartner) + ' ' + str(contmax)
                        print(new_cat_cl)
                        if new_cat_cl != post.get('CAT_CL'):
                            cont = odoo.SearchCount('res.partner',
                                                    [('write_date', '>=', fecha_inicio)])
                            partners = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio)],
                                                       ['name', 'display_name', 'website', 'function', 'phone',
                                                        'mobile', 'email',
                                                        'active'])
                            data = str(post.get('CAT_CL') + ' ') + str(cont)
                            if cont > 0:
                                print("entro al if ")
                                for p in partners:
                                    if str(p['active']) == False:
                                        activo = 0
                                    else:
                                        activo = 1
                                    if (p['website']) == False: p['website'] = ''
                                    if (p['function']) == False: p['function'] = ''
                                    if (p['phone']) == False: p['phone'] = ''
                                    if (p['mobile']) == False: p['mobile'] = ''
                                    if (p['email']) == False: p['email'] = ''

                                    insertcliente = "INSERT OR REPLACE INTO cliente (id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES ((select id from cliente where id_servidor='" + str(
                                        p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(
                                        p['display_name']) + "','" + str(p['website']) + "','" + str(
                                        p['function']) + "','" + str(
                                        p['phone']) + "','" + str(p['mobile']) + "','','" + str(
                                        p['email']) + "','" + str(
                                        1) + "','" + str(activo) + "')"
                                    listacliente.append(insertcliente)
                                vals = {
                                    'update': 'true',
                                    'db_clientes_last_mod_date_count': new_cat_cl,
                                    'qrys': listacliente
                                }
                            else:
                                print("entro al else")
                                vals = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            vals = {
                                'update': 'false'
                            }

                    else:
                        fecha_inicio = post.get('CAT_CL') + '.0'
                        print("fecha inicio  clientes %s" % fecha_inicio)
                        cont = odoo.SearchCount('res.partner',
                                                [('write_date', '>=', fecha_inicio)])
                        print("contador cliente")
                        print(cont)

                        partners = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio)],
                                                   ['name', 'display_name', 'website', 'function', 'phone', 'mobile', 'email',
                                                    'active'])
                        data = str(post.get('CAT_CL') + ' ') + str(cont)
                        partners = odoo.SearchRead('res.partner', [],
                                                   ['name', 'display_name', 'website', 'function', 'phone', 'mobile',
                                                    'email', 'active'])
                        partnersmx = odoo.SearchRead('res.partner', [], ['id', 'write_date'])
                        v1 = True
                        maxpartner = ''
                        for part in partnersmx:
                            if v1 == True:
                                maxpartner = part['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v1 = False
                            else:
                                if part['write_date'] > maxpartner:
                                    maxpartner = part['write_date']

                        print("valor maximo de fecha")
                        print(maxpartner)
                        contmax = odoo.SearchCount('res.partner',
                                                   [('write_date', '>=', str(maxpartner) + '.0'),
                                                    ('write_date', '<=', str(maxpartner) + '.99')])
                        print("contador maximo")
                        print(contmax)
                        new_cat_cl = str(maxpartner) + ' ' + str(contmax)
                        print(new_cat_cl)
                        if cont > 0:
                            print("entro al if ")
                            for p in partners:
                                if str(p['active']) == False:
                                    activo = 0
                                else:
                                    activo = 1
                                if (p['website']) == False: p['website']=''
                                if (p['function']) == False: p['function'] = ''
                                if (p['phone']) == False: p['phone'] = ''
                                if (p['mobile']) == False: p['mobile'] = ''
                                if (p['email']) == False: p['email'] = ''

                                insertcliente = "INSERT OR REPLACE INTO cliente (id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES ((select id from cliente where id_servidor='" + str(
                                    p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(
                                    p['display_name']) + "','" + str(p['website']) + "','" + str(p['function']) + "','" + str(
                                    p['phone']) + "','" + str(p['mobile']) + "','','" + str(p['email']) + "','" + str(
                                    1) + "','" + str(activo) + "')"
                                listacliente.append(insertcliente)
                            vals = {
                                'update': 'true',
                                'db_clientes_last_mod_date_count': new_cat_cl,
                                'qrys': listacliente
                            }
                        else:
                            print("entro al else")
                            vals = {
                                'update': 'false'
                            }

                #################### DIRECCION CLIENTES############################
                if post.get('CAT_CLD') is None or post.get('CAT_CLD') == '':
                    contcld = odoo.SearchCount('res.partner',[])
                    print("entro al vacio")

                    partners_cld = odoo.SearchRead('res.partner', [],
                                                   ['id', 'type', 'street', 'city', 'state_id', 'zip', 'country_id',
                                                    'email', 'phone', 'mobile', 'parent_id'])
                    partnerscldmx = odoo.SearchRead('res.partner', [], ['id', 'write_date'])
                    v2 = True
                    maxpartnercld = ''
                    for partcld in partnerscldmx:
                        if v2 == True:
                            maxpartnercld = partcld['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v2 = False
                        else:
                            if partcld['write_date'] > maxpartnercld:
                                maxpartnercld = partcld['write_date']

                    print("valor maximo de fecha de clientes direecciones")
                    print(maxpartnercld)
                    contmaxcld = odoo.SearchCount('res.partner',
                                               [('write_date', '>=', str(maxpartnercld) + '.0'),
                                                ('write_date', '<=', str(maxpartnercld) + '.99')])
                    print("contador maximo cld")
                    print(contmaxcld)
                    new_cat_cld = str(maxpartnercld) + ' ' + str(contmaxcld)
                    print(new_cat_cld)
                    data_cld = str(post.get('CAT_CLD') + ' ') + str(contcld)
                    if contcld > 0:
                        for pcl in partners_cld:
                            activo_cld = 1
                            estado = ''
                            pais = ''
                            if pcl['parent_id']:
                                pclid = pcl['parent_id']
                            else:
                                pclid = pcl['id']
                            if pcl['type'] == 'delivery': pcl['type'] = 'E'
                            if pcl['type'] == 'invoice': pcl['type'] = 'F'
                            if (pcl['type']) == False: pcl['type'] = ''
                            if (pcl['street']) == False: pcl['street'] = ''
                            if (pcl['city']) == False: pcl['city'] = ''
                            if (pcl['state_id']) == False:
                                pcl['state_id'] = ''
                                estado = ''
                            if (pcl['zip']) == False: pcl['zip'] = ''
                            if (pcl['country_id']) == False:
                                pcl['country_id'] = ''
                                pais = ''
                            if (pcl['email']) == False: pcl['email'] = ''
                            if (pcl['phone']) == False: pcl['phone'] = ''
                            if (pcl['mobile']) == False: pcl['mobile'] = ''
                            if pcl['state_id'] is not '':
                                valor = True
                                for i in pcl['state_id']:
                                    if valor == True:
                                        estado = i
                                        valor = False
                            if pcl['country_id'] is not '':
                                valor2 = True
                                for a in pcl['country_id']:
                                    if valor2 == True:
                                        pais = a
                                        valor2 = False
                            insertcliente_cld = "INSERT OR REPLACE INTO cliente_direccion (id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES ((select  id from cliente_direccion where id_servidor ='" + str(
                                pcl['id']) + "'),'" + str(
                                pcl['id']) + "', (select id from cliente where id_servidor ='" + str(
                                pclid) + "'),'" + str(
                                pclid) + "','" + str(pcl['type']) + "','" + str(pcl['street']) + "',''," + "'','" + str(
                                pcl['city']) + "','" + str(estado) + "','" + str(pcl['zip']) + "','" + str(
                                pais) + "','','" + str(pcl['email']) + "','" + str(
                                pcl['phone']) + "','" + str(
                                pcl['mobile']) + "','','" + str(activo_cld) + "')"
                            listadirecciones.append(insertcliente_cld)
                        valscld = {
                            'update': 'true',
                            'db_clientes_dirs_last_mod_date_count': new_cat_cld,
                            'qrys': listadirecciones
                        }

                    else:
                        print("entro al else")
                        valscld = {
                            'update': 'false'
                        }
                else:
                    print("entro al else clientesdirecciones")
                    if len(post.get('CAT_CLD')) > 19:
                        d = post.get('CAT_CLD')[0:19]
                        fecha_inicio_cld = d + '.0'
                        print(fecha_inicio_cld)

                        partnerscldmx = odoo.SearchRead('res.partner', [], ['id', 'write_date'])
                        v2 = True
                        maxpartnercld = ''
                        for partcld in partnerscldmx:
                            if v2 == True:
                                maxpartnercld = partcld['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v2 = False
                            else:
                                if partcld['write_date'] > maxpartnercld:
                                    maxpartnercld = partcld['write_date']

                        print("valor maximo de fecha de clientes direecciones")
                        print(maxpartnercld)
                        contmaxcld = odoo.SearchCount('res.partner',
                                                      [('write_date', '>=', str(maxpartnercld) + '.0'),
                                                       ('write_date', '<=', str(maxpartnercld) + '.99')])
                        print("contador maximo cld")
                        print(contmaxcld)
                        new_cat_cld = str(maxpartnercld) + ' ' + str(contmaxcld)
                        print("entorrrrrrooooo aquiiiiii en cld correcto")
                        print(new_cat_cld)
                        print(post.get('CAT_CLD'))
                        print(new_cat_cld != post.get('CAT_CLD'))
                        print("hola")


                        if new_cat_cld != post.get('CAT_CLD'):
                            print("fecha inicio cld %s" % fecha_inicio_cld)

                            contcld = odoo.SearchCount('res.partner',
                                                       [('write_date', '>=', fecha_inicio_cld)])

                            partners_cld = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio_cld)],
                                                           ['id', 'type', 'street', 'city', 'state_id', 'zip', 'country_id',
                                                            'email', 'phone', 'mobile', 'parent_id'])
                            data_cld = str(post.get('CAT_CLD') + ' ') + str(contcld)
                            if contcld > 0:
                                for pcl in partners_cld:
                                    activo_cld = 1
                                    estado = ''
                                    pais = ''
                                    if pcl['parent_id']:
                                        pclid = pcl['parent_id']
                                    else:
                                        pclid = pcl['id']
                                    if pcl['type'] == 'delivery': pcl['type'] = 'E'
                                    if pcl['type'] == 'invoice': pcl['type'] = 'F'
                                    if (pcl['type']) == False: pcl['type'] = ''
                                    if (pcl['street']) == False: pcl['street'] = ''
                                    if (pcl['city']) == False: pcl['city'] = ''
                                    if (pcl['state_id']) == False:
                                        pcl['state_id'] = ''
                                        estado = ''
                                    if (pcl['zip']) == False: pcl['zip'] = ''
                                    if (pcl['country_id']) == False:
                                        pcl['country_id'] = ''
                                        pais = ''
                                    if (pcl['email']) == False: pcl['email'] = ''
                                    if (pcl['phone']) == False: pcl['phone'] = ''
                                    if (pcl['mobile']) == False: pcl['mobile'] = ''
                                    if pcl['state_id'] is not '':
                                        valor = True
                                        for i in pcl['state_id']:
                                            if valor == True:
                                                estado = i
                                                valor = False
                                    if pcl['country_id'] is not '':
                                        valor2 = True
                                        for a in pcl['country_id']:
                                            if valor2 == True:
                                                pais = a
                                                valor2 = False
                                    insertcliente_cld = "INSERT OR REPLACE INTO cliente_direccion (id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES ((select  id from cliente_direccion where id_servidor ='" + str(
                                        pcl['id']) + "'),'" + str(
                                        pcl['id']) + "', (select id from cliente where id_servidor ='" + str(
                                        pclid) + "'),'" + str(
                                        pclid) + "','" + str(pcl['type']) + "','" + str(
                                        pcl['street']) + "',''," + "'','" + str(
                                        pcl['city']) + "','" + str(estado) + "','" + str(pcl['zip']) + "','" + str(
                                        pais) + "','','" + str(pcl['email']) + "','" + str(
                                        pcl['phone']) + "','" + str(
                                        pcl['mobile']) + "','','" + str(activo_cld) + "')"
                                    listadirecciones.append(insertcliente_cld)
                                valscld = {
                                    'update': 'true',
                                    'db_clientes_dirs_last_mod_date_count': new_cat_cld,
                                    'qrys': listadirecciones
                                }

                            else:
                                print("entro al else")
                                valscld = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valscld = {
                                'update': 'false'
                            }

                    else:
                        fecha_inicio_cld = post.get('CAT_CLD') + '.0'
                        print("fecha inicio cld %s" % fecha_inicio_cld)
                        partnerscldmx = odoo.SearchRead('res.partner', [], ['id', 'write_date'])
                        v2 = True
                        maxpartnercld = ''
                        for partcld in partnerscldmx:
                            if v2 == True:
                                maxpartnercld = partcld['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v2 = False
                            else:
                                if partcld['write_date'] > maxpartnercld:
                                    maxpartnercld = partcld['write_date']

                        print("valor maximo de fecha de clientes direecciones")
                        print(maxpartnercld)
                        contmaxcld = odoo.SearchCount('res.partner',
                                                      [('write_date', '>=', str(maxpartnercld) + '.0'),
                                                       ('write_date', '<=', str(maxpartnercld) + '.99')])
                        print("contador maximo cld")
                        print(contmaxcld)
                        new_cat_cld = str(maxpartnercld) + ' ' + str(contmaxcld)
                        print(new_cat_cld)
                        contcld = odoo.SearchCount('res.partner',
                                                   [('write_date', '>=', fecha_inicio_cld)])

                        partners_cld = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio_cld)],
                                                       ['id', 'type', 'street', 'city', 'state_id', 'zip', 'country_id',
                                                        'email', 'phone', 'mobile', 'parent_id'])
                        data_cld = str(post.get('CAT_CLD') + ' ') + str(contcld)
                        if contcld > 0:
                            for pcl in partners_cld:
                                activo_cld = 1
                                estado =''
                                pais= ''
                                if pcl['parent_id']:
                                    pclid = pcl['parent_id']
                                else:
                                    pclid = pcl['id']
                                if pcl['type'] == 'delivery': pcl['type'] = 'E'
                                if pcl['type'] == 'invoice': pcl['type'] = 'F'
                                if (pcl['type']) == False: pcl['type'] = ''
                                if (pcl['street']) == False: pcl['street'] = ''
                                if (pcl['city']) == False: pcl['city'] = ''
                                if (pcl['state_id']) == False:
                                    pcl['state_id'] = ''
                                    estado=''
                                if (pcl['zip']) == False: pcl['zip'] = ''
                                if (pcl['country_id']) == False:
                                    pcl['country_id'] = ''
                                    pais = ''
                                if (pcl['email']) == False: pcl['email'] = ''
                                if (pcl['phone']) == False: pcl['phone'] = ''
                                if (pcl['mobile']) == False: pcl['mobile'] = ''
                                if pcl['state_id'] is not '':
                                    valor=True
                                    for i in pcl['state_id']:
                                        if valor==True:
                                            estado=i
                                            valor=False
                                if pcl['country_id'] is not '':
                                    valor2=True
                                    for a in pcl['country_id']:
                                        if valor2==True:
                                            pais=a
                                            valor2=False
                                insertcliente_cld =  "INSERT OR REPLACE INTO cliente_direccion (id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES ((select  id from cliente_direccion where id_servidor ='" + str(
                                    pcl['id']) + "'),'" + str(
                                    pcl['id']) + "', (select id from cliente where id_servidor ='" + str(
                                    pclid) + "'),'" + str(
                                    pclid) + "','" + str(pcl['type']) + "','" + str(pcl['street']) + "',''," + "'','" + str(
                                    pcl['city']) + "','" + str(estado) + "','" + str(pcl['zip']) + "','" + str(pais) + "','','" + str(pcl['email']) + "','" + str(
                                    pcl['phone']) + "','" + str(
                                    pcl['mobile']) + "','','" + str(activo_cld) + "')"
                                listadirecciones.append(insertcliente_cld)
                            valscld = {
                                'update': 'true',
                                'db_clientes_dirs_last_mod_date_count': new_cat_cld,
                                'qrys': listadirecciones
                            }

                        else:
                            print("entro al else")
                            valscld = {
                                'update': 'false'
                            }


                #####################PRODUCTOS###########################
                if post.get('CAT_P') is  None or post.get('CAT_P')== '':
                    contp = odoo.SearchCount('product.template',[])
                    product = odoo.SearchRead('product.template', [],
                                              ['id', 'default_code', 'name', 'description', 'list_price', 'uom_id',
                                               'active'])
                    productmx = odoo.SearchRead('product.template', [], ['id', 'write_date'])
                    v3 = True
                    maxproduct = ''
                    for prod in productmx:
                        if v3 == True:
                            maxproduct = prod['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v3 = False
                        else:
                            if prod['write_date'] > maxproduct:
                                maxproduct = prod['write_date']

                    print("valor maximo de fecha de productos")
                    print(maxproduct)
                    contmaxproduct = odoo.SearchCount('product.template',
                                                  [('write_date', '>=', str(maxproduct) + '.0'),
                                                   ('write_date', '<=', str(maxproduct) + '.99')])
                    print("contador maximo producto")
                    print(contmaxproduct)
                    new_cat_p = str(maxproduct) + ' ' + str(contmaxproduct)
                    print(new_cat_p)
                    data_pr = str(post.get('CAT_P') + ' ') + str(contp)
                    if contp > 0:
                        for pr in product:
                            if str(pr['active']) == False:
                                activop = 0
                            else:
                                activop = 1
                            if (pr['default_code']) == False: pr['default_code'] = ''
                            if (pr['name']) == False: pr['name'] = ''
                            if (pr['description']) == False: pr['description'] = ''
                            if (pr['list_price']) == False: pr['list_price'] = ''
                            if (pr['uom_id']) == False: pr['uom_id'] = ''
                            insertproduct = "INSERT OR REPLACE INTO producto (id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES ('" + str(
                                pr['id']) + "','" + str(pr['default_code']) + "','" + str(pr['name']) + "','" + str(
                                pr['description']) + "','" + str(pr['list_price']) + "','" + str(
                                6) + "', '" + str(activop) + "')"
                            listaproductos.append(insertproduct)
                        valsproduct = {
                            'update': 'true',
                            'db_productos_last_mod_date_count': new_cat_p,
                            'qrys': listaproductos
                        }
                    else:
                        print("entro al else")
                        valsproduct = {
                            'update': 'false'
                        }

                else:
                    print("entro al else productos")
                    if len(post.get('CAT_P')) > 19:
                        dE = post.get('CAT_P')[0:19]
                        fecha_inicio_p = dE + '.0'
                        print(fecha_inicio_p)
                        productmx = odoo.SearchRead('product.template', [], ['id', 'write_date'])
                        v3 = True
                        maxproduct = ''
                        for prod in productmx:
                            if v3 == True:
                                maxproduct = prod['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v3 = False
                            else:
                                if prod['write_date'] > maxproduct:
                                    maxproduct = prod['write_date']

                        print("valor maximo de fecha de productos")
                        print(maxproduct)
                        contmaxproduct = odoo.SearchCount('product.template',
                                                          [('write_date', '>=', str(maxproduct) + '.0'),
                                                           ('write_date', '<=', str(maxproduct) + '.99')])
                        print("contador maximo producto")
                        print(contmaxproduct)
                        new_cat_p = str(maxproduct) + ' ' + str(contmaxproduct)
                        print(new_cat_p)
                        if new_cat_p != post.get('CAT_P'):
                            contp = odoo.SearchCount('product.product',
                                                     [('write_date', '>=', fecha_inicio_p)])

                            product = odoo.SearchRead('product.product', [('write_date', '>=', fecha_inicio_p)],
                                                      ['id', 'default_code', 'name', 'description', 'list_price', 'uom_id',
                                                       'active'])
                            data_pr = str(post.get('CAT_P') + ' ') + str(contp)

                            if contp > 0:
                                for pr in product:
                                    if str(pr['active']) == False:
                                        activop = 0
                                    else:
                                        activop = 1
                                    if (pr['default_code']) == False: pr['default_code'] = ''
                                    if (pr['name']) == False: pr['name'] = ''
                                    if (pr['description']) == False: pr['description'] = ''
                                    if (pr['list_price']) == False: pr['list_price'] = ''
                                    if (pr['uom_id']) == False: pr['uom_id'] = ''
                                    insertproduct = "INSERT OR REPLACE INTO producto (id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES ('" + str(
                                        pr['id']) + "','" + str(pr['default_code']) + "','" + str(pr['name']) + "','" + str(
                                        pr['description']) + "','" + str(pr['list_price']) + "','" + str(
                                        6) + "', '" + str(activop) + "')"
                                    listaproductos.append(insertproduct)
                                valsproduct = {
                                    'update': 'true',
                                    'db_productos_last_mod_date_count': new_cat_p,
                                    'qrys': listaproductos
                                }
                            else:
                                print("entro al else")
                                valsproduct = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valsproduct = {
                                'update': 'false'
                            }

                    else:
                        fecha_inicio_p = post.get('CAT_P') + '.0'
                        print("fecha inicio productos %s" % fecha_inicio_p)
                        contp = odoo.SearchCount('product.product',
                                                 [('write_date', '>=', fecha_inicio_p)])

                        product = odoo.SearchRead('product.product', [('write_date', '>=', fecha_inicio_p)],
                                                  ['id', 'default_code', 'name', 'description', 'list_price', 'uom_id',
                                                   'active'])
                        data_pr = str(post.get('CAT_P') + ' ') + str(contp)
                        productmx = odoo.SearchRead('product.template', [], ['id', 'write_date'])
                        v3 = True
                        maxproduct = ''
                        for prod in productmx:
                            if v3 == True:
                                maxproduct = prod['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v3 = False
                            else:
                                if prod['write_date'] > maxproduct:
                                    maxproduct = prod['write_date']

                        print("valor maximo de fecha de productos")
                        print(maxproduct)
                        contmaxproduct = odoo.SearchCount('product.template',
                                                          [('write_date', '>=', str(maxproduct) + '.0'),
                                                           ('write_date', '<=', str(maxproduct) + '.99')])
                        print("contador maximo producto")
                        print(contmaxproduct)
                        new_cat_p = str(maxproduct) + ' ' + str(contmaxproduct)
                        print(new_cat_p)
                        if contp > 0:
                            for pr in product:
                                if str(pr['active']) == False:
                                    activop = 0
                                else:
                                    activop = 1
                                if (pr['default_code']) == False: pr['default_code'] = ''
                                if (pr['name']) == False: pr['name'] = ''
                                if (pr['description']) == False: pr['description'] = ''
                                if (pr['list_price']) == False: pr['list_price'] = ''
                                if (pr['uom_id']) == False: pr['uom_id'] = ''
                                insertproduct =  "INSERT OR REPLACE INTO producto (id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES ('" + str(
                                    pr['id']) + "','" + str(pr['default_code']) + "','" + str(pr['name']) + "','" + str(
                                    pr['description']) + "','" + str(pr['list_price']) + "','" + str(
                                    6) + "', '" + str(activop) + "')"
                                listaproductos.append(insertproduct)
                            valsproduct = {
                                'update': 'true',
                                'db_productos_last_mod_date_count': new_cat_p,
                                'qrys': listaproductos
                            }
                        else:
                            print("entro al else")
                            valsproduct = {
                                'update': 'false'
                            }

                #####################Estados###########################
                if post.get('CAT_ES') is None or post.get('CAT_ES')==  '':
                    contstate = odoo.SearchCount('res.country.state',[])

                    state_ids = odoo.SearchRead('res.country.state', [],
                                                ['id', 'country_id', 'name', 'active'])
                    datastate = str(post.get('CAT_ES') + ' ') + str(contstate)
                    statemx = odoo.SearchRead('res.country.state', [], ['id', 'write_date'])
                    v4 = True
                    maxstate = ''
                    for st in statemx:
                        if v4 == True:
                            maxstate = st['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v4 = False
                        else:
                            if st['write_date'] > maxstate:
                                maxstate = st['write_date']

                    print("valor maximo de fecha de estados")
                    print(maxstate)
                    contmaxstate = odoo.SearchCount('res.country.state',
                                                      [('write_date', '>=', str(maxstate) + '.0'),
                                                       ('write_date', '<=', str(maxstate) + '.99')])
                    print("contador maximo state")
                    print(contmaxstate)
                    new_cat_es = str(maxstate) + ' ' + str(contmaxstate)
                    print(new_cat_es)
                    if contstate > 0:
                        for state in state_ids:
                            activostate = 1
                            country = ''
                            if (state['country_id']) == False: state['country_id'] = ''
                            if (state['name']) == False: state['name'] = ''
                            if state['country_id'] is not '':
                                valor = True
                                for i in state['country_id']:
                                    if valor == True:
                                        country = i
                                        valor = False
                            insertstate = "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES ('" + str(
                                state['id']) + "','" + str(country) + "','" + str(
                                state['name']) + "','" + str(
                                activostate) + "')"
                            listastate.append(insertstate)
                        valsstate = {
                            'update': 'true',
                            'db_estados_last_mod_date_count': new_cat_es,
                            'qrys': listastate
                        }
                    else:
                        print("entro al else")
                        valsstate = {
                            'update': 'false'
                        }
                else:
                    print("entro al else estados")
                    if len(post.get('CAT_ES')) > 19:
                        print(post.get('CAT_ES'))
                        dEs = post.get('CAT_ES')[0:19]
                        print(dEs)
                        fecha_inicio_state = dEs + '.0'
                        print(fecha_inicio_state)

                        statemx = odoo.SearchRead('res.country.state', [], ['id', 'write_date'])
                        v4 = True
                        maxstate = ''
                        for st in statemx:
                            if v4 == True:
                                maxstate = st['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v4 = False
                            else:
                                if st['write_date'] > maxstate:
                                    maxstate = st['write_date']

                        print("valor maximo de fecha de estados")
                        print(maxstate)
                        contmaxstate = odoo.SearchCount('res.country.state',
                                                        [('write_date', '>=', str(maxstate) + '.0'),
                                                         ('write_date', '<=', str(maxstate) + '.99')])
                        print("contador maximo state")
                        print(contmaxstate)
                        new_cat_es = str(maxstate) + ' ' + str(contmaxstate)
                        print(new_cat_es)
                        if new_cat_es != post.get('CAT_ES'):
                            print("entro al if de diferentes valores estados")
                            contstate = odoo.SearchCount('res.country.state',
                                                         [('write_date', '>=', fecha_inicio_state)])

                            state_ids = odoo.SearchRead('res.country.state', [('write_date', '>=', fecha_inicio_state)],
                                                        ['id', 'country_id', 'name', 'active'])
                            datastate = str(post.get('CAT_ES') + ' ') + str(contstate)
                            print("valor de cont state")
                            print(contstate)
                            if contstate > 0:
                                print("entro al if de cont mayor a 0")
                                for state in state_ids:
                                    print("entro al for")
                                    activostate = 1
                                    country = ''
                                    if (state['country_id']) == False: state['country_id'] = ''
                                    if (state['name']) == False: state['name'] = ''
                                    if state['country_id'] is not '':
                                        valor = True
                                        for i in state['country_id']:
                                            if valor == True:
                                                country = i
                                                valor = False
                                    insertstate = "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES ('" + str(
                                        state['id']) + "','" + str(country) + "','" + str(
                                        state['name']) + "','" + str(
                                        activostate) + "')"
                                    listastate.append(insertstate)
                                valsstate = {
                                    'update': 'true',
                                    'db_estados_last_mod_date_count': new_cat_es,
                                    'qrys': listastate
                                }
                            else:
                                print("entro al else")
                                valsstate = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valsstate = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_state = post.get('CAT_ES') + '.0'
                        print("fecha inicio estados %s" % fecha_inicio_state)
                        contstate = odoo.SearchCount('res.country.state',
                                                     [('write_date', '>=', fecha_inicio_state)])

                        state_ids = odoo.SearchRead('res.country.state', [('write_date', '>=', fecha_inicio_state)],
                                                    ['id', 'country_id', 'name', 'active'])
                        datastate = str(post.get('CAT_ES') + ' ') + str(contstate)
                        statemx = odoo.SearchRead('res.country.state', [], ['id', 'write_date'])
                        v4 = True
                        maxstate = ''
                        for st in statemx:
                            if v4 == True:
                                maxstate = st['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v4 = False
                            else:
                                if st['write_date'] > maxstate:
                                    maxstate = st['write_date']

                        print("valor maximo de fecha de estados")
                        print(maxstate)
                        contmaxstate = odoo.SearchCount('res.country.state',
                                                        [('write_date', '>=', str(maxstate) + '.0'),
                                                         ('write_date', '<=', str(maxstate) + '.99')])
                        print("contador maximo state")
                        print(contmaxstate)
                        new_cat_es = str(maxstate) + ' ' + str(contmaxstate)
                        print(new_cat_es)
                        if contstate >0:
                            for state in state_ids:
                                activostate = 1
                                country=''
                                if (state['country_id']) == False: state['country_id'] = ''
                                if (state['name']) == False: state['name'] = ''
                                if state['country_id'] is not '':
                                    valor=True
                                    for i in state['country_id']:
                                        if valor==True:
                                            country=i
                                            valor=False
                                insertstate = "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES ('" + str(
                                    state['id']) + "','" + str(country) + "','" + str(
                                    state['name']) + "','" + str(
                                    activostate) + "')"
                                listastate.append(insertstate)
                            valsstate = {
                                'update': 'true',
                                'db_estados_last_mod_date_count': new_cat_es,
                                'qrys': listastate
                            }
                        else:
                            print("entro al else")
                            valsstate = {
                                'update': 'false'
                            }

                #####################Paises###########################
                if post.get('CAT_PA') is None or post.get('CAT_PA') == '':
                    paismx = odoo.SearchRead('res.country', [], ['id', 'write_date'])
                    v5 = True
                    maxpais = ''
                    for pai in paismx:
                        if v5 == True:
                            maxpais = pai['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v5 = False
                        else:
                            if pai['write_date'] > maxpais:
                                maxpais = pai['write_date']

                    print("valor maximo de fecha de pais")
                    print(maxpais)
                    contmaxpais = odoo.SearchCount('res.country',
                                                   [('write_date', '>=', str(maxpais) + '.0'),
                                                    ('write_date', '<=', str(maxpais) + '.99')])
                    print("contador maximo pais")
                    print(contmaxpais)
                    new_cat_pa = str(maxpais) + ' ' + str(contmaxpais)
                    print(new_cat_pa)
                    contpais = odoo.SearchCount('res.country', [])

                    pais_ids = odoo.SearchRead('res.country', [],
                                               ['id', 'name', 'active'])
                    datapais = str(post.get('CAT_PA') + ' ') + str(contpais)
                    if contpais > 0:
                        for pais in pais_ids:
                            activopais = 1
                            insertpais = "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES (" + str(
                                pais['id']) + ",'" + str(pais['name']) + "'," + str(activopais) + ")"
                            listapais.append(insertpais)
                        valspaises = {
                            'update': 'true',
                            'db_paises_last_mod_date_count': new_cat_pa,
                            'qrys': listapais
                        }
                    else:
                        print("entro al else")
                        valspaises = {
                            'update': 'false'
                        }
                else:
                    print("entro al else pais")
                    if len(post.get('CAT_PA')) > 19:
                        print(post.get('CAT_PA'))
                        dEst = post.get('CAT_PA')[0:19]
                        print(dEst)
                        fecha_inicio_pais =dEst + '.0'
                        print("fecha inicio %s" % fecha_inicio_pais)
                        paismx = odoo.SearchRead('res.country', [], ['id', 'write_date'])
                        v5 = True
                        maxpais = ''
                        for pai in paismx:
                            if v5 == True:
                                maxpais = pai['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v5 = False
                            else:
                                if pai['write_date'] > maxpais:
                                    maxpais = pai['write_date']

                        print("valor maximo de fecha de pais")
                        print(maxpais)
                        contmaxpais = odoo.SearchCount('res.country',
                                                       [('write_date', '>=', str(maxpais) + '.0'),
                                                        ('write_date', '<=', str(maxpais) + '.99')])
                        print("contador maximo pais")
                        print(contmaxpais)
                        new_cat_pa = str(maxpais) + ' ' + str(contmaxpais)
                        print(new_cat_pa)
                        if new_cat_pa != post.get('CAT_PA'):
                            contpais = odoo.SearchCount('res.country',
                                                        [('write_date', '>=', fecha_inicio_pais)])

                            pais_ids = odoo.SearchRead('res.country', [('write_date', '>=', fecha_inicio_pais)],
                                                       ['id', 'name', 'active'])
                            datapais = str(post.get('CAT_PA') + ' ') + str(contpais)
                            if contpais > 0:
                                for pais in pais_ids:
                                    activopais = 1
                                    insertpais = "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES (" + str(
                                        pais['id']) + ",'" + str(pais['name']) + "'," + str(activopais) + ")"
                                    listapais.append(insertpais)
                                valspaises = {
                                    'update': 'true',
                                    'db_paises_last_mod_date_count': new_cat_pa,
                                    'qrys': listapais
                                }
                            else:
                                print("entro al else")
                                valspaises = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valspaises = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_pais = post.get('CAT_PA') + '.0'
                        print("fecha inicio %s" % fecha_inicio_pais)
                        paismx = odoo.SearchRead('res.country', [], ['id', 'write_date'])
                        v5 = True
                        maxpais = ''
                        for pai in paismx:
                            if v5 == True:
                                maxpais = pai['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v5 = False
                            else:
                                if pai['write_date'] > maxpais:
                                    maxpais = pai['write_date']

                        print("valor maximo de fecha de pais")
                        print(maxpais)
                        contmaxpais = odoo.SearchCount('res.country',
                                                        [('write_date', '>=', str(maxpais) + '.0'),
                                                         ('write_date', '<=', str(maxpais) + '.99')])
                        print("contador maximo pais")
                        print(contmaxpais)
                        new_cat_pa = str(maxpais) + ' ' + str(contmaxpais)
                        print(new_cat_pa)
                        contpais = odoo.SearchCount('res.country',
                                                    [('write_date', '>=', fecha_inicio_pais)])

                        pais_ids = odoo.SearchRead('res.country', [('write_date', '>=', fecha_inicio_pais)],
                                                   ['id', 'name', 'active'])
                        datapais = str(post.get('CAT_PA') + ' ') + str(contpais)
                        if contpais >0:
                            for pais in pais_ids:
                                activopais = 1
                                insertpais =  "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES (" + str(
                                    pais['id']) + ",'" + str(pais['name']) + "'," + str(activopais) + ")"
                                listapais.append(insertpais)
                            valspaises = {
                                'update': 'true',
                                'db_paises_last_mod_date_count': new_cat_pa,
                                'qrys': listapais
                            }
                        else:
                            print("entro al else")
                            valspaises = {
                                'update': 'false'
                            }
                #####################TARIFAS###########################
                if post.get('CAT_TA') is None or post.get('CAT_TA') == '':
                    pricelistmx = odoo.SearchRead('product.pricelist', [], ['id', 'write_date'])
                    v6 = True
                    maxpricelist = ''
                    for prl in pricelistmx:
                        if v6 == True:
                            maxpricelist = prl['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v6 = False
                        else:
                            if prl['write_date'] > maxpricelist:
                                maxpricelist = prl['write_date']

                    print("valor maximo de fecha de precio de listas")
                    print(maxpricelist)
                    contmaxpricelist = odoo.SearchCount('product.pricelist',
                                                        [('write_date', '>=', str(maxpricelist) + '.0'),
                                                         ('write_date', '<=', str(maxpricelist) + '.99')])
                    print("contador maximo precio de lista")
                    print(contmaxpricelist)
                    new_cat_ta = str(maxpricelist) + ' ' + str(contmaxpricelist)
                    print(new_cat_ta)
                    conttarifa = odoo.SearchCount('product.pricelist',[])

                    tarifa_ids = odoo.SearchRead('product.pricelist', [],
                                                 ['id', 'name', 'active'])
                    print("valor de tarifas")
                    print(conttarifa)
                    datatarifa = str(post.get('CAT_TA') + ' ') + str(conttarifa)
                    if conttarifa > 0:
                        print("entro al if")
                        print(tarifa_ids)
                        for tarifa in tarifa_ids:
                            print("entro al for")
                            if tarifa['active'] == False:
                                activotarifa = 0
                            else:
                                activotarifa = 1

                            inserttarifa = "INSERT OR REPLACE INTO tarifa (id_servidor,nombre,active) VALUES (" + str(
                                tarifa['id']) + ",'" + str(tarifa['name']) + "'," + str(activotarifa) + ")"
                            listatarifa.append(inserttarifa)
                        valstarifa = {
                            'update': 'true',
                            'db_tarifas_last_mod_date_count': new_cat_ta,
                            'qrys': listatarifa
                        }
                    else:
                        print("entro al else")
                        valstarifa = {
                            'update': 'false'
                        }
                else:
                    print("entro al else PRECIO LISTA")
                    if len(post.get('CAT_TA')) > 19:
                        print(post.get('CAT_TA'))
                        ta = post.get('CAT_TA')[0:19]
                        print(ta)
                        fecha_inicio_tarifa = ta + '.0'
                        print("fecha inicio %s" % fecha_inicio_tarifa)
                        pricelistmx = odoo.SearchRead('product.pricelist', [], ['id', 'write_date'])
                        v6 = True
                        maxpricelist = ''
                        for prl in pricelistmx:
                            if v6 == True:
                                maxpricelist = prl['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v6 = False
                            else:
                                if prl['write_date'] > maxpricelist:
                                    maxpricelist = prl['write_date']

                        print("valor maximo de fecha de precio de listas")
                        print(maxpricelist)
                        contmaxpricelist = odoo.SearchCount('product.pricelist',
                                                            [('write_date', '>=', str(maxpricelist) + '.0'),
                                                             ('write_date', '<=', str(maxpricelist) + '.99')])
                        print("contador maximo precio de lista")
                        print(contmaxpricelist)
                        new_cat_ta = str(maxpricelist) + ' ' + str(contmaxpricelist)
                        print(new_cat_ta)
                        if new_cat_ta != post.get('CAT_TA'):
                            conttarifa = odoo.SearchCount('product.pricelist',
                                                          [('write_date', '>=', fecha_inicio_tarifa)])

                            tarifa_ids = odoo.SearchRead('product.pricelist', [('write_date', '>=', fecha_inicio_tarifa)],
                                                         ['id', 'name', 'active'])
                            print("valor de tarifas")
                            print(conttarifa)
                            datatarifa = str(post.get('CAT_TA') + ' ') + str(conttarifa)
                            if conttarifa > 0:
                                print("entro al if")
                                print(tarifa_ids)
                                for tarifa in tarifa_ids:
                                    print("entro al for")
                                    if tarifa['active'] == False:
                                        activotarifa = 0
                                    else:
                                        activotarifa = 1

                                    inserttarifa = "INSERT OR REPLACE INTO tarifa (id_servidor,nombre,active) VALUES (" + str(
                                        tarifa['id']) + ",'" + str(tarifa['name']) + "'," + str(activotarifa) + ")"
                                    listatarifa.append(inserttarifa)
                                valstarifa = {
                                    'update': 'true',
                                    'db_tarifas_last_mod_date_count': new_cat_ta,
                                    'qrys': listatarifa
                                }
                            else:
                                print("entro al else")
                                valstarifa = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valstarifa = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_tarifa = post.get('CAT_TA') + '.0'
                        print("fecha inicio %s" % fecha_inicio_tarifa)
                        pricelistmx = odoo.SearchRead('product.pricelist', [], ['id', 'write_date'])
                        v6 = True
                        maxpricelist = ''
                        for prl in pricelistmx:
                            if v6 == True:
                                maxpricelist = prl['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v6 = False
                            else:
                                if prl['write_date'] > maxpricelist:
                                    maxpricelist = prl['write_date']

                        print("valor maximo de fecha de precio de listas")
                        print(maxpricelist)
                        contmaxpricelist = odoo.SearchCount('product.pricelist',
                                                       [('write_date', '>=', str(maxpricelist) + '.0'),
                                                        ('write_date', '<=', str(maxpricelist) + '.99')])
                        print("contador maximo precio de lista")
                        print(contmaxpricelist)
                        new_cat_ta = str(maxpricelist) + ' ' + str(contmaxpricelist)
                        print(new_cat_ta)
                        conttarifa = odoo.SearchCount('product.pricelist',
                                                      [('write_date', '>=', fecha_inicio_tarifa)])

                        tarifa_ids = odoo.SearchRead('product.pricelist', [('write_date', '>=', fecha_inicio_tarifa)],
                                                     ['id', 'name', 'active'])
                        print("valor de tarifas")
                        print(conttarifa)
                        datatarifa = str(post.get('CAT_TA') + ' ') + str(conttarifa)
                        if conttarifa > 0:
                            print("entro al if")
                            print(tarifa_ids)
                            for tarifa in tarifa_ids:
                                print("entro al for")
                                if tarifa['active'] == False:
                                    activotarifa = 0
                                else:
                                    activotarifa = 1

                                inserttarifa = "INSERT OR REPLACE INTO tarifa (id_servidor,nombre,active) VALUES (" + str(
                                    tarifa['id']) + ",'" + str(tarifa['name']) + "'," + str(activotarifa) + ")"
                                listatarifa.append(inserttarifa)
                            valstarifa = {
                                'update': 'true',
                                'db_tarifas_last_mod_date_count': new_cat_ta,
                                'qrys': listatarifa
                            }
                        else:
                            print("entro al else")
                            valstarifa = {
                                'update': 'false'
                            }

                ####################PLAZOS DE PAGO###########################
                if post.get('CAT_PLP') is None or post.get('CAT_PLP') == '':
                    plpmx = odoo.SearchRead('account.payment.term', [], ['id', 'write_date'])
                    v7 = True
                    maxplp = ''
                    for plpl in plpmx:
                        print(plpl['write_date'])
                        if v7 == True:
                            maxplp = plpl['write_date']
                            v7 = False
                        else:
                            if plpl['write_date'] > maxplp:
                                maxplp = plpl['write_date']

                    print("valor maximo de plazo de pago")
                    print(maxplp)
                    contmaxplp = odoo.SearchCount('account.payment.term',
                                                  [('write_date', '>=', str(maxplp) + '.0'),
                                                   ('write_date', '<=', str(maxplp) + '.99')])
                    print("contador maximo plazo de pago")
                    print(contmaxplp)
                    new_cat_plp = str(maxplp) + ' ' + str(contmaxplp)
                    print(new_cat_plp)
                    contplp = odoo.SearchCount('account.payment.term', [])

                    plp_ids = odoo.SearchRead('account.payment.term', [],
                                              ['id', 'name', 'active'])
                    dataplp = str(post.get('CAT_PLP') + ' ') + str(contplp)
                    if contplp > 0:
                        for plp in plp_ids:
                            if plp['active'] == False:
                                activoplp = 0
                            else:
                                activoplp = 1
                            insertplp = "INSERT OR REPLACE INTO​ plaza_pago (id_servidor,nombre,active) VALUES (" + str(
                                plp['id']) + ",'" + str(plp['name']) + "'," + str(activoplp) + ")"

                            listaplp.append(insertplp)
                        valsplp = {
                            'update': 'true',
                            'db_plazas_pago_last_mod_date_count': new_cat_plp,
                            'qrys': listaplp
                        }
                    else:
                        print("entro al else")
                        valsplp = {
                            'update': 'false'
                        }
                else:
                    print("entro al else Plazo de pago")
                    if len(post.get('CAT_PLP')) > 19:
                        print(post.get('CAT_PLP'))
                        catplp = post.get('CAT_PLP')[0:19]
                        print(catplp)
                        fecha_inicio_plp = catplp + '.0'
                        print("fecha inicio %s" % fecha_inicio_plp)
                        plpmx = odoo.SearchRead('account.payment.term', [], ['id', 'write_date'])
                        v7 = True
                        maxplp = ''
                        for plpl in plpmx:
                            if v7 == True:
                                maxplp = plpl['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v7 = False
                            else:
                                if plpl['write_date'] > maxplp:
                                    maxplp = plpl['write_date']

                        print("valor maximo de plazo de pago")
                        print(maxplp)
                        contmaxplp = odoo.SearchCount('account.payment.term',
                                                      [('write_date', '>=', str(maxplp) + '.0'),
                                                       ('write_date', '<=', str(maxplp) + '.99')])
                        print("contador maximo plazo de pago")
                        print(contmaxplp)
                        new_cat_plp = str(maxplp) + ' ' + str(contmaxplp)
                        print(new_cat_plp)
                        if new_cat_plp != post.get('CAT_PLP'):
                            contplp = odoo.SearchCount('account.payment.term',
                                                       [('write_date', '>=', fecha_inicio_plp)])

                            plp_ids = odoo.SearchRead('account.payment.term', [('write_date', '>=', fecha_inicio_plp)],
                                                      ['id', 'name', 'active'])
                            dataplp = str(post.get('CAT_PLP') + ' ') + str(contplp)
                            if contplp > 0:
                                for plp in plp_ids:
                                    if plp['active'] == False:
                                        activoplp = 0
                                    else:
                                        activoplp = 1
                                    insertplp = "INSERT OR REPLACE INTO​ plaza_pago (id_servidor,nombre,active) VALUES (" + str(
                                        plp['id']) + ",'" + str(plp['name']) + "'," + str(activoplp) + ")"

                                    listaplp.append(insertplp)
                                valsplp = {
                                    'update': 'true',
                                    'db_plazas_pago_last_mod_date_count': new_cat_plp,
                                    'qrys': listaplp
                                }
                            else:
                                print("entro al else")
                                valsplp = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valsplp = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_plp = post.get('CAT_PLP') + '.0'
                        print("fecha inicio %s" % fecha_inicio_plp)
                        plpmx = odoo.SearchRead('account.payment.term', [], ['id', 'write_date'])
                        v7 = True
                        maxplp = ''
                        for plpl in plpmx:
                            if v7 == True:
                                maxplp = plpl['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v7 = False
                            else:
                                if plpl['write_date'] > maxplp:
                                    maxplp = plpl['write_date']

                        print("valor maximo de plazo de pago")
                        print(maxplp)
                        contmaxplp = odoo.SearchCount('account.payment.term',
                                                            [('write_date', '>=', str(maxplp) + '.0'),
                                                             ('write_date', '<=', str(maxplp) + '.99')])
                        print("contador maximo plazo de pago")
                        print(contmaxplp)
                        new_cat_plp = str(maxplp) + ' ' + str(contmaxplp)
                        print(new_cat_plp)
                        contplp = odoo.SearchCount('account.payment.term',
                                                   [('write_date', '>=', fecha_inicio_plp)])

                        plp_ids = odoo.SearchRead('account.payment.term', [('write_date', '>=', fecha_inicio_plp)],
                                                  ['id', 'name', 'active'])
                        dataplp = str(post.get('CAT_PLP') + ' ') + str(contplp)
                        if contplp > 0:
                            for plp in plp_ids:
                                if plp['active'] == False:
                                    activoplp = 0
                                else:
                                    activoplp = 1
                                insertplp =  "INSERT OR REPLACE INTO​ plaza_pago (id_servidor,nombre,active) VALUES (" + str(
                                    plp['id']) + ",'" + str(plp['name']) + "'," + str(activoplp) + ")"

                                listaplp.append(insertplp)
                            valsplp = {
                                'update': 'true',
                                'db_plazas_pago_last_mod_date_count': new_cat_plp,
                                'qrys': listaplp
                            }
                        else:
                            print("entro al else")
                            valsplp = {
                                'update': 'false'
                            }

                ####################CUENTAS BANCARIAS###########################
                if post.get('CAT_CUB') is  None or post.get('CAT_CUB') == '':
                    cubmx = odoo.SearchRead('res.bank', [], ['id', 'write_date'])
                    v8 = True
                    maxcub = ''
                    for cu in cubmx:
                        if v8 == True:
                            maxcub = cu['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v8 = False
                        else:
                            if cu['write_date'] > maxcub:
                                maxcub = cu['write_date']

                    print("valor maximo de  cuentas bancarias")
                    print(maxcub)
                    contmaxcub = odoo.SearchCount('res.bank',
                                                  [('write_date', '>=', str(maxcub) + '.0'),
                                                   ('write_date', '<=', str(maxcub) + '.99')])
                    print("contador maximo cuentas bancarias")
                    print(contmaxcub)
                    new_cat_cub = str(maxcub) + ' ' + str(contmaxcub)
                    print(new_cat_cub)
                    contcub = odoo.SearchCount('res.bank',
                                               [])

                    cub_ids = odoo.SearchRead('res.bank', [],
                                              ['id', 'name', 'active'])
                    datacub = str(post.get('CAT_CUB') + ' ') + str(contcub)
                    if contcub > 0:
                        for cub in cub_ids:
                            if cub['active'] == False:
                                activocub = 0
                            else:
                                activocub = 1
                            insertcub = "INSERT OR REPLACE INTO  cuenta_bancaria (id_servidor,nombre,active) VALUES (" + str(
                                cub['id']) + ",'" + str(cub['name']) + "'," + str(activocub) + ")"
                            listacub.append(insertcub)
                        valscub = {
                            'update': 'true',
                            'db_cuentas_bancarias_last_mod_date_count': new_cat_cub,
                            'qrys': listacub
                        }
                    else:
                        print("entro al else")
                        valscub = {
                            'update': 'false'
                        }
                else:
                    print("entro al else cuentas bancarias")
                    if len(post.get('CAT_CUB')) > 19:
                        print(post.get('CAT_CUB'))
                        catcub = post.get('CAT_CUB')[0:19]
                        print(catcub)
                        fecha_inicio_cub = catcub + '.0'
                        print("fecha inicio %s" % fecha_inicio_plp)
                        cubmx = odoo.SearchRead('res.bank', [], ['id', 'write_date'])
                        v8 = True
                        maxcub = ''
                        for cu in cubmx:
                            if v8 == True:
                                maxcub = cu['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v8 = False
                            else:
                                if cu['write_date'] > maxcub:
                                    maxcub = cu['write_date']

                        print("valor maximo de  cuentas bancarias")
                        print(maxcub)
                        contmaxcub = odoo.SearchCount('res.bank',
                                                      [('write_date', '>=', str(maxcub) + '.0'),
                                                       ('write_date', '<=', str(maxcub) + '.99')])
                        print("contador maximo cuentas bancarias")
                        print(contmaxcub)
                        new_cat_cub = str(maxcub) + ' ' + str(contmaxcub)
                        print(new_cat_cub)
                        if new_cat_cub != post.get('CAT_CUB'):
                            contcub = odoo.SearchCount('res.bank',
                                                       [('write_date', '>=', fecha_inicio_cub)])

                            cub_ids = odoo.SearchRead('res.bank', [('write_date', '>=', fecha_inicio_cub)],
                                                      ['id', 'name', 'active'])
                            datacub = str(post.get('CAT_CUB') + ' ') + str(contcub)
                            if contcub > 0:
                                for cub in cub_ids:
                                    if cub['active'] == False:
                                        activocub = 0
                                    else:
                                        activocub = 1
                                    insertcub = "INSERT OR REPLACE INTO  cuenta_bancaria (id_servidor,nombre,active) VALUES (" + str(
                                        cub['id']) + ",'" + str(cub['name']) + "'," + str(activocub) + ")"
                                    listacub.append(insertcub)
                                valscub = {
                                    'update': 'true',
                                    'db_cuentas_bancarias_last_mod_date_count': new_cat_cub,
                                    'qrys': listacub
                                }
                            else:
                                print("entro al else")
                                valscub = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valscub = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_cub = post.get('CAT_CUB') + '.0'
                        print("fecha inicio %s" % fecha_inicio_cub)
                        cubmx = odoo.SearchRead('res.bank', [], ['id', 'write_date'])
                        v8 = True
                        maxcub = ''
                        for cu in cubmx:
                            if v8 == True:
                                maxcub = cu['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v8 = False
                            else:
                                if cu['write_date'] > maxcub:
                                    maxcub = cu['write_date']

                        print("valor maximo de  cuentas bancarias")
                        print(maxcub)
                        contmaxcub = odoo.SearchCount('res.bank',
                                                      [('write_date', '>=', str(maxcub) + '.0'),
                                                       ('write_date', '<=', str(maxcub) + '.99')])
                        print("contador maximo cuentas bancarias")
                        print(contmaxcub)
                        new_cat_cub = str(maxcub) + ' ' + str(contmaxcub)
                        print(new_cat_cub)
                        contcub = odoo.SearchCount('res.bank',
                                                   [('write_date', '>=', fecha_inicio_cub)])

                        cub_ids = odoo.SearchRead('res.bank', [('write_date', '>=', fecha_inicio_cub)],
                                                  ['id', 'name', 'active'])
                        datacub = str(post.get('CAT_CUB') + ' ') + str(contcub)
                        if contcub >0:
                            for cub in cub_ids:
                                if cub['active'] == False:
                                    activocub = 0
                                else:
                                    activocub = 1
                                insertcub =  "INSERT OR REPLACE INTO  cuenta_bancaria (id_servidor,nombre,active) VALUES (" + str(
                                    cub['id']) + ",'" + str(cub['name']) + "'," + str(activocub) + ")"
                                listacub.append(insertcub)
                            valscub = {
                                'update': 'true',
                                'db_cuentas_bancarias_last_mod_date_count': new_cat_cub,
                                'qrys': listacub
                            }
                        else:
                            print("entro al else")
                            valscub = {
                                'update': 'false'
                            }

                ####################PRECIO DE LISTA PARA PRODUCTOS###########################
                if post.get('CAT_PPRE') is None or  post.get('CAT_PPRE') == '':
                    ppremx = odoo.SearchRead('product.pricelist.item', [], ['id', 'write_date'])
                    v9 = True
                    maxppre = ''
                    for ppr in ppremx:
                        if v9 == True:
                            maxppre = ppr['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v9 = False
                        else:
                            if ppr['write_date'] > maxppre:
                                maxppre = ppr['write_date']

                    print("valor maximo de  precio de lista de productos")
                    print(maxppre)
                    contmaxppre = odoo.SearchCount('product.pricelist.item',
                                                   [('write_date', '>=', str(maxppre) + '.0'),
                                                    ('write_date', '<=', str(maxppre) + '.99')])
                    print("contador maximo precio lista de productos")
                    print(contmaxppre)
                    new_cat_ppre = str(maxppre) + ' ' + str(contmaxppre)
                    print(new_cat_ppre)
                    contppre = odoo.SearchCount('product.pricelist.item',
                                                [('product_tmpl_id', '!=', False)])

                    ppre_ids = odoo.SearchRead('product.pricelist.item', [('product_tmpl_id', '!=', False)],
                                               ['id', 'pricelist_id', 'product_tmpl_id', 'price_discount'])
                    datappre = str(post.get('CAT_PPRE') + ' ') + str(contppre)
                    if contppre > 0:
                        for ppre in ppre_ids:
                            listaprecio = ''
                            activoppre = 1
                            producto = ''
                            valor3 = True
                            for c in ppre['pricelist_id']:
                                if valor3 == True:
                                    listaprecio = c
                                    valor3 = False

                            valor4 = True
                            for t in ppre['product_tmpl_id']:
                                if valor4 == True:
                                    producto = t
                                    valor4 = False
                            insertppre = "INSERT OR REPLACE INTO producto_precio_lista (id_producto,id_precio_lista,precio,active) VALUES (" + str(
                                producto) + ",'" + str(listaprecio) + "','" + str(ppre['price_discount']) + "','" + str(
                                activoppre) + "')"
                            listappre.append(insertppre)
                        valsppre = {
                            'update': 'true',
                            'db_precios_last_mod_date_count': new_cat_ppre,
                            'qrys': listappre
                        }
                    else:
                        print("entro al else")
                        valsppre = {
                            'update': 'false'
                        }
                else:
                    print("entro al else precio de  lista de productos")
                    if len(post.get('CAT_PPRE')) > 19:
                        print(post.get('CAT_PPRE'))
                        catppre = post.get('CAT_PPRE')[0:19]
                        print(catppre)
                        fecha_inicio_ppre = catppre + '.0'
                        print("fecha inicio %s" % fecha_inicio_ppre)
                        ppremx = odoo.SearchRead('product.pricelist.item', [], ['id', 'write_date'])
                        v9 = True
                        maxppre = ''
                        for ppr in ppremx:
                            if v9 == True:
                                maxppre = ppr['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v9 = False
                            else:
                                if ppr['write_date'] > maxppre:
                                    maxppre = ppr['write_date']

                        print("valor maximo de  precio de lista de productos")
                        print(maxppre)
                        contmaxppre = odoo.SearchCount('product.pricelist.item',
                                                       [('write_date', '>=', str(maxppre) + '.0'),
                                                        ('write_date', '<=', str(maxppre) + '.99')])
                        print("contador maximo precio lista de productos")
                        print(contmaxppre)
                        new_cat_ppre = str(maxppre) + ' ' + str(contmaxppre)
                        print(new_cat_ppre)
                        if new_cat_ppre != post.get('CAT_PPRE'):
                            contppre = odoo.SearchCount('product.pricelist.item',
                                                        [('write_date', '>=', fecha_inicio_ppre),
                                                         ('product_tmpl_id', '!=', False)])

                            ppre_ids = odoo.SearchRead('product.pricelist.item', [('write_date', '>=', fecha_inicio_ppre),
                                                                                  ('product_tmpl_id', '!=', False)],
                                                       ['id', 'pricelist_id', 'product_tmpl_id', 'price_discount'])
                            datappre = str(post.get('CAT_PPRE') + ' ') + str(contppre)
                            if contppre > 0:
                                for ppre in ppre_ids:
                                    listaprecio = ''
                                    activoppre = 1
                                    producto = ''
                                    valor3 = True
                                    for c in ppre['pricelist_id']:
                                        if valor3 == True:
                                            listaprecio = c
                                            valor3 = False

                                    valor4 = True
                                    for t in ppre['product_tmpl_id']:
                                        if valor4 == True:
                                            producto = t
                                            valor4 = False
                                    insertppre = "INSERT OR REPLACE INTO producto_precio_lista (id_producto,id_precio_lista,precio,active) VALUES (" + str(
                                        producto) + ",'" + str(listaprecio) + "','" + str(
                                        ppre['price_discount']) + "','" + str(activoppre) + "')"
                                    listappre.append(insertppre)
                                valsppre = {
                                    'update': 'true',
                                    'db_precios_last_mod_date_count': new_cat_ppre,
                                    'qrys': listappre
                                }
                            else:
                                print("entro al else")
                                valsppre = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valsppre = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_ppre = post.get('CAT_PPRE') + '.0'
                        print("fecha inicio %s" % fecha_inicio_ppre)
                        ppremx = odoo.SearchRead('product.pricelist.item', [], ['id', 'write_date'])
                        v9 = True
                        maxppre = ''
                        for ppr in ppremx:
                            if v9 == True:
                                maxppre = ppr['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v9 = False
                            else:
                                if ppr['write_date'] > maxppre:
                                    maxppre = ppr['write_date']

                        print("valor maximo de  precio de lista de productos")
                        print(maxppre)
                        contmaxppre = odoo.SearchCount('product.pricelist.item',
                                                      [('write_date', '>=', str(maxppre) + '.0'),
                                                       ('write_date', '<=', str(maxppre) + '.99')])
                        print("contador maximo precio lista de productos")
                        print(contmaxppre)
                        new_cat_ppre = str(maxppre) + ' ' + str(contmaxppre)
                        print(new_cat_ppre)
                        contppre = odoo.SearchCount('product.pricelist.item',
                                                    [('write_date', '>=', fecha_inicio_ppre),('product_tmpl_id','!=',False)])

                        ppre_ids = odoo.SearchRead('product.pricelist.item', [('write_date', '>=', fecha_inicio_ppre),('product_tmpl_id','!=',False)],
                                                   ['id', 'pricelist_id', 'product_tmpl_id', 'price_discount'])
                        datappre = str(post.get('CAT_PPRE') + ' ') + str(contppre)
                        if contppre > 0:
                            for ppre in ppre_ids:
                                listaprecio=''
                                activoppre = 1
                                producto=''
                                valor3=True
                                for c in ppre['pricelist_id']:
                                    if valor3==True:
                                        listaprecio=c
                                        valor3=False

                                valor4=True
                                for t in ppre['product_tmpl_id']:
                                    if valor4==True:
                                        producto=t
                                        valor4=False
                                insertppre =  "INSERT OR REPLACE INTO producto_precio_lista (id_producto,id_precio_lista,precio,active) VALUES (" + str(producto) + ",'" + str(listaprecio) + "','" + str(ppre['price_discount']) + "','" + str(activoppre) + "')"
                                listappre.append(insertppre)
                            valsppre = {
                                'update': 'true',
                                'db_precios_last_mod_date_count': new_cat_ppre,
                                'qrys': listappre
                            }
                        else:
                            print("entro al else")
                            valsppre = {
                                'update': 'false'
                            }


                #####################MOTIVOS###########################
                if post.get('CAT_MO') is None or post.get('CAT_MO') == '':
                    momx = odoo.SearchRead('reason.rejection', [], ['id', 'write_date'])
                    v10 = True
                    maxmo = ''
                    for mmo in momx:
                        if v10 == True:
                            maxmo = mmo['write_date']
                            # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                            v10 = False
                        else:
                            if mmo['write_date'] > maxmo:
                                maxmo = mmo['write_date']

                    print("valor maximo de motivos")
                    print(maxmo)
                    contmaxmo = odoo.SearchCount('reason.rejection',
                                                 [('write_date', '>=', str(maxmo) + '.0'),
                                                  ('write_date', '<=', str(maxmo) + '.99')])
                    print("contador maximo motivos")
                    print(contmaxmo)
                    new_cat_mo = str(maxmo) + ' ' + str(contmaxmo)
                    print(new_cat_mo)
                    contmo = odoo.SearchCount('reason.rejection', [])

                    mo_ids = odoo.SearchRead('reason.rejection', [],
                                             ['id', 'name', 'active'])
                    datamo = str(post.get('CAT_MO') + ' ') + str(contmo)
                    if contmo > 0:
                        for mo in mo_ids:
                            activomo = 1
                            insertmo = "INSERT OR REPLACE INTO motivo (id_servidor,nombre,active) VALUES (" + str(
                                mo['id']) + ",'" + str(mo['name']) + "'," + str(activomo) + ")"
                            listamo.append(insertmo)
                        valsmo = {
                            'update': 'true',
                            'db_motivos_last_mod_date_count': new_cat_mo,
                            'qrys': listamo
                        }
                    else:
                        print("entro al else")
                        valsmo = {
                            'update': 'false'
                        }
                else:
                    print("entro al else de  motivos")
                    if len(post.get('CAT_MO')) > 19:
                        print(post.get('CAT_MO'))
                        catmo = post.get('CAT_MO')[0:19]
                        print(catmo)
                        fecha_inicio_mo  = catmo + '.0'
                        print("fecha inicio %s" % fecha_inicio_mo)
                        momx = odoo.SearchRead('reason.rejection', [], ['id', 'write_date'])
                        v10 = True
                        maxmo = ''
                        for mmo in momx:
                            if v10 == True:
                                maxmo = mmo['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v10 = False
                            else:
                                if mmo['write_date'] > maxmo:
                                    maxmo = mmo['write_date']

                        print("valor maximo de motivos")
                        print(maxmo)
                        contmaxmo = odoo.SearchCount('reason.rejection',
                                                     [('write_date', '>=', str(maxmo) + '.0'),
                                                      ('write_date', '<=', str(maxmo) + '.99')])
                        print("contador maximo motivos")
                        print(contmaxmo)
                        new_cat_mo = str(maxmo) + ' ' + str(contmaxmo)
                        print(new_cat_mo)
                        if new_cat_mo != post.get('CAT_MO'):
                            contmo = odoo.SearchCount('reason.rejection',
                                                      [('write_date', '>=', fecha_inicio_mo)])

                            mo_ids = odoo.SearchRead('reason.rejection', [('write_date', '>=', fecha_inicio_mo)],
                                                     ['id', 'name', 'active'])
                            datamo = str(post.get('CAT_MO') + ' ') + str(contmo)
                            if contmo > 0:
                                for mo in mo_ids:
                                    activomo = 1
                                    insertmo = "INSERT OR REPLACE INTO motivo (id_servidor,nombre,active) VALUES (" + str(
                                        mo['id']) + ",'" + str(mo['name']) + "'," + str(activomo) + ")"
                                    listamo.append(insertmo)
                                valsmo = {
                                    'update': 'true',
                                    'db_motivos_last_mod_date_count': new_cat_mo,
                                    'qrys': listamo
                                }
                            else:
                                print("entro al else")
                                valsmo = {
                                    'update': 'false'
                                }
                        else:
                            print("entro al else")
                            valsmo = {
                                'update': 'false'
                            }
                    else:
                        fecha_inicio_mo = post.get('CAT_MO') + '.0'
                        print("fecha inicio %s" % fecha_inicio_mo)
                        momx = odoo.SearchRead('reason.rejection', [], ['id', 'write_date'])
                        v10 = True
                        maxmo = ''
                        for mmo in momx:
                            if v10 == True:
                                maxmo = mmo['write_date']
                                # datetime.strptime(part['write_date'], '%Y-%m-%d %H:%M:%S')
                                v10 = False
                            else:
                                if mmo['write_date'] > maxmo:
                                    maxmo = mmo['write_date']

                        print("valor maximo de motivos")
                        print(maxmo)
                        contmaxmo = odoo.SearchCount('reason.rejection',
                                                       [('write_date', '>=', str(maxmo) + '.0'),
                                                        ('write_date', '<=', str(maxmo) + '.99')])
                        print("contador maximo motivos")
                        print(contmaxmo)
                        new_cat_mo = str(maxmo) + ' ' + str(contmaxmo)
                        print(new_cat_mo)
                        contmo = odoo.SearchCount('reason.rejection',
                                                  [('write_date', '>=', fecha_inicio_mo)])

                        mo_ids = odoo.SearchRead('reason.rejection', [('write_date', '>=', fecha_inicio_mo)],
                                                 ['id', 'name', 'active'])
                        datamo = str(post.get('CAT_MO') + ' ') + str(contmo)
                        if contmo >0:
                            for mo in mo_ids:
                                activomo = 1
                                insertmo =  "INSERT OR REPLACE INTO motivo (id_servidor,nombre,active) VALUES (" + str(
                                    mo['id']) + ",'" + str(mo['name']) + "'," + str(activomo) + ")"
                                listamo.append(insertmo)
                            valsmo = {
                                'update': 'true',
                                'db_motivos_last_mod_date_count': new_cat_mo,
                                'qrys': listamo
                            }
                        else:
                            print("entro al else")
                            valsmo = {
                                'update': 'false'
                            }
                #####################ORDENES###########################
                #if post.get('E') is None or post.get('E') == '':
                #    print("no hay ordenes de ventas")
                #else:
                #    post.get('E')
                #    orden_id = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio_mo)],
                #                         ['id', 'property_product_pricelist', 'active'])
                #    l={}
                #    for orden in orden_id:
                #        dirfac= odoo.SearchRead('res.partner', [('id', '==', orden['id']),('type', '==','invoice')],
                #                                   ['id'])
                #        deli = odoo.SearchRead('res.partner', [('id', '==', orden['id']), ('type', '==', 'delivery')],
                #                                 ['id'])
                #        bank = odoo.SearchRead('res.partner.bank', [('id', '==', orden['id'])],
                #                               ['id'])

                #        valsorden = {
                #            'id': str(orden['id']),
                #            'id_cliente': str(orden['id']),
                #            'id_dir_facturacion':str(dirfac['id']),
                #            'id_dir_entrega':str(deli['id']),
                #            'fecha_caducidad':'',
                #            'id_tarifa':str(orden['property_product_pricelist']),
                #            'id_plazo_pago':'',
                #            'id_cuenta_bancaria':str(bank['id']),
                #            'agendada':str(orden['date']),
                #        }
                #        l.update(valsorden)

                #    valsordenes = {
                #        'update': 'true',
                #        'md5': datamo,
                #        'qrys': [l]
                #    }
            valsmep = {
                        'update': 'false'
                    }
            valspromocion ={
                        'update': 'false'
                    }
            valores={
                'clientes':vals,
                'clientes_dirs': valscld,
                'productos': valsproduct,
                'estados': valsstate,
                'paises':valspaises,
                'tarifas':valstarifa,
                'plazas_pago':valsplp,
                'metodos_pago':valsmep,
                'cuentas_bancarias':valscub,
                'precios': valsppre,
                'motivos':valsmo,
                'promociones' : valspromocion
            }
            json_datos['datos'].append(valores)
            datos = {
                        'datos': valores
                    }

            lista.clear()
        return json.dumps(datos)

