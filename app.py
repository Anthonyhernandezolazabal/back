from flask import Flask,request,jsonify
import psycopg2
from flask_cors import CORS
from conexion import db, init_db
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


# Ruta para editar una categoría
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




if __name__ == '__main__':
    app.run(debug=True)
    app.run(host=HOST, port=PORT)

