from flask_mongoengine import MongoEngine


db = MongoEngine()

#Essa função vai fazer a chamada para o nosso
#app.py para iniciar o banco de dados.
def start_db(app):
    db.init_app(app)