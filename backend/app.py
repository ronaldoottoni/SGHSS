from flask import Flask, jsonify, request
from datetime import datetime, timedelta, date, time
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


@app.route("/api/pessoa", methods=["DELETE"])
def deletar_pessoa():
    data = request.json
    resultado = db.deletar_pessoa(data["idPessoa"])
    return resultado


######################################################
#              Modalidades de Atendimento            #
######################################################
@app.route("/api/modalidade", methods=["GET"])
def listar_modalidades():
    retorno = db.listar_modalidades()
    return jsonify(retorno)


@app.route("/api/modalidade", methods=["GET"])
def consultar_modalidade():
    data = request.json
    resultado = db.consultar_modalidade(data["idModalidade"])
    return resultado


@app.route("/api/modalidade", methods=["POST"])
def gravar_modalidade():
    data = request.json
    id = data.get("idModalidade", " ")
    resultado = db.gravar_modalidade(id, data["descricao"], data["status"])
    return resultado


@app.route("/api/modalidade", methods=["DELETE"])
def deletar_modalidade():
    data = request.json
    resultado = db.deletar_modalidade(data["idModalidade"])
    return resultado


######################################################
#                  Acomodações                       #
######################################################
@app.route("/api/acomodacao", methods=["GET"])
def listar_acomodacoes():
    retorno = db.listar_acomodacoes()
    return jsonify(retorno)


@app.route("/api/acomodacao", methods=["GET"])
def consultar_acomodacao():
    data = request.json
    resultado = db.consultar_acomodacao(data["idAcomodacao"])
    return resultado


@app.route("/api/acomodacao", methods=["POST"])
def gravar_acomodacao():
    data = request.json
    id = data.get("idAcomodacao", " ")
    resultado = db.gravar_acomodacao(
        data["ala"], data["quarto"], data["leito"], data["descricao"], data["status"]
    )
    return resultado


@app.route("/api/acomodacao", methods=["DELETE"])
def deletar_acomodacao():
    data = request.json
    resultado = db.deletar_acomodacao(data["idAcomodacao"])
    return resultado


######################################################
#                  Registros                         #
######################################################
@app.route("/api/registro", methods=["GET"])
def listar_registros():
    retorno = db.listar_registros()
    return jsonify(retorno)


@app.route("/api/registro", methods=["GET"])
def consultar_registro():
    data = request.json
    resultado = db.consultar_registro(data["idRegistro"])
    return jsonify(resultado)


@app.route("/api/registro", methods=["POST"])
def gravar_registro():
    data = request.json
    id = data.get("idRegistro", " ")
    dataSaida = data.get("dataSaida", "0")
    dataRetorno = data.get("dataRetorno", "0")
    idAcomodacao = data.get("idAcomodacao", "0")
    observacoes = data.get("observacoes")
    resultado = db.gravar_registro(
        id,
        data["idPessoa"],
        data["tipoRegistro"],
        data["idProfissional"],
        data["dataEntrada"],
        dataSaida,
        dataRetorno,
        idAcomodacao,
        data["sinaisVitais"],
        data["sintomas"],
        data["diagnostico"],
        data["tratamento"],
        observacoes,
        data["idModalidade"],
    )
    return resultado


@app.route("/api/registro", methods=["DELETE"])
def deletar_registro():
    data = request.json
    resultado = db.deletar_registro(data["idRegistro"])
    return resultado


######################################################
#             Agenda de Medicações                   #
######################################################
@app.route("/api/medicagem", methods=["GET"])
def listar_medicagens():
    resultado = db.listar_medicagens()
    return jsonify(resultado)


@app.route("/api/medicagem", methods=["GET"])
def consutar_medicagem():
    data = request.json
    resultado = db.consultar_medicagem(data["idMedicagem"])
    return jsonify(resultado)


@app.route("/api/medicagem", methods=["PUT"])
def gravar_medicagem():
    data = request.json
    resultado = db.gravar_medicagem(
        data["idMedicagem"],
        data["idRegistro"],
        data["idLotacao"],
        data["horario"],
        data["medicamento"],
        data["dosagem"],
        data["status"],
    )
    return resultado


@app.route("/api/medicagem", methods=["POST"])
def inserir_medicagem():
    data = request.json
    id = data.get("idMedicagem", " ")

    dataPri = data["dataPri"]
    ano, mes, dia = map(int, dataPri.split("-"))
    dataPri = date(year=ano, month=mes, day=dia)

    horaPri = data["horaPri"]
    hora, min = map(int, horaPri.split(":"))
    horaPri = time(hour=hora, minute=min)

    intervalo = int(data["intervalo"])
    dosesDia = int(24 / intervalo)
    qtdeDias = int(data["qtdeDias"])

    dosesTotal = dosesDia * qtdeDias
    dataDose = datetime.combine(dataPri, horaPri)

    resultado = []
    for x in range(dosesTotal):
        if x > 0:
            dataDose = dataDose + timedelta(hours=(intervalo))
        gravacao = db.inserir_medicagem(
            id,
            data["idRegistro"],
            data["idLotacao"],
            dataDose,
            data["medicamento"],
            data["dosagem"],
            data["status"],
        )
        resultado.append(gravacao)
    return resultado


@app.route("/api/medicagem", methods=["DELETE"])
def deletar_medicagem():
    data = request.json
    resultado = db.deletar_medicagem(data["idMedicagem"])
    return resultado
