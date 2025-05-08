import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import ImagenPECL2

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
def mostrar_imagenes_pecl2():
    imagenes = ImagenPECL2.query.all()
    return render_template('imagenes_pecl2.html', imagenes=imagenes)

@app.route('/enviar-texto', methods=['POST'])
def recibir_texto():
    data = request.get_json()

    imagen = ImagenPECL2(
        nombre_fichero=data.get("nombre_fichero"),
        pixeles_rojo=data.get("pixeles_rojo"),
        pixeles_verde=data.get("pixeles_verde"),
        pixeles_azul=data.get("pixeles_azul"),
        usuario=data.get("usuario"),
        tipo_imagen=data.get("tipo_imagen", "original")  # por defecto "original"
    )

    db.session.add(imagen)
    db.session.commit()

    return {"estado": "ok", "id": imagen.id}



if __name__ == '__main__':
    app.run()
