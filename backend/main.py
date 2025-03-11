import BancoDados as db
from datetime import datetime, timedelta, date, time
from os import system, name
from tabulate import tabulate

def clearScreen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def menuPrincipal():
    print("+------------------------------------------------+")
    print("| Agenda de Medicamentos - Menu Principal        |")
    print("+------------------------------------------------+")
    print("| 1 - Listar Pacientes                           |")
    print("| 2 - Inserir Paciente                           |")
    print("| 3 - Deletar Paciente                           |")
    print("| 4 - Listar Agendas do dia                      |")
    print("| 5 - Inserir Agenda                             |")
    print("| 0 - Sair do Sistema                            |")
    print("+------------------------------------------------+")

def deletePaciente():
    clearScreen()
    print("+------------------------------------------------+")
    print("| Agenda de Medicamentos - Excluir Paciente      |")
    print("+------------------------------------------------+")
    idPaciente=int(input("Informe o Codigo do Paciente: "))

    dbCon = db.conectarBanco()
    dbSql = dbCon.cursor()
    sql = "DELETE FROM `paciente` WHERE idPaciente = %s"
    dbSql.execute(sql, (idPaciente,))

    dbCon.commit()

    print(dbSql.rowcount, "Paciente Excluido")
    input("Pressione qualquer tecla para voltar ao Menu Principal ")

def inserirPaciente():
    clearScreen()
    print("+------------------------------------------------+")
    print("| Agenda de Medicamentos - Inserir Paciente      |")
    print("+------------------------------------------------+")
    nome=input("|Informe o Nome do Paciente: ")
    idade=input("| Informe a Idade do Paciente: ")
    cuidador=input("| Informe o Cuidadore do Paciente: ")
    print("+------------------------------------------------+")

    dbCon = db.conectarBanco()
    dbSql = dbCon.cursor()
    sql = "INSERT INTO paciente(nome, idade, cuidador) VALUES(%s, %s, %s)"
    val = (nome, idade, cuidador)
    dbSql.execute(sql, val)

    dbCon.commit()

    print(dbSql.rowcount, "Paciente Registrado")
    input("Pressione qualquer tecla para voltar ao Menu Principal ")

def listarPacientes():
    dbCon = db.conectarBanco()
    dbSql = dbCon.cursor()
    dbSql.execute("SELECT * FROM paciente")
    dataResult = dbSql.fetchall()
    
    clearScreen()

    print("+------------------------------------------------------+")
    print("| Agenda de Medicamentos - Lista Pacientes             |")
    print(tabulate(dataResult, headers=['Id', 'Nome', 'Idade', 'Cuidador'], tablefmt='psql'))
    input("Pressione qualquer tecla para voltar ao Menu Principal ")

def listarAgendasDia():
    dbCon = db.conectarBanco()
    dbSql = dbCon.cursor()
    dbSql.execute("SELECT idagenda, hp.nome, medicamento, qtde, quando FROM cuidadores.agenda ag INNER JOIN cuidadores.paciente hp ON ag.idPaciente = hp.idPaciente WHERE date_format(ag.quando, '%Y-%m-%d') = CURDATE()")
    dataResult = dbSql.fetchall()

    clearScreen()

    print("+------------------------------------------------------+")
    print("| Agenda de Medicamentos - Lista Agendas do Dia        |")
    print(tabulate(dataResult, headers=['Id', 'Paciente', 'Medicamento', 'Dose', 'Horario'], tablefmt='psql'))
    input("Pressione qualquer tecla para voltar ao Menu Principal ")

def inserirAgenda():
    clearScreen()
    print("+------------------------------------------------+")
    print("| Agenda de Medicamentos - Inserir Agenda        |")
    print("+------------------------------------------------+")

    idPaciente=input("Informe o ID do Paciente: ")
    medicamento=input("Informe o Nome do Medicamento: ")
    dosagem=input("Informe a dosagem do Mecidamento: ")
    intervalo=int(input("Informe o Intervalo em horas: "))
    qtdeDias=int(input("Informe por quantos dias: "))
    
    dataPri=input("Informe a data da Primeira Dose (AAAA-MM-DD): ")
    ano,  mes, dia = map(int, dataPri.split('-'))
    dataPri=date(year=ano, month=mes, day=dia)

    horaPri=input("Informe a Hora da Primeira Dose (HH:MM): ")
    hora, min = map(int, horaPri.split(":"))
    horaPri=time(hour=hora, minute=min)

    dosesDia = int(24 / intervalo)
    dosesTotal = dosesDia * qtdeDias
    dataDose = datetime.combine(dataPri, horaPri)

    print(dataDose)
    
    dbCon = db.conectarBanco()
    dbSql = dbCon.cursor()

    for x in range(dosesTotal):
        if x > 0:
            dataDose = dataDose + timedelta(hours=(intervalo))
        sql = ("INSERT INTO agenda(idPaciente, medicamento, qtde, quando) VALUES(%s, %s, %s, %s)")
        val = (idPaciente, medicamento, dosagem, dataDose)
        dbSql.execute(sql, val)
    
    dbCon.commit()

def escolherOpcao():
    opt = input("Selecione uma opção: ")
    return opt

if __name__ == "__main__":
    while True:
        clearScreen()
        menuPrincipal()
        opt = escolherOpcao()
        match opt:
            case "1":
                listarPacientes()
            case "2":
                inserirPaciente()
            case "3":
                deletePaciente()
            case "4":
                listarAgendasDia()
            case "5":
                inserirAgenda()
            case "0":
                clearScreen()
                quit()
            case _:
                print("Opcao Invalida, tente de novo")