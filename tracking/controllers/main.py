# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
from .odooclient import client
import json
import time

_logger = logging.getLogger(__name__)
lista=[]
xl =dict()
pwd_admin='admin'
class trackController(http.Controller):
    #parameter = {CAT_CL=2017-10-09 16:47:55,"CAT_PR":'-'}
    #http://localhost:8069/track/SYNC?CAT_CL=2017-10-13%2016:47:55&CAT_CLD=2017-10-10%2016:47:55&CAT_P=2017-10-13%2016:47:55&CAT_ES=2017-10-13%2016:47:55&CAT_PA=2017-10-13%2016:47:55&CAT_PLP=2017-10-13%2016:47:55&CAT_TA=2017-10-13%2016:47:55&CAT_PLP=2017-10-13%2016:47:55&CAT_CUB=2017-10-13%2016:47:55
    #localhost:8069/track/login?BD=web&N=admin&P=admin&DTO=Samsung gt8&DTY=0&E=SAMSUNG GT8&V=3.3


    @http.route('/track/login',type='http', auth='public', methods=['POST'], website=True,csrf = False)
    def loginlxtrack(self, **post):
        print(request.session.uid)
        if 'BD' in post and 'N' in post and 'P' in post:
            print("entro aqui")
            odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=post.get('BD'), port=8069,debug=True)
            odoo.ServerInfo()
            print("hola")
            uid= odoo.Authenticate('admin', 'admin')
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
                                "id_session_app": uid,
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
                return '{"​ error​ ":"DB"}'
        else:
            return '{"​ error​ ": "INVALID"}'

    @http.route('/track/sync', type='http', auth='public', methods=['POST'], website=True,csrf = False)
    def track_web(self, **post):
        print("valor sync")
        print(xl)
        odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname=xl.get('BD'), port=8069, debug=True)
        odoo.ServerInfo()
        odoo.Authenticate('admin', pwd_admin)
        if odoo.Authenticate('admin', pwd_admin) is not False or None:
            json_list = {
                'clientes': [],
                'clientes_dirs': [],
                'productos': [],
                'estados': [],
                'paises': [],
                'tarifas': [],
                'plazos_pago': [],
                'metodos_pago': [],
                'cuentas_bancarias': [],
                'precios': [],
                'motivos': [],

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

            if 'CAT_CL' in post or 'CAT_CLD' in post or 'CAT_P' in post or 'CAT_ES' in post or 'CAT_PA' in post or 'CAT_PLP' in post or 'CAT_TA' in post or 'CAT_PLP' in post or 'CAT_CUB' in post or 'CAT_PPRE' in post:
                ####################CLIENTES#####################################
                fecha_inicio = post.get('CAT_CL') + '.0'
                print("fecha inicio %s" % fecha_inicio)
                cont = odoo.SearchCount('res.partner',
                                        [('write_date', '>=', fecha_inicio)])

                partners = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio)],
                                           ['name', 'display_name', 'website', 'function', 'phone', 'mobile', 'email',
                                            'active'])
                data = str(post.get('CAT_CL') + ' ') + str(cont)
                if partners is not None:
                    for p in partners:
                        if str(p['active']) == False:
                            activo = 0
                        else:
                            activo = 1

                        insertcliente = insertcliente + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES((select id from cliente where id_servidor='" + str(
                            p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(
                            p['display_name']) + "','" + str(p['website']) + "','" + str(p['function']) + "','" + str(
                            p['phone']) + "','" + str(p['mobile']) + "','','" + str(p['email']) + "','" + str(
                            1) + "','" + str(activo) + "');"
                vals = {
                    data: insertcliente
                }
                #################### DIRECCION CLIENTES############################
                fecha_inicio_cld = post.get('CAT_CLD') + '.0'
                print("fecha inicio %s" % fecha_inicio_cld)
                contcld = odoo.SearchCount('res.partner',
                                           [('write_date', '>=', fecha_inicio_cld)])

                partners_cld = odoo.SearchRead('res.partner', [('write_date', '>=', fecha_inicio_cld)],
                                               ['id', 'type', 'street', 'city', 'state_id', 'zip', 'country_id',
                                                'email', 'phone', 'mobile', 'parent_id'])
                data_cld = str(post.get('CAT_CLD') + ' ') + str(contcld)
                if partners_cld is not None:
                    for pcl in partners_cld:
                        activo_cld = 1
                        if pcl['parent_id']:
                            pclid = pcl['parent_id']
                        else:
                            pclid = pcl['id']

                        insertcliente_cld = insertcliente_cld + "INSERT OR REPLACE INTO cliente_direccion(id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES((select  id from cliente_direccion where id_servidor ='" + str(
                            pcl['id']) + "'),'" + str(
                            pcl['id']) + "', (select id from cliente where id_servidor ='" + str(pclid) + "'),'" + str(
                            pclid) + "','" + str(pcl['type']) + "','" + str(pcl['street']) + "',''," + "'','" + str(
                            pcl['city']) + "','" + str(pcl['state_id']) + "','" + str(pcl['zip']) + "','" + str(
                            pcl['country_id']) + "','','" + str(pcl['email']) + "','" + str(pcl['phone']) + "','" + str(
                            pcl['mobile']) + "','','" + str(activo_cld) + "');"

                valscld = {
                    data_cld: insertcliente_cld
                }
                #####################PRODUCTOS###########################
                fecha_inicio_p = post.get('CAT_P') + '.0'
                print("fecha inicio %s" % fecha_inicio_p)
                contp = odoo.SearchCount('product.product',
                                         [('write_date', '>=', fecha_inicio_p)])

                product = odoo.SearchRead('product.product', [('write_date', '>=', fecha_inicio_p)],
                                          ['id', 'default_code', 'name', 'description', 'list_price', 'uom_id',
                                           'active'])
                data_pr = str(post.get('CAT_P') + ' ') + str(contp)
                if product is not None:
                    for pr in product:
                        if str(pr['active']) == False:
                            activop = 0
                        else:
                            activop = 1
                        insertproduct = insertproduct + "INSERT OR REPLACE INTO producto(id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES('" + str(
                            pr['id']) + "','" + str(pr['default_code']) + "','" + str(pr['name']) + "','" + str(
                            pr['description']) + "','" + str(pr['list_price']) + "','" + str(
                            pr['uom_id']) + "', '" + str(activop) + "');"
                valsproduct = {
                    data_pr: insertproduct
                }
                #####################Estados###########################
                fecha_inicio_state = post.get('CAT_ES') + '.0'
                print("fecha inicio %s" % fecha_inicio_state)
                contstate = odoo.SearchCount('res.country.state',
                                             [('write_date', '>=', fecha_inicio_state)])

                state_ids = odoo.SearchRead('res.country.state', [('write_date', '>=', fecha_inicio_state)],
                                            ['id', 'country_id', 'name', 'active'])
                datastate = str(post.get('CAT_ES') + ' ') + str(contstate)
                if state_ids is not None:
                    for state in state_ids:
                        activostate = 1
                        insertstate = insertstate + "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES('" + str(
                            state['id']) + "','" + str(state['country_id']) + "','" + str(state['name']) + "','" + str(
                            activostate) + "');"

                valsstate = {
                    datastate: insertstate
                }
                #####################Paises###########################
                fecha_inicio_pais = post.get('CAT_PA') + '.0'
                print("fecha inicio %s" % fecha_inicio_pais)
                contpais = odoo.SearchCount('res.country',
                                            [('write_date', '>=', fecha_inicio_pais)])

                pais_ids = odoo.SearchRead('res.country', [('write_date', '>=', fecha_inicio_pais)],
                                           ['id', 'name', 'active'])
                datapais = str(post.get('CAT_PA') + ' ') + str(contpais)
                if pais_ids is not None:
                    for pais in pais_ids:
                        activopais = 1
                        insertpais = insertpais + "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES(" + str(
                            pais['id']) + ",'" + str(pais['name']) + "'," + str(activopais) + ");"

                valspaises = {
                    datapais: insertpais
                }
                #####################TARIFAS###########################
                fecha_inicio_tarifa = post.get('CAT_TA') + '.0'
                print("fecha inicio %s" % fecha_inicio_tarifa)
                conttarifa = odoo.SearchCount('product.pricelist',
                                              [('write_date', '>=', fecha_inicio_tarifa)])

                tarifa_ids = odoo.SearchRead('product_pricelist', [('write_date', '>=', fecha_inicio_tarifa)],
                                             ['id', 'name', 'active'])
                print("valor de tarifas")
                print(tarifa_ids)
                datatarifa = str(post.get('CAT_TA') + ' ') + str(conttarifa)
                if tarifa_ids is not None:
                    for tarifa in tarifa_ids:
                        if tarifa['active'] == False:
                            activotarifa = 0
                        else:
                            activotarifa = 1
                        inserttarifa = inserttarifa + "INSERT OR REPLACE INTO tarifa(id_servidor,nombre,active) VALUES(" + str(
                            tarifa['id']) + ",'" + str(tarifa['name']) + "'," + str(activotarifa) + ");"

                valstarifa = {
                    datatarifa: inserttarifa
                }
                ####################PLAZOS DE PAGO###########################
                fecha_inicio_plp = post.get('CAT_PLP') + '.0'
                print("fecha inicio %s" % fecha_inicio_plp)
                contplp = odoo.SearchCount('account.payment.term',
                                           [('write_date', '>=', fecha_inicio_plp)])

                plp_ids = odoo.SearchRead('account.payment.term', [('write_date', '>=', fecha_inicio_plp)],
                                          ['id', 'name', 'active'])
                dataplp = str(post.get('CAT_PLP') + ' ') + str(contplp)
                if plp_ids is not None:
                    for plp in plp_ids:
                        if plp['active'] == False:
                            activoplp = 0
                        else:
                            activoplp = 1
                        insertplp = insertplp + "INSERT OR REPLACE INTO ​plaza_pago(id_servidor,nombre,active) VALUES(" + str(
                            plp['id']) + ",'" + str(plp['name']) + "'," + str(activoplp) + ");"

                valsplp = {
                    dataplp: insertplp
                }
                ####################METODO DE PAGO###########################
                # fecha_inicio_mep = post.get('CAT_MEP') + '.0'
                # print("fecha inicio %s" % fecha_inicio_mep)
                # contmep = odoo.SearchCount('account.payment.term',
                #                           [('write_date', '>=', fecha_inicio_mep)])

                # mep_ids = odoo.SearchRead('account.payment.term', [('write_date', '>=', fecha_inicio_mep)],
                #                          ['id', 'name', 'active'])
                # datamep = str(post.get('CAT_MEP') + ' ') + str(contmep)

                # for mep in mep_ids:
                #    if mep['active'] == False:
                #        activomep = 0
                #    else:
                #        activomep = 1
                #    insertmep = insertmep + "INSERT OR REPLACE INTO ​plaza_pago(id_servidor,nombre,active) VALUES(" + str(
                #        plp['id']) + ",'" + str(plp['name']) + "'," + str(activoplp) + ");"

                # valsmep = {
                #    datamep: insertmep
                # }
                ####################CUENTAS BANCARIAS###########################
                fecha_inicio_cub = post.get('CAT_CUB') + '.0'
                print("fecha inicio %s" % fecha_inicio_cub)
                contcub = odoo.SearchCount('res.bank',
                                           [('write_date', '>=', fecha_inicio_cub)])

                cub_ids = odoo.SearchRead('res.bank', [('write_date', '>=', fecha_inicio_cub)],
                                          ['id', 'name', 'active'])
                datacub = str(post.get('CAT_CUB') + ' ') + str(contcub)
                if cub_ids is not None:
                    for cub in cub_ids:
                        if cub['active'] == False:
                            activocub = 0
                        else:
                            activocub = 1
                        insertcub = insertcub + "INSERT OR REPLACE INTO ​plaza_pago(id_servidor,nombre,active) VALUES(" + str(
                            cub['id']) + ",'" + str(cub['name']) + "'," + str(activocub) + ");"

                valscub = {
                    datacub: insertcub
                }
                ####################PRECIO DE LISTA PARA PRODUCTOS###########################
                fecha_inicio_ppre = post.get('CAT_PPRE') + '.0'
                print("fecha inicio %s" % fecha_inicio_ppre)
                contppre = odoo.SearchCount('product.pricelist.item',
                                            [('write_date', '>=', fecha_inicio_ppre)])

                ppre_ids = odoo.SearchRead('product.pricelist.item', [('write_date', '>=', fecha_inicio_ppre)],
                                           ['id', 'pricelist_id', 'product_tmpl_id', 'price_discount' 'active'])
                datappre = str(post.get('CAT_PPRE') + ' ') + str(contppre)
                if ppre_ids is not None:
                    for ppre in ppre_ids:
                        #if ppre['active'] == False:
                        #activoppre = 0
                        #else:
                        activoppre = 1
                        insertppre = insertppre + "INSERT OR REPLACE INTO producto_precio_lista(id_producto,id_precio_lista,precio,active) VALUES(" + str(
                            ppre['product_tmpl_id']) + ",'" + str(ppre['pricelist_id']) + "','" + str(
                            ppre['price_discount']) + "','" + str(activoppre) + "');"

                valsppre = {
                    datappre: insertppre
                }
                #####################MOTIVOS###########################
                fecha_inicio_mo = post.get('CAT_MO') + '.0'
                print("fecha inicio %s" % fecha_inicio_mo)
                contmo = odoo.SearchCount('reason.rejection',
                                          [('write_date', '>=', fecha_inicio_mo)])

                mo_ids = odoo.SearchRead('reason.rejection', [('write_date', '>=', fecha_inicio_mo)],
                                         ['id', 'name', 'active'])
                datamo = str(post.get('CAT_MO') + ' ') + str(contmo)
                if mo_ids is not None:
                    for mo in mo_ids:
                        activomo = 1
                        insertmo = insertmo + "INSERT OR REPLACE INTO motivo (id_servidor,nombre,active) VALUES(" + str(
                            mo['id']) + ",'" + str(mo['name']) + "'," + str(activomo) + ");"

                valsmo = {
                    datamo: insertmo
                }

            else:
                cont = odoo.SearchCount('res.partner', [])

                partners = odoo.SearchRead('res.partner', [],
                                           ['name', 'display_name', 'website', 'function', 'phone', 'mobile', 'email',
                                            'active'])
                data = str(cont)
                if partners is not None:
                    for p in partners:
                        if str(p['active']) == False:
                            activo = 0
                        else:
                            activo = 1

                        insertcliente = insertcliente + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active) VALUES((select id from cliente where id_servidor='" + str(
                            p['id']) + "'), '" + str(p['id']) + "','" + str(p['name']) + "','" + str(
                            p['display_name']) + "','" + str(p['website']) + "','" + str(p['function']) + "','" + str(
                            p['phone']) + "','" + str(p['mobile']) + "','','" + str(p['email']) + "','" + str(
                            1) + "','" + str(activo) + "');"
                vals = {
                    data: insertcliente
                }
                #################### DIRECCION CLIENTES############################

                cont = odoo.SearchCount('res.partner', [])
                partners_cld = odoo.SearchRead('res.partner', [],
                                               ['id', 'type', 'street', 'city', 'state_id', 'zip', 'country_id',
                                                'email', 'phone', 'mobile', 'parent_id'])
                data_cld = str(cont)
                if partners_cld is not None:
                    for pcl in partners_cld:
                        if pcl['parent_id']:
                            pclid = pcl['parent_id']
                        else:
                            pclid = pcl['id']

                        insertcliente_cld = insertcliente_cld + "INSERT OR REPLACE INTO cliente_direccion(id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES((select  id from cliente_direccion where id_servidor ='" + str(
                            pcl['id']) + "'),'" + str(
                            pcl['id']) + "', (select id from cliente where id_servidor ='" + str(pclid) + "'),'" + str(
                            pclid) + "','" + str(pcl['type']) + "','" + str(pcl['street']) + "',''," + "'','" + str(
                            pcl['city']) + "','" + str(pcl['state_id']) + "','" + str(pcl['zip']) + "','" + str(
                            pcl['country_id']) + "','','" + str(pcl['email']) + "','" + str(pcl['phone']) + "','" + str(
                            pcl['mobile']) + "','','" + str(1) + "');"

                valscld = {
                    data_cld: insertcliente_cld
                }
                #####################PRODUCTOS###########################
                contp = odoo.SearchCount('product.product',
                                         [])

                product = odoo.SearchRead('product.product', [],
                                          ['id', 'default_code', 'name', 'description', 'list_price', 'uom_id',
                                           'active'])
                data_pr = str(contp)
                if product is not None:
                    for pr in product:
                        if str(pr['active']) == False:
                            activop = 0
                        else:
                            activop = 1
                        insertproduct = insertproduct + "INSERT OR REPLACE INTO producto(id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES('" + str(
                            pr['id']) + "','" + str(pr['default_code']) + "','" + str(pr['name']) + "','" + str(
                            pr['description']) + "','" + str(pr['list_price']) + "','" + str(
                            pr['uom_id']) + "', '" + str(
                            activop) + "');"
                valsproduct = {
                    data_pr: insertproduct
                }
                #####################Estados###########################
                contstate = odoo.SearchCount('res.country.state', [])
                state_ids = odoo.SearchRead('res.country.state', [],
                                            ['id', 'country_id', 'name', 'active'])
                datastate = str(contstate)
                if state_ids is not None:
                    for state in state_ids:
                        activostate = 1
                        insertstate = insertstate + "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES('" + str(
                            state['id']) + "','" + str(state['country_id']) + "','" + str(state['name']) + "','" + str(
                            activostate) + "');"

                valsstate = {
                    datastate: insertstate
                }
                #####################Paises###########################
                contpais = odoo.SearchCount('res.country',
                                            [])

                pais_ids = odoo.SearchRead('res.country', [],
                                           ['id', 'name', 'active'])
                datapais = str(contpais)
                if pais_ids is not None:
                    for pais in pais_ids:
                        activopais = 1
                        insertpais = insertpais + "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES(" + str(
                            pais['id']) + ",'" + str(pais['name']) + "'," + str(activopais) + ");"

                valspaises = {
                    datapais: insertpais
                }
                #####################TARIFASs###########################
                conttarifa = odoo.SearchCount('product_pricelist',
                                              [])

                tarifa_ids = odoo.SearchRead('product_pricelist', [],
                                             ['id', 'name', 'active'])
                datatarifa = str(conttarifa)
                if tarifa_ids is not None:
                    for tarifa in tarifa_ids:
                        if tarifa['active'] == False:
                            activotarifa = 0
                        else:
                            activotarifa = 1
                        inserttarifa = inserttarifa + "INSERT OR REPLACE INTO tarifa(id_servidor,nombre,active) VALUES(" + str(
                            tarifa['id']) + ",'" + str(tarifa['name']) + "'," + str(activotarifa) + ");"

                valstarifa = {
                    datatarifa: inserttarifa
                }
                ####################PLAZOS DE PAGO###########################
                contplp = odoo.SearchCount('account.payment.term', [])
                plp_ids = odoo.SearchRead('account.payment.term', [],
                                          ['id', 'name', 'active'])
                dataplp = str(contplp)
                if plp_ids is not None:
                    for plp in plp_ids:
                        if plp['active'] == False:
                            activoplp = 0
                        else:
                            activoplp = 1
                        insertplp = insertplp + "INSERT OR REPLACE INTO ​plaza_pago(id_servidor,nombre,active) VALUES(" + str(
                            plp['id']) + ",'" + str(plp['name']) + "'," + str(activoplp) + ");"

                valsplp = {
                    dataplp: insertplp
                }
                ####################CUENTAS BANCARIAS###########################
                contcub = odoo.SearchCount('res.bank',
                                           [])

                cub_ids = odoo.SearchRead('res.bank', [],
                                          ['id', 'name', 'active'])
                datacub = str(contcub)
                if cub_ids is not None:
                    for cub in cub_ids:
                        if cub['active'] == False:
                            activocub = 0
                        else:
                            activocub = 1
                        insertcub = insertcub + "INSERT OR REPLACE INTO ​plaza_pago(id_servidor,nombre,active) VALUES(" + str(
                            cub['id']) + ",'" + str(cub['name']) + "'," + str(activocub) + ");"

                valscub = {
                    datacub: insertcub
                }

                #####################MOTIVOS###########################
                contmo = odoo.SearchCount('reason.rejection',
                                          [])

                mo_ids = odoo.SearchRead('reason.rejection', [],
                                         ['id', 'name', 'active'])
                datamo = str(contmo)
                if mo_ids is not None:
                    for mo in mo_ids:
                        activomo = 1
                        insertmo = insertmo + "INSERT OR REPLACE INTO motivo (id_servidor,nombre,active) VALUES(" + str(
                            mo['id']) + ",'" + str(mo['name']) + "'," + str(activomo) + ");"

                valsmo = {
                    datamo: insertmo
                }


            json_list['clientes'].append(vals)
            json_list['clientes_dirs'].append(valscld)
            json_list['productos'].append(valsproduct)
            json_list['estados'].append(valsstate)
            json_list['paises'].append(valspaises)
            json_list['tarifas'].append(valstarifa)
            json_list['plazos_pago'].append(valstarifa)
            json_list['metodos_pago'].append(valsmep)
            json_list['cuentas_bancarias'].append(valscub)
            json_list['precios'].append(valsppre)
            json_list['motivos'].append(valsmo)
            lista.clear()
        return json.dumps(json_list)

