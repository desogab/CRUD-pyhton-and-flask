#Quando não há um método explícito nas chamadas,
#o método GET é tomado por padrão.
from flask import Flask, request, Response, jsonify, render_template
from database.db import start_db
from database.models import User
import json
import  bs4, parser, urllib.request
import re
from bs4 import BeautifulSoup


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/api'
}

start_db(app)


@app.route('/')
def index():
    return render_template('home.html')


#Esta função tem objetivo de procurar as urls de um determinado site
#pela tag 'a' e extrair do 'href' e adiciona-los a um array
#que sera entregue em json

@app.route('/<path:urls>')
def find_urls(urls):
    html = urllib.request.urlopen(urls)
    soup = BeautifulSoup(html.read(), 'html.parser')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return jsonify(links)


#Aqui é feito a conversão do documento
# que por padrão é um objeto com os
#registros de usuários em nosso banco de dados
#e como retorno nos traz ja em JSON as informação
#solicitadas.
#Nos traz todos os usuários na base de dados local
@app.route('/users')
def all_users():
    user = User.objects().to_json()
    return Response(user, mimetype="application/json", status=200)

#Faz a solicitação de um usuário específico.
@app.route('/users/<id>')
def get_user(id):
    user = User.objects(id=id).to_json()
    return Response(user, mimetype="application/json", status=200)


#A particularidade desta funçaoa baixo 
#é o elemento spread(**), reduzindo a sintaxe.
#Ele transforma algo como :
#   User(name="qualquer",
#        first_name="qualquer",
#        last_name="qualquer",
#        email="qualquer")
@app.route('/users', methods=['POST'])
def add_user():
    body = request.get_json()
    user = User(**body).save()
    id = user.id
    return {'id': str(id)}, 200


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()
    User.objects.get(id=id).update(**body)
    return "Atualização Efetuada com Sucesso!", 200


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.objects.get(id=id).delete()
    return "O usuário já não está em nosso banco de dados.", 200




if __name__ == "__main__":
    app.run()