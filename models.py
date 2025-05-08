from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import validates
from datetime import datetime

from app import db

class ImagenPECL2(db.Model):
    __tablename__ = 'imagenes_pecl2'
    id = db.Column(db.Integer, primary_key=True)
    nombre_fichero = db.Column(db.String(255), nullable=False)
    pixeles_rojo = db.Column(db.Integer, nullable=False)
    pixeles_verde = db.Column(db.Integer, nullable=False)
    pixeles_azul = db.Column(db.Integer, nullable=False)
    usuario = db.Column(db.String(100), nullable=False)
    fecha_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo_imagen = db.Column(db.String(50))
    