from flask import Flask,request,jsonify
import psycopg2
from flask_cors import CORS
from conexion import db, init_db
app = Flask(__name__)

HOST = "127.168.0.4"
PORT = 5400

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



class bd_usuario(db.Model):
    us_id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    us_nombre       = db.Column(db.String(100))
    us_username     = db.Column(db.String(50), unique=True)
    us_email        = db.Column(db.String(100), unique=True)
    us_password     = db.Column(db.String(100))
    us_codigo       = db.Column(db.String(100))
    us_rol          = db.Column(db.String(50))

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
    
    usuario = bd_usuario.query.filter_by(us_username=username).first()

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
    

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host=HOST, port=PORT)

