from flask import Flask, jsonify, request
import database as db

app = Flask(__name__)

# Inicialização do banco de dados na chamada do App
db.init_db()

######################################################
#                                                    #
#                Rotas para camada Web               #
#                                                    #
######################################################

######################################################
#                 Planos de Saúde                    #
######################################################
@app.route('/api/planoSaude', methods=['GET'])
def listar_planosSaude():
    planos = db.get_planosSaude()
    return jsonify(planos)