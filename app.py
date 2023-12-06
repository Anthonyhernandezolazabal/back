from flask import Flask,request,jsonify
import psycopg2
from flask_cors import CORS
from conexion import db, init_db
from datetime import datetime
from sqlalchemy import func
app = Flask(__name__)

HOST = "127.0.0.1"
PORT = 5000

# Inicializa la extensión CORS
cors = CORS(app, resources={
    r"/api/v1/*": {
        "origins": ["*"],
        "methods": "GET, POST, OPTIONS",
        "allow_headers": "Authorization, Content-Type"
    }
})
cors = CORS(app) #intercambio de recursos de origen cruzado (FrontEnd al Backend)

init_db(app)



class in_usuario(db.Model):
    us_id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    us_nombre       = db.Column(db.String(100))
    us_username     = db.Column(db.String(50), unique=True)
    us_email        = db.Column(db.String(100), unique=True)
    us_password     = db.Column(db.String(100))
    us_codigo       = db.Column(db.String(100))
    us_rol          = db.Column(db.String(50))


class in_categoria(db.Model):
    cat_id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_nombre          = db.Column(db.String(255))
    cat_descripcion     = db.Column(db.String(255))
    cat_estado          = db.Column(db.Integer)

class in_producto(db.Model):
    prod_id              = db.Column(db.Integer, primary_key=True,autoincrement=True)
    prod_codigo          = db.Column(db.String(255))
    prod_nombre          = db.Column(db.String(255))
    prod_precio          = db.Column(db.Numeric)
    prod_cantidad        = db.Column(db.Integer)
    prod_cat_id          = db.Column(db.Integer, db.ForeignKey('in_categoria.cat_id'))
    prod_estado          = db.Column(db.Integer)
    prod_fecha_registro  = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    para_lamina         = db.Column(db.Integer)
    para_rafia          = db.Column(db.Integer)

    
class in_proveedor(db.Model):
    prov_id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prov_nombre     = db.Column(db.String(255))
    prov_telefono   = db.Column(db.String(20))
    prov_ruc        = db.Column(db.String(20))
    prov_correo     = db.Column(db.String(255))
    prov_estado     = db.Column(db.Integer)

class parametroadmin(db.Model):
    para_id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    para_cadena1        = db.Column(db.String(255))
    para_cadena2        = db.Column(db.String(20))
    para_fecha1         = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    para_fecha2         = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    para_int1           = db.Column(db.Integer)
    para_int2           = db.Column(db.Integer)
    para_correlativo    = db.Column(db.Integer, default=0)
    para_prefijo        = db.Column(db.Integer, default=0)
    para_estado         = db.Column(db.Integer, default=0)

class in_venta(db.Model):
    vent_id         = db.Column(db.Integer, primary_key=True)
    vent_usuario    = db.Column(db.Integer, nullable=False)
    vent_cliente    = db.Column(db.Integer, nullable=False)
    vent_direccion  = db.Column(db.String(255), nullable=False)
    vent_fecha      = db.Column(db.Date, nullable=False)
    vent_total      = db.Column(db.Numeric(10, 2), nullable=False)
    vent_igv        = db.Column(db.Numeric(10, 2), nullable=False)
    vent_subtotal   = db.Column(db.Numeric(10, 2), nullable=False)

class in_ventadetalle(db.Model):
    vent_det_id         = db.Column(db.Integer, primary_key=True)
    vent_det_vent_id    = db.Column(db.Integer, db.ForeignKey('in_venta.vent_id'), nullable=False)
    vent_item           = db.Column(db.Numeric(10, 2), nullable=False)
    vent_cantidad       = db.Column(db.Numeric(10, 2), nullable=False)
    vent_unidad         = db.Column(db.String(255), nullable=False)
    vent_producto       = db.Column(db.String(255), nullable=False)
    vent_valor          = db.Column(db.Numeric(10, 2), nullable=False)
    vent_subtotal       = db.Column(db.Numeric(10, 2), nullable=False)

class in_clientes(db.Model):
    cl_id           = db.Column(db.Integer, primary_key=True)
    cl_nombre       = db.Column(db.String(255), nullable=False)
    cl_doc          = db.Column(db.String(20), nullable=False)
    cl_email        = db.Column(db.String(255), nullable=True)
    cl_telefono     = db.Column(db.String(20), nullable=True)
    cl_fnacimiento  = db.Column(db.Date, nullable=True)
    cl_direccion    = db.Column(db.String(255), nullable=True)
    cl_estado       = db.Column(db.Integer, default=0)

class in_compras(db.Model):
    comp_id         = db.Column(db.Integer, primary_key=True)
    comp_usuario    = db.Column(db.Integer, db.ForeignKey('in_usuario.us_id'))
    comp_proveedor  = db.Column(db.Integer, db.ForeignKey('in_proveedor.prov_id'))
    comp_direccion  = db.Column(db.String(255), nullable=False)
    comp_fecha      = db.Column(db.Date, nullable=False)
    comp_total      = db.Column(db.Numeric(10, 2), nullable=False)
    comp_igv        = db.Column(db.Numeric(10, 2), nullable=False)
    comp_subtotal   = db.Column(db.Numeric(10, 2), nullable=False)

class in_compradetalle(db.Model):
    comp_det_id         = db.Column(db.Integer, primary_key=True)
    comp_det_comp_id    = db.Column(db.Integer, db.ForeignKey('in_compras.comp_id'), nullable=False)
    comp_det_item       = db.Column(db.Numeric(10, 2), nullable=False)
    comp_det_cantidad   = db.Column(db.Numeric(10, 2), nullable=False)
    comp_det_unidad     = db.Column(db.String(255), nullable=False)
    comp_det_producto   = db.Column(db.String(255), nullable=False)
    comp_det_valor      = db.Column(db.Numeric(10, 2), nullable=False)
    comp_det_subtotal   = db.Column(db.Numeric(10, 2), nullable=False)


@app.route('/api/v1/',methods=['GET'])
def index():
    return jsonify({'Mensaje':'Bienvenido al API REST'})


# Consulta SELECT con INNER JOIN
#  resultado = db.session.query(TablaPrincipal, TablaSecundaria).join(TablaSecundaria).all()

# Consulta INNER JOIN con dos condiciones WHERE
# resultado = db.session.query(TablaPrincipal, TablaSecundaria).join(TablaSecundaria, TablaSecundaria.tabla_principal_id == TablaPrincipal.id).filter(TablaSecundaria.columna_a == valor_condicion_1, TablaSecundaria.columna_b == valor_condicion_2).all()

# Actualizar campos
# registro_a_actualizar = TablaPrincipal.query.get(id_conocido)
# registro_a_actualizar.columna_a_actualizar = nuevo_valor

# Eliminar el registro de la base de datos
# registro_a_eliminar = TablaPrincipal.query.get(id_conocido)
#db.session.delete(registro_a_eliminar)


# Ruta para autenticar un usuario
@app.route('/api/v1/login', methods=['POST'])
def login():
    data = request.json
    username = data['us_username']
    password = data['us_password']
    
    usuario = in_usuario.query.filter_by(us_username=username).first()

    if usuario and usuario.us_password == password:
        datos_user = {
            'id': usuario.us_id,
            'username': usuario.us_username,
            'email': usuario.us_email,
            'password': usuario.us_password,
            'rol': usuario.us_rol
        }
        return jsonify({'message': 0, 'data': datos_user})
    else:
        return jsonify({'message': 1})  # 1: error    0: ok
    
#================================== CATEGORIA ===================================
# Ruta para traer las categorias
@app.route('/api/v1/obtener_categorias', methods=['GET'])
def obtener_categorias():
    categorias = in_categoria.query.filter(in_categoria.cat_estado != 9).order_by(in_categoria.cat_id.desc()).all()

    resultados = []
    for categoria in categorias:
        resultados.append({
            'cat_id': categoria.cat_id,
            'cat_nombre': categoria.cat_nombre,
            'cat_descripcion': categoria.cat_descripcion,
            'cat_estado': categoria.cat_estado,
        })
    return resultados

# Ruta para traer las categorias
@app.route('/api/v1/registrar_categoria', methods=['POST'])
def registrar_categoria():
    try:
        data = request.get_json()
        nueva_categoria  = in_categoria(
            cat_nombre=data['cat_nombre'],
            cat_descripcion=data['cat_descripcion'],
            cat_estado=data['cat_estado'],
        )
        db.session.add(nueva_categoria)
        db.session.commit()

        return jsonify({'message': 'Categoría registrada exitosamente', 'est': 'success'})
        
    except Exception as e:
        
        return jsonify({'message': str(e), 'est': 'error'})


# Ruta para editar y/o eliminar una categoría
@app.route('/api/v1/editar_eliminar_categoria/<int:cat_id>/<string:accion>', methods=['PUT'])
def editar_categoria(cat_id, accion):
    try:
        # Fetch the category from the database
        categoria = in_categoria.query.get(cat_id)

        if categoria is None:
            return jsonify({'error': 'Categoría no encontrada', 'est': 'warning'})

        if accion == 'deleted':
            categoria.cat_estado = 9
            db.session.commit()
            return jsonify({'mensaje': 'Categoría eliminada exitosamente', 'est': 'success'})

        if accion == 'edit':
            data = request.get_json()
            categoria.cat_nombre        = data.get('cat_nombre', categoria.cat_nombre)
            categoria.cat_descripcion   = data.get('cat_descripcion', categoria.cat_descripcion)
            categoria.cat_estado        = data.get('cat_estado', categoria.cat_estado)

            db.session.commit()
            return jsonify({'mensaje': 'Categoría editada exitosamente', 'est': 'success'})

    except Exception as e:
        return jsonify({'message': str(e), 'est': 'error'})


#================================== PRODUCTOS ===================================
# Ruta para traer los productos
@app.route('/api/v1/obtener_productos', methods=['GET'])
def obtener_productos():
    productos = in_producto.query.filter(in_producto.prod_estado != 9).order_by(in_producto.prod_id.desc()).all()

    resultados = []
    for producto in productos:
        resultados.append({
            'prod_id'               : producto.prod_id,
            'prod_codigo'           : producto.prod_codigo,
            'prod_nombre'           : producto.prod_nombre,
            'prod_precio'           : float(producto.prod_precio),
            'prod_cantidad'         : producto.prod_cantidad,
            'prod_cat_id'           : producto.prod_cat_id,
            'prod_estado'           : producto.prod_estado,
            'prod_fecha_registro'   : producto.prod_fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
            'para_lamina'           : producto.para_lamina,
            'para_rafia'            : producto.para_rafia
        })
    return resultados

# Ruta para traer los productos
@app.route('/api/v1/registrar_producto', methods=['POST'])
def registrar_producto():
    try:
        data = request.get_json()
        nueva_producto  = in_producto(
            prod_codigo     =data['prod_codigo'],
            prod_nombre     =data['prod_nombre'],
            prod_precio     =data['prod_precio'],
            prod_cantidad   =data['prod_cantidad'],
            prod_cat_id     =data['prod_cat_id'],
            prod_estado     =data['prod_estado'],
            para_lamina     =data['para_lamina'],
            para_rafia      =data['para_rafia']
        )
        db.session.add(nueva_producto)
        db.session.commit()

        return jsonify({'message': 'Producto registrada exitosamente', 'est': 'success'})
        
    except Exception as e:
        
        return jsonify({'message': str(e), 'est': 'error'})

# Ruta para editar y/o eliminar los productos
@app.route('/api/v1/editar_eliminar_producto/<int:prod_id>/<string:accion>', methods=['PUT'])
def editar_producto(prod_id, accion):
    try:
        # Fetch the category from the database
        producto = in_producto.query.get(prod_id)

        if producto is None:
            return jsonify({'error': 'Producto no encontrada', 'est': 'warning'})

        if accion == 'deleted':
            producto.prod_estado = 9
            db.session.commit()
            return jsonify({'mensaje': 'Producto eliminado exitosamente', 'est': 'success'})

        if accion == 'edit':
            data = request.get_json()
            producto.prod_codigo    = data.get('prod_codigo', producto.prod_codigo)
            producto.prod_nombre    = data.get('prod_nombre', producto.prod_nombre)
            producto.prod_precio    = data.get('prod_precio', producto.prod_precio)
            producto.prod_cantidad  = data.get('prod_cantidad', producto.prod_cantidad)
            producto.prod_cat_id    = data.get('prod_cat_id', producto.prod_cat_id)
            producto.prod_estado    = data.get('prod_estado', producto.prod_estado)
            producto.para_lamina    = data.get('para_lamina', producto.para_lamina)
            producto.para_rafia     = data.get('para_rafia', producto.para_rafia)

            db.session.commit()
            return jsonify({'mensaje': 'Producto editado exitosamente', 'est': 'success'})

    except Exception as e:
        return jsonify({'message': str(e), 'est': 'error'})


#================================== PROVEEDORES ===================================
# Ruta para traer los proveedores
@app.route('/api/v1/registrar_proveedor', methods=['POST'])
def registrar_proveedor():
    try:
        data = request.get_json()
        nueva_proveedor  = in_proveedor(
            prov_nombre     =data['prov_nombre'],
            prov_telefono   =data['prov_telefono'],
            prov_ruc        =data['prov_ruc'],
            prov_correo     =data['prov_correo'],
            prov_estado     =data['prov_estado']
        )
        db.session.add(nueva_proveedor)
        db.session.commit()

        return jsonify({'message': 'Proveedor registrada exitosamente', 'est': 'success'})
        
    except Exception as e:
        
        return jsonify({'message': str(e), 'est': 'error'})

# Ruta para traer los proveedores
@app.route('/api/v1/obtener_proveedor', methods=['GET'])
def obtener_proveedor():
    proveedores = in_proveedor.query.filter(in_proveedor.prov_estado != 9).order_by(in_proveedor.prov_id.desc()).all()

    resultados = []
    for proveedor in proveedores:
        resultados.append({
            'prov_id': proveedor.prov_id,
            'prov_nombre': proveedor.prov_nombre,
            'prov_telefono': proveedor.prov_telefono,
            'prov_ruc': proveedor.prov_ruc,
            'prov_correo': proveedor.prov_correo,
            'prov_estado': proveedor.prov_estado
        })
    return resultados

# Ruta para editar y/o eliminar los proveedores
@app.route('/api/v1/editar_eliminar_proveedores/<int:prov_id>/<string:accion>', methods=['PUT'])
def editar_proveedores(prov_id, accion):
    try:
        # Fetch the category from the database
        proveedor = in_proveedor.query.get(prov_id)

        if proveedor is None:
            return jsonify({'error': 'Proveedor no encontrado', 'est': 'warning'})

        if accion == 'deleted':
            proveedor.prov_estado = 9
            db.session.commit()
            return jsonify({'mensaje': 'Proveedor eliminado exitosamente', 'est': 'success'})

        if accion == 'edit':
            data = request.get_json()
            proveedor.prov_nombre = data.get('prov_nombre', proveedor.prov_nombre)
            proveedor.prov_telefono = data.get('prov_telefono', proveedor.prov_telefono)
            proveedor.prov_ruc = data.get('prov_ruc', proveedor.prov_ruc)
            proveedor.prov_correo = data.get('prov_correo', proveedor.prov_correo)
            proveedor.prov_estado = data.get('prov_estado', proveedor.prov_estado)

            db.session.commit()
            return jsonify({'mensaje': 'Proveedor editado exitosamente', 'est': 'success'})

    except Exception as e:
        return jsonify({'message': str(e), 'est': 'error'})


#================================== PARAMETROS ===================================
# Ruta para traer los proveedores
@app.route('/api/v1/parametroadmin/<int:para_id>', methods=['GET'])
def obtener_parametro(para_id):
    # Corregir la consulta y utilizar la variable correcta en la condición if
    parametros = parametroadmin.query.filter(parametroadmin.para_prefijo == para_id, parametroadmin.para_estado != 9).all()

    if parametros:
        resultados = []

        for parametro in parametros:
            resultados.append({
                'para_id': parametro.para_id,
                'para_cadena1': parametro.para_cadena1,
                'para_cadena2': parametro.para_cadena2,
                'para_fecha1': str(parametro.para_fecha1),
                'para_fecha2': str(parametro.para_fecha2),
                'para_int1': parametro.para_int1,
                'para_int2': parametro.para_int2,
                'para_correlativo': parametro.para_correlativo,
                'para_prefijo': parametro.para_prefijo,
                'para_estado': parametro.para_estado
            })

        return jsonify(resultados)
    else:
        return jsonify({'mensaje': 'Parametro no encontrado'}), 404

#================================== CLIENTE ===================================
# Ruta para traer los clientes
@app.route('/api/v1/obtener_clientes', methods=['GET'])
def obtener_clientes():
    clientes = in_clientes.query.filter(in_clientes.cl_estado != 9).order_by(in_clientes.cl_id.desc()).all()

    resultados = []
    for cliente in clientes:
        resultados.append({
            'cl_id': cliente.cl_id,
            'cl_nombre': cliente.cl_nombre,
            'cl_doc': cliente.cl_doc,
            'cl_email': cliente.cl_email,
            'cl_telefono': cliente.cl_telefono,
            'cl_fnacimiento': str(cliente.cl_fnacimiento),
            'cl_direccion': cliente.cl_direccion
        })
    return resultados


# Ruta para traer los clientes
@app.route('/api/v1/registrar_clientes', methods=['POST'])
def registrar_clientes():
    try:
        data = request.get_json()
        nueva_clientes  = in_clientes(
            cl_nombre       =data['cl_nombre'],
            cl_doc          =data['cl_doc'],
            cl_email        =data.get('cl_email'),
            cl_telefono     =data.get('cl_telefono'),
            cl_fnacimiento  =data.get('cl_fnacimiento'),
            cl_direccion    =data.get('cl_direccion'),
            cl_estado       =data.get('cl_estado')
        )
        db.session.add(nueva_clientes)
        db.session.commit()

        return jsonify({'message': 'clientes registrada exitosamente', 'est': 'success'})
        
    except Exception as e:
        
        return jsonify({'message': str(e), 'est': 'error'})


# Ruta para editar y/o eliminar los clientes
@app.route('/api/v1/editar_eliminar_clientes/<int:cl_id>/<string:accion>', methods=['PUT'])
def editar_cliente(cl_id, accion):
    try:
        cliente = in_clientes.query.get(cl_id)

        if cliente is None:
            return jsonify({'error': 'Cliente no encontrado', 'est': 'warning'})

        if accion == 'deleted':
            cliente.cl_estado = 9
            db.session.commit()
            return jsonify({'mensaje': 'Cliente eliminado exitosamente', 'est': 'success'})

        if accion == 'edit':
            data = request.get_json()
            cliente.cl_nombre       = data.get('cl_nombre', cliente.cl_nombre)
            cliente.cl_doc          = data.get('cl_doc', cliente.cl_doc)
            cliente.cl_email        = data.get('cl_email', cliente.cl_email)
            cliente.cl_telefono     = data.get('cl_telefono', cliente.cl_telefono)
            cliente.cl_fnacimiento  = data.get('cl_fnacimiento', cliente.cl_fnacimiento)
            cliente.cl_direccion    = data.get('cl_direccion', cliente.cl_direccion)
            cliente.cl_estado       = data.get('cl_estado', cliente.cl_estado)

            db.session.commit()
            return jsonify({'mensaje': 'Cliente editado exitosamente', 'est': 'success'})

    except Exception as e:
        return jsonify({'message': str(e), 'est': 'error'})

#================================== VENTA ===================================
@app.route('/api/v1/registar_venta', methods=['POST'])
def agregar_venta():
    try:
        data = request.get_json()

        nueva_venta = in_venta(
            vent_usuario=data['vent_usuario'],
            vent_cliente=data['vent_cliente'],
            vent_direccion=data['vent_direccion'],
            vent_fecha=data['vent_fecha'],
            vent_total=data['vent_total'],
            vent_igv=data['vent_igv'],
            vent_subtotal=data['vent_subtotal']
        )

        db.session.add(nueva_venta)
        db.session.commit()  # Guarda la venta para obtener el vent_id

        for detalle in data['venta_detalle']:
            nuevo_detalle = in_ventadetalle(
                vent_det_vent_id=nueva_venta.vent_id,
                vent_item=detalle['vent_item'],
                vent_cantidad=detalle['vent_cantidad'],
                vent_unidad=detalle['vent_unidad'],
                vent_producto=detalle['vent_producto'],
                vent_valor=detalle['vent_valor'],
                vent_subtotal=detalle['vent_subtotal']
            )

            db.session.add(nuevo_detalle)

        db.session.commit()

        return jsonify({'message': 'Venta registrada exitosamente', 'est': 'success'})
    
    except Exception as e:
        # Asegúrate de hacer rollback en caso de error para evitar inconsistencias en la base de datos
        db.session.rollback()
        return jsonify({'message': str(e), 'est': 'error'})

@app.route('/api/v1/obtener_venta', methods=['GET'])
def obtener_venta():
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])  # Establece la conexión a la base de datos
    cursor = conn.cursor()
    consulta = """
        select v.vent_id,v.vent_usuario,v.vent_cliente,v.vent_direccion,v.vent_fecha,v.vent_total,v.vent_igv,v.vent_subtotal,
        us.us_nombre as nombre_usuario,us.us_username, cl.cl_nombre as cliente, cl.cl_id as id_cliente 
        from in_venta v 
        inner join in_usuario us on us.us_id = v.vent_usuario
        inner join in_clientes cl on cl.cl_id = v.vent_cliente
		order by v.vent_id DESC
        """
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()  # Cierra la conexión a la base de datos

    resultados_ventas = []
    for resultado in resultados:
        vent_id, vent_usuario, vent_cliente, vent_direccion, vent_fecha, vent_total, vent_igv, vent_subtotal,nombre_usuario,us_username,cliente,id_cliente = resultado
        venta_detalles = in_ventadetalle.query.filter_by(vent_det_vent_id=vent_id).all()
        resultados_venta_detalle = []
        for venta_detalle in venta_detalles:
            resultados_venta_detalle.append({
                'vent_det_id':venta_detalle.vent_det_id,
                'vent_det_vent_id':venta_detalle.vent_det_vent_id,
                'vent_item':venta_detalle.vent_item,
                'vent_cantidad':venta_detalle.vent_cantidad,
                'vent_unidad':venta_detalle.vent_unidad,
                'vent_producto':venta_detalle.vent_producto,
                'vent_valor':venta_detalle.vent_valor,
                'vent_subtotal':venta_detalle.vent_subtotal,
            })
        
        resultados_ventas.append({
            'vent_id': vent_id,
            'vent_usuario': vent_usuario,
            'vent_cliente': vent_cliente,
            'vent_direccion': vent_direccion,
            'vent_fecha': vent_fecha.strftime('%Y-%m-%d'),
            'vent_total': vent_total,
            'vent_igv': vent_igv,
            'nombre_usuario': nombre_usuario,
            'us_username': us_username,
            'cliente': cliente,
            'id_cliente': id_cliente,
            'detalles':resultados_venta_detalle,
            'vent_subtotal_venta':vent_subtotal,
        })

    return jsonify(resultados_ventas)

# Total de ventas del día
@app.route('/api/v1/ventas-dia', methods=['POST'])
def reporte_ventas_dia():
    try:
        fecha_actual = request.json.get('fecha')
        resultado = db.session.query(func.sum(in_venta.vent_total).label('vent_total')).filter(in_venta.vent_fecha == fecha_actual).first()
        if resultado.vent_total:
            total_ventas_dia = float(resultado.vent_total)
            return jsonify({'ventas_dia': total_ventas_dia})
        else:
            return jsonify({'ventas_dia': 0.0})
    except Exception as e:
        return jsonify({'error': str(e)})

# Total de ventas del día
@app.route('/api/v1/compras-dia', methods=['POST'])
def compras_dia():
    try:
        fecha_actual = request.json.get('fecha')
        resultado = db.session.query(func.sum(in_compras.comp_total).label('comp_total')).filter(in_compras.comp_fecha == fecha_actual).first()
        if resultado.comp_total:
            compras_dia = float(resultado.comp_total)
            return jsonify({'compras_dia': compras_dia})
        else:
            return jsonify({'compras_dia': 0.0})
    except Exception as e:
        return jsonify({'error': str(e)})
    
# Productos mas vendidos
@app.route('/api/v1/productos_mas_vendidos', methods=['GET'])
def productos_mas_vendidos():

    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
    cursor = conn.cursor()
    consulta = """
        SELECT SUM(vent_cantidad) as cantidad, vent_producto FROM in_ventadetalle
        GROUP BY vent_producto ORDER BY SUM(vent_cantidad) DESC LIMIT 5
    """
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()

    resultados_formateados = [{'cantidad': row[0], 'vent_producto': row[1]} for row in resultados]

    return jsonify(resultados_formateados)

# Reporte abc
@app.route('/api/v1/reporte_abc/<string:accion>', methods=['GET'])
def consultar_api(accion):
    try:
        conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        cur = conn.cursor()

        # consulta = """
        #     SELECT
        #         (SELECT prod_precio FROM in_producto WHERE prod_nombre = vent_producto) as valor_articulo,
        #         SUM(vent_cantidad) as unidades_consumidas,
        #         vent_producto as producto,
        #         SUM(vent_subtotal) as consumo_anual,
        #         (((SUM(vent_subtotal))/(SELECT SUM(vent_subtotal) FROM in_ventadetalle))*100) as porcentaje_total_anual
        #     FROM in_ventadetalle
        #     GROUP BY vent_producto
        #     ORDER BY SUM(vent_cantidad) DESC
        # """

        if accion == 'resumen':   
            consulta = """
                SELECT
                    (SELECT prod_precio FROM in_producto WHERE prod_nombre = vent_producto limit 1) as valor_articulo,
                    SUM(vent_cantidad) as unidades_consumidas,
                    vent_producto as producto,
                    SUM(vent_subtotal) as consumo_anual,
                    (((SUM(vent_subtotal))/(SELECT SUM(vent_subtotal) FROM in_ventadetalle))*100) as porcentaje_total_anual,
                    SUM((((SUM(vent_subtotal))/(SELECT SUM(vent_subtotal) FROM in_ventadetalle))*100)) OVER (ORDER BY SUM(vent_cantidad) DESC) as porcentaje_acumulado_total_anual
                FROM in_ventadetalle
                GROUP BY vent_producto
                ORDER BY SUM(vent_cantidad) ASC limit 3
            """
        if accion == 'reporte':   
            consulta = """
                SELECT
                    (SELECT prod_precio FROM in_producto WHERE prod_nombre = vent_producto limit 1) as valor_articulo,
                    SUM(vent_cantidad) as unidades_consumidas,
                    vent_producto as producto,
                    SUM(vent_subtotal) as consumo_anual,
                    (((SUM(vent_subtotal))/(SELECT SUM(vent_subtotal) FROM in_ventadetalle))*100) as porcentaje_total_anual,
                    SUM((((SUM(vent_subtotal))/(SELECT SUM(vent_subtotal) FROM in_ventadetalle))*100)) OVER (ORDER BY SUM(vent_cantidad) DESC) as porcentaje_acumulado_total_anual
                FROM in_ventadetalle
                GROUP BY vent_producto
                ORDER BY SUM(vent_cantidad) DESC
            """

        #  OVER para calcular la suma acumulativa

        cur.execute(consulta)

        resultado = cur.fetchall()

        cur.close()

        respuesta = []
        for row in resultado:
            resultado_dict = {
                'valor_articulo': row[0],
                'unidades_consumidas': row[1],
                'producto': row[2],
                'consumo_anual': row[3],
                'porcentaje_total_anual': row[4],
                'porcentaje_acumulado_total_anual': row[5]
            }
            respuesta.append(resultado_dict)

        return jsonify({'resultado': respuesta})

    except Exception as e:
        return jsonify({'error': str(e)})

#================================== COMPRA ===================================
@app.route('/api/v1/registar_compra', methods=['POST'])
def agregar_compra():
    try:
        data = request.get_json()

        nueva_compra = in_compras(
            comp_usuario    =data['comp_usuario'],
            comp_proveedor  =data['comp_proveedor'],
            comp_direccion  =data['comp_direccion'],
            comp_fecha      =data['comp_fecha'],
            comp_total      =data['comp_total'],
            comp_igv        =data['comp_igv'],
            comp_subtotal   =data['comp_subtotal']
        )

        db.session.add(nueva_compra)
        db.session.commit()

        for detalle in data['compra_detalle']:
            nuevo_detalle = in_compradetalle(
                comp_det_comp_id=nueva_compra.comp_id,
                comp_det_item=detalle['comp_det_item'],
                comp_det_cantidad=detalle['comp_det_cantidad'],
                comp_det_unidad=detalle['comp_det_unidad'],
                comp_det_producto=detalle['comp_det_producto'],
                comp_det_valor=detalle['comp_det_valor'],
                comp_det_subtotal=detalle['comp_det_subtotal']
            )

            db.session.add(nuevo_detalle)
            # Cambiar por el ID
            in_producto.query.filter_by(prod_nombre=detalle['comp_det_producto']).update({
                "prod_cantidad": in_producto.prod_cantidad + detalle['comp_det_cantidad']
            })

        db.session.commit()

        return jsonify({'message': 'Compra registrada exitosamente', 'est': 'success'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e), 'est': 'error'})


@app.route('/api/v1/obtener_compra', methods=['GET'])
def obtener_compra():
    conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])  # Establece la conexión a la base de datos
    cursor = conn.cursor()
    consulta = """
        select c.comp_id,c.comp_usuario,c.comp_proveedor,c.comp_direccion,c.comp_fecha,c.comp_total,c.comp_igv,c.comp_subtotal,
        us.us_nombre as nombre_usuario,us.us_username, prv.prov_nombre as proveedor, prv.prov_id as id_proveedor 
        from in_compras c 
        inner join in_usuario us on us.us_id = c.comp_usuario
        inner join in_proveedor prv on prv.prov_id = c.comp_id
		order by c.comp_id DESC
        """
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()  # Cierra la conexión a la base de datos

    resultados_compras = []
    for resultado in resultados:
        comp_id,comp_usuario,comp_proveedor,comp_direccion,comp_fecha,comp_total,comp_igv,comp_subtotal,nombre_usuario,us_username,proveedor,id_proveedor = resultado
        compras_detalles = in_compradetalle.query.filter_by(comp_det_comp_id=comp_id).all()
        resultados_venta_detalle = []
        for compras_detalle in compras_detalles:
            resultados_venta_detalle.append({
                'comp_det_id':compras_detalle.comp_det_id,
                'comp_det_comp_id':compras_detalle.comp_det_comp_id,
                'comp_det_item':compras_detalle.comp_det_item,
                'comp_det_cantidad':compras_detalle.comp_det_cantidad,
                'comp_det_unidad':compras_detalle.comp_det_unidad,
                'comp_det_producto':compras_detalle.comp_det_producto,
                'comp_det_valor':compras_detalle.comp_det_valor,
                'comp_det_subtotal':compras_detalle.comp_det_subtotal,
            })
        
        resultados_compras.append({
            'comp_id': comp_id,
            'comp_usuario': comp_usuario,
            'comp_proveedor': comp_proveedor,
            'comp_direccion': comp_direccion,
            'comp_fecha': comp_fecha.strftime('%Y-%m-%d'),
            'comp_total': comp_total,
            'comp_igv': comp_igv,
            'nombre_usuario': nombre_usuario,
            'us_username': us_username,
            'proveedor': proveedor,
            'id_proveedor': id_proveedor,
            'detalles':resultados_venta_detalle,
            'compra_subtotal_compra':comp_subtotal,
        })

    return jsonify(resultados_compras)




if __name__ == '__main__':
    app.run(debug=True)
    app.run(host=HOST, port=PORT)

