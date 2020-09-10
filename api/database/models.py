"""#Aqui será criado os modelos que serão utilizados
para trabalhar na estruturação dos dados.

Nessa primeira parte estamos chamando o banco
de dados para que seja possivel ter os recursos
necessários para inicializar a os modelos. """
from .db import db
from mongoengine.fields import EmailField, StringField

class User(db.Document):
    username = db.StringField(min_length=4, max_length=16, required=True, unique=True)
    first_name = db.StringField(min_length=3, max_length=20, required=True)
    last_name = db.StringField(min_length=3, max_length=20, required=True)
    email = db.EmailField(unique=True)