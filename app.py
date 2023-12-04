from flask import Flask,request,jsonify
import psycopg2
from flask_cors import CORS
from conexion import db, init_db
from datetime import datetime
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
    vent_id = db.Column(db.Integer, primary_key=True)
    vent_usuario = db.Column(db.Integer, nullable=False)
    vent_cliente = db.Column(db.Integer, nullable=False)
    vent_direccion = db.Column(db.String(255), nullable=False)
    vent_fecha = db.Column(db.Date, nullable=False)
    vent_total = db.Column(db.Numeric(10, 2), nullable=False)
    vent_igv = db.Column(db.Numeric(10, 2), nullable=False)
    vent_subtotal = db.Column(db.Numeric(10, 2), nullable=False)

class in_ventadetalle(db.Model):
    vent_det_id = db.Column(db.Integer, primary_key=True)
    vent_det_vent_id = db.Column(db.Integer, db.ForeignKey('in_venta.vent_id'), nullable=False)
    vent_item = db.Column(db.Numeric(10, 2), nullable=False)
    vent_cantidad = db.Column(db.Numeric(10, 2), nullable=False)
    vent_unidad = db.Column(db.String(255), nullable=False)
    vent_producto = db.Column(db.String(255), nullable=False)
    vent_valor = db.Column(db.Numeric(10, 2), nullable=False)
    vent_subtotal = db.Column(db.Numeric(10, 2), nullable=False)

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
            prod_estado     =data['prod_estado']
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

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host=HOST, port=PORT)

