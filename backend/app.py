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
@app.route("/api/planoSaude", methods=["GET"])
def listar_planosSaude():
    planos = db.listar_planosSaude()
    return jsonify(planos)


@app.route("/api/planoSaude", methods=["GET"])
def consultar_planoSaude():
    data = request.json
    resultado = db.validar_planoSaude(data["idPlanoSaude"])
    return resultado


# Rota com dupla finalidade, Inserir caso não exista e Atualizar caso exista
# A tela terá apenas um botão para gravação.
@app.route("/api/planoSaude", methods=["POST"])
def gravar_planoSaude():
    data = request.json
    id = data.get("idPlanoSaude", " ")
    resultado = db.gravar_planoSaude(id, data["descricao"])
    return resultado


@app.route("/api/planoSaude", methods=["DELETE"])
def deletar_planoSaude():
    data = request.json
    resultado = db.deletar_planoSaude(data["idPlanoSaude"])
    return resultado


######################################################
#                 Pessoas                            #
######################################################
@app.route("/api/pessoas", methods=["GET"])
def listar_pessoas():
    pessoas = db.listar_pessoas()
    return jsonify(pessoas)


@app.route("/api/pessoas", methods=["GET"])
def consultar_pessoa():
    data = request.json
    resultado = db.consultar_pessoa(data["idPessoa"])
    return resultado


@app.route("/api/pessoa", methods=["POST"])
def gravar_pessoa():
    data = request.json
    id = data.get("idPessoa", " ")
    numero = data.get("numero", "")
    complemento = data.get("complemento", "")
    tipoSanguineo = data.get("tipoSanguineo", "")
    profissao = data.get("profissao", "")
    regProfissional = data.get("regProfissional", "")
    historico = data.get("historico", "")
    resultado = db.gravar_pessoa(
        id,
        data["nome"],
        data["dataNascimento"],
        data["sexo"],
        data["celular"],
        data["cep"],
        data["pais"],
        data["estado"],
        data["cidade"],
        data["bairro"],
        data["endereco"],
        numero,
        complemento,
        tipoSanguineo,
        data["idPlanoSaude"],
        profissao,
        regProfissional,
        historico,
    )
    return resultado

@app.route("/api/pessoa", methods=['DELETE'])
def deletar_pessoa():
    data = request.json
    resultado = db.deletar_pessoa(data['idPessoa'])
    return resultado
