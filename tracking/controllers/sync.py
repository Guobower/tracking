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
                print("CL VALOR")
                print(post.get('CAT_CL'))
                if post.get('CAT_CL') is None or post.get('CAT_CL') == '':
                    vals = {
                        'update': 'false'
                    }
                else:
                    partnersmx = odoo.SearchRead('res.partner', [],
                                               ['id', 'write_date'])
                    v1=True
                    maxpartner=''
                    for part in partnersmx:
                        if v1==True:
                            maxpartner=datetime.strptime(part['write_date'],'%Y-%m-%d %H:%M:%S')
                            v1=False
                        else:
                            if datetime.strptime(part['write_date'],'%Y-%m-%d %H:%M:%S') > maxpartner:
                                maxpartner=datetime.strptime(part['write_date'],'%Y-%m-%d %H:%M:%S')
                    print("valor maximo de fecha")
                    print(maxpartner)

                    fecha_inicio=''
                    print("valor de cl")
                    print(len(post.get('CAT_CL')) )
                    print("valor de cld")
                    print(len(post.get('CAT_CLD')))
                    if len(post.get('CAT_CL'))>19:
                        d=post.get('CAT_CL')[0:19]
                        fecha_inicio=d + '.0'
                        print(fecha_inicio)
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
                    if cont >0:
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
                            'db_clientes_last_mod_date_count': data,
                            'qrys': listacliente
                        }
                    else:
                        print("entro al else")
                        vals = {
                            'update': 'false'
                        }

                #################### DIRECCION CLIENTES############################
                if post.get('CAT_CLD') is  None or post.get('CAT_CLD')== '':
                    valscld = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_cld = post.get('CAT_CLD') + '.0'
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
                            'db_clientes_dirs_last_mod_date_count': data_cld,
                            'qrys': listadirecciones
                        }

                    else:
                        print("entro al else")
                        valscld = {
                            'update': 'false'
                        }


                #####################PRODUCTOS###########################
                if post.get('CAT_P') is  None or post.get('CAT_P')== '':
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
                            'db_productos_last_mod_date_count': data_pr,
                            'qrys': listaproductos
                        }
                    else:
                        print("entro al else")
                        valsproduct = {
                            'update': 'false'
                        }

                #####################Estados###########################
                if post.get('CAT_ES') is None or post.get('CAT_ES')==  '':
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
                            'db_estados_last_mod_date_count': datastate,
                            'qrys': listastate
                        }
                    else:
                        print("entro al else")
                        valsstate = {
                            'update': 'false'
                        }

                #####################Paises###########################
                if post.get('CAT_PA') is None or post.get('CAT_PA') == '':
                    print("entro al else")
                    valspaises = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_pais = post.get('CAT_PA') + '.0'
                    print("fecha inicio %s" % fecha_inicio_pais)
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
                            'db_paises_last_mod_date_count': datapais,
                            'qrys': listapais
                        }
                    else:
                        print("entro al else")
                        valspaises = {
                            'update': 'false'
                        }
                #####################TARIFAS###########################
                if post.get('CAT_TA') is None or post.get('CAT_TA') == '':
                    print("entro al else")
                    valstarifa = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_tarifa = post.get('CAT_TA') + '.0'
                    print("fecha inicio %s" % fecha_inicio_tarifa)
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
                            'db_tarifas_last_mod_date_count': datatarifa,
                            'qrys': listatarifa
                        }
                    else:
                        print("entro al else")
                        valstarifa = {
                            'update': 'false'
                        }

                ####################PLAZOS DE PAGO###########################
                if post.get('CAT_PLP') is  None or post.get('CAT_PLP') ==  '':
                    valsplp = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_plp = post.get('CAT_PLP') + '.0'
                    print("fecha inicio %s" % fecha_inicio_plp)
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
                            'db_plazas_pago_last_mod_date_count': dataplp,
                            'qrys': listaplp
                        }
                    else:
                        print("entro al else")
                        valsplp = {
                            'update': 'false'
                        }

                ####################CUENTAS BANCARIAS###########################
                if post.get('CAT_CUB') is  None or post.get('CAT_CUB') == '':
                    valscub = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_cub = post.get('CAT_CUB') + '.0'
                    print("fecha inicio %s" % fecha_inicio_cub)
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
                            'db_cuentas_bancarias_last_mod_date_count': datacub,
                            'qrys': listacub
                        }
                    else:
                        print("entro al else")
                        valscub = {
                            'update': 'false'
                        }

                ####################PRECIO DE LISTA PARA PRODUCTOS###########################
                if post.get('CAT_PPRE') is None or  post.get('CAT_PPRE') == '':
                    valsppre = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_ppre = post.get('CAT_PPRE') + '.0'
                    print("fecha inicio %s" % fecha_inicio_ppre)
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
                            'db_cuentas_bancarias_last_mod_date_count': datappre,
                            'qrys': listappre
                        }
                    else:
                        print("entro al else")
                        valsppre = {
                            'update': 'false'
                        }


                #####################MOTIVOS###########################
                if post.get('CAT_MO') is None or post.get('CAT_MO') == '':
                    valsmo = {
                        'update': 'false'
                    }
                else:
                    fecha_inicio_mo = post.get('CAT_MO') + '.0'
                    print("fecha inicio %s" % fecha_inicio_mo)
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
                            'db_motivos_last_mod_date_count': datamo,
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

