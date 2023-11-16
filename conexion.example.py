from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    
    USUARIO = 'postgres'
    PASS = ''
    PORT = "5432"
    DB = 'bd_inventario'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+USUARIO+':'+PASS+'@localhost:'+PORT+'/'+DB
    db.init_app(app)