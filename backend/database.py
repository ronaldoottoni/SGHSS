import sqlite3

def db_connect():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db_connect()    
    c = conn.cursor()
    
    # Criar a tabela de Planos de Saúde caso não exista
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS planosSaude (
            idPlanoSaude INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao VARCHR(050) NOT NULL
        )
        '''
    )
    # Incluir os primeiros Planos de Saúde caso tabela esteja vazia
    c.execute('SELECT COUNT(*) FROM planosSaude')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO planosSaude (descricao) VALUES (?)', [
            ("SUS",),
            ("Particular",),
            ("Amil",),
            ("Unimed",)
        ])
    
    # Criar a tabela de Pessoas se não existir
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS pessoas (
            idPessoa INTEGER PRIMARY KEY,  
            nome VARCHAR(60) NOT NULL,
            dataNascimento DATETIME NOT NULL,
            sexo VARCHAR(001) NOT NULL,
            celular INTEGER NOT NULL,
            cep INTEGER NOT NULL,
            pais VARCHAR(050) NOT NULL,
            estado VCARCHAR(002) NOT NULL,
            cidade VARCHAR(050) NOT NULL,
            bairro VARCHAR(025) NOT NULL,
            endereco VARCHAR(050) NOT NULL,
            numero INTEGER,
            complemento VARCHAR(030), 
            tipoSanguineo VARCHAR(005),
            idPlanoSaude INTEGER NOT NULL,
            profissao VARCHAR(030),
            regProfissional VARCHAR(030),
            historico VARCHAR(800)
        )
        '''
    )
    
    # Incluir Pessoa padrão para caso tabela esteja vazia
    c.execute('SELECT COUNT(*) FROM pessoas')
    if c.fetchone()[0] == 0:
        c.executemany('''INSERT INTO pessoas (idPessoa, nome, dataNascimento, sexo, celular, cep, pais, estado, cidade, bairro, endereco, idPlanoSaude) 
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            [
                (70090020030, 'RONALDO OTTONI BORGES', '1983-03-09 15:15:15', 'M', 41991471108, 83420000, 'BRAZIL', 'PR', 'QUATRO BARRAS', 'JD MENINO DEUS', 'RUA PAPA JOAO XXIII', 1)
            ])
        
    # Criar a tabela de usuários se não existir
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS usuarios (
            idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            idPessoa INTEGER NOT NULL,
            login VARCHAR(10) NOT NULL,
            senha VARCHAR(10) NOT NULL,
            ocupacao VARCHAR(25) NOT NULL
        )
        '''
    )
    
    # Adicionar o usuário padrão "root" caso tabela esteja vazia
    c.execute('SELECT COUNT(*) FROM usuarios')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO usuarios (idPessoa, login, senha, ocupacao) VALUES (?, ?, ?, ?)',
            [
                (70090020030, 'root', 'root', 'ADM')
            ])
        
    # Criar a tabela de Modalidades, para tipos de Registros, se a tabela não existir
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS modalidades (
            idModalidade INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao VARCHAR(020) NOT NULL,
            status VARCHAR(001) NOT NULL
        )'''
    )
    
    # Adicionar modalidades principais para os tipode te Registros, caso tabela esteja vazia
    c.execute('SELECT COUNT(*) FROM modalidades')
    if c.fetchone()[0] == 0 :
        c.executemany('INSERT INTO modalidades (descricao, status) VALUES (?, ? )',
            [
                ('Presencial', 'A'),
                ('Virtual', 'A'),
                ('Telefone', 'A'),
            ])
        
    # Criar a tabela de Acomodações, se tabela nao existir
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS acomodacoes(
            idAcomodacao INTEGER PRIMARY KEY AUTOINCREMENT,
            ala INTEIRO NOT NULL,
            quarto INTEIRO NOT NULL,
            leito INTEIRO NOT NULL,
            descricao VARCHAR(030) NOT NULL,
            status VARCHAR(001) NOT NULL
        )
        '''
    )
    
    # Adicionar Acomodações de Modelo, caso esteja vazia
    c.execute('SELECT COUNT(*) FROM acomodacoes')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO acomodacoes (ala, quarto, leito, descricao, status) VALUES (?, ?, ?, ?, ?)',
            [
                (1, 0, 0, 'Enfermaria', 'A'),
                (1, 1, 0, 'Quarto 1', 'A'),
                (1, 1, 1, 'Leito 1', 'A'),
                (2, 0, 0, 'UTI', 'A'),
                (2, 1, 0, 'Quarto 1', 'A'),
                (2, 1, 1, 'Leito 1', 'A'),
                (3, 0, 0, 'Apartamento', 'A'),
                (3, 1, 0, 'Quarto 1', 'A'),
                (3, 1, 1, 'Leito 1', 'A'),
            ])
    
    # Criar a tabela de Registros, se não existir
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS registros(
            idRegistro INTEGER PRIMARY KEY AUTOINCREMENT,
            idPessoa INTEGER NOT NULL,
            tipoRegistro VARCHAR(003) NOT NULL,
            idProfissional INTEGER NOT NULL,
            dataEntrada DATETIME NOT NULL,
            dataSaida DATETIME,
            dataRetorno DATETIME,
            idAcomodacao INTEGER,
            sinaisVitais VARCHAR(300) NOT NULL,
            sintomas VARCHAR(300) NOT NULL,
            diagnostico VARCHAR(300) NOT NULL,
            tratamento VARCHAR(300) NOT NULL,
            observacoes VARCHAR(800),
            idModalidade INTEGER NOT NULL
        )      
        ''')
    
    # Criar a tabela Medicagens, uma agenda para registros de medicamentos, se não existir
    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS medicagens(
            idMedicagem INTEGER PRIMARY KEY AUTOINCREMENT,
            idRegistro INTEGER NOT NULL,
            idLotacao INTEGER NOT NULL,
            horario DATETIME NOT NULL,
            medicamento VARCHAR(020) NOT NULL,
            dosagem VARCHAR(020) NOT NULL,
            status VARCHAR(001) NOT NULL
        )
        ''')
    
    conn.commit()
    conn.close()
    
###########################################################################################
#                                                                                         #
#        ########  #########   #      #    ########                                       #
#        #         #       #   #      #    #       #                                      #
#        #         #      #    #      #    #        #                                     #
#        #         #######     #      #    #        #                                     #
#        #         #      #    #      #    #       #                                      #
#        ########  #       #    ######     ########                                       #
#                                                                                         #
###########################################################################################
    
def get_usuarios():
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_usuario(idPessoa, login, senha, ocupacao):
    conn = db_connect()
    c = conn.cursor()
    c.execute('INSERT INTO usuarios (idPessoa, login, senha, ocupacao) VALUES (?, ?, ?, ?)',
              (idPessoa, login, senha, ocupacao))
    conn.commit()
    conn.close()

def del_usuario(login):
    conn = db_connect()
    c = conn.cursor()
    c.execute('DELETE FROM usuarios WHERE Login = ?', (login,))
    conn.commit()
    conn.close()

def val_usuario(login, senha):
    retorno = ''
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE login = ?', (login,))
    res = c.fetchone()
    conn.close()
    
    if res:
        senha_db = res["senha"]
        if senha_db == senha:
            retorno = "v"
        else:
            retorno = "i"
    else:
        retorno = "n"
    
    
    return retorno

def get_planosSaude():
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM planosSaude')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def add_planoSaude(descricao):
    conn = db_connect()
    c = conn.cursor()
    c.execute('INSERT INTO planosSaude (descricao) VALUES(?)'),(descricao,)
    conn.commit()
    conn.close()

def del_planoSaude(idPlanoSaude):
    conn = db_connect()
    c = conn.cursor()
    c.execute('DELETE FROM planosSaude WHERE idPlanoSaude = ?', (idPlanoSaude))
    conn.commit()
    conn.execute()

def val_planoSaude(idPlanoSaude):
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM planosSaude WHERE idPlanoSaude = ?', (idPlanoSaude))
    res = c.fetchone()
    conn.close()
    
    return res["descricao"] if res else "Plano de Saúde não Encontrado"
    
def get_pessoas():
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM pessoas')
    row = c.fetchall()
    conn.close()
    return [dict(row)for row in rows]

def add_pessoa(nome, dataNascimento, sexo, celular, cep, pais, estado, cidade, bairro, endereco, numero, complemento, tipoSanguineo, idPlanoSaude, profissao, regProfissional, historigodataNascimento):
    conn = db_connect()
    c = conn.cursor()
    c.execute('''
              INSER INTO pessoas (nome, dataNascimento, sexo, celular, cep, pais, estado, cidade, bairro, endereco, numero, complemento, tipoSanguineo, idPlanoSaude, profissao, regProfissional, historigodataNascimento, sexo, celular, cep, pais, estado, cidade, bairro, endereco, numero, complemento, tipoSanguineo, idPlanoSaude, profissao, regProfissional, historico)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              ''',
              (nome, dataNascimento, sexo, celular, cep, pais, estado, cidade, bairro, endereco, numero, complemento, tipoSanguineo, idPlanoSaude, profissao, regProfissional, historigodataNascimento, sexo, celular, cep, pais, estado, cidade, bairro, endereco, numero, complemento, tipoSanguineo, idPlanoSaude, profissao, regProfissional, historico)
            )
    conn.commit()
    conn.close()

def del_pessoa(idPessoa):
    conn = db_connect()
    c = conn.cursor()
    c.execute('DELETE FROM pessoas WHERE idPessoa = ?',(idPessoa,))
    conn.commit()
    conn.close()

def val_pessoa(idPessoa):
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM pessoas WHERE idPessoa = ?', (idPessoa))
    res = c.fetchone()
    conn.close()
    return dict(res) if res else "Pessoa não localizada"

def get_modalidades():
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM modalidades')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
    
def add_modalidade(descricao, status):
    conn = db_connect()
    c = conn.cursor()
    c.execute('INSERTO INTO modalidades (descricao, status) VALUES (?, ?)',
              (descricao, status)
            )
    conn.commit()
    conn.close()

def del_validade(idModalidade):
    conn = db_connect()
    c = conn.cursor()
    c.execute('DELETE FROM modalidades WHERE idModalidade = ?', (idModalidade))
    
def val_modalidade(idModalidade):
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM modalidades WHERE idModalidade = ?', (idModalidade))
    res = c.fetchone()
    return dict(res) if res else "Modalidade não encontrada"

def get_acomodacoes():
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM acomodacoes')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
    
def add_acomodacao():
    conn = db_connect()
    c = conn.cursor()
    c.execute()
    conn.close()
    
def del_acomodacao(idAcomodacao):
    conn = db_connect()
    c = conn.cursor()
    c.execute('DELETE FROM acomodacoes WHERE idAcomodacao = ?', (idAcomodacao))
    conn.close()
    
def val_acomodacao(idAcomodacao):
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM acomodacoes WHERE idAcomodacao = ?', (idAcomodacao))
    res = c.fetchone()
    conn.close()
    return res if res else "Acomodação não cadastrada"

def get_registros():
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM registros')
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]
    
def add_registro(idPesoa, tipoRegistro, idProfissional, dataEntrada, dataSaida, dataRetorno, idAcomodacao, sinaisVitais, sintomas, diagnostico, tratamento, observacoes, idModalidade):
    conn = db_connect()
    c = conn.cursor()
    c.execute('''INSERT INTO registros (idPesoa, tipoRegistro, idProfissional, dataEntrada, dataSaida, dataRetorno, idAcomodacao, sinaisVitais, sintomas, diagnostico, tratamento, observacoes, idModalidade)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (idPesoa, tipoRegistro, idProfissional, dataEntrada, dataSaida, dataRetorno, idAcomodacao, sinaisVitais, sintomas, diagnostico, tratamento, observacoes, idModalidade)
            )
    conn.commit()
    conn.close()
    
def del_registro(idRegistro):
    conn = db_connect()
    c = conn.cursor()
    c.execute('DELETE FROM registros WHERE idRegistro = ?', (idRegistro))
    conn.commit()
    conn.close()
    
def val_registro(idRegistro):
    conn = db_connect()
    c = conn.cursor()
    c.execute('SELECT * FROM registros WHERE idRegistro = ?', (idRegistro))
    res = c.fetchone()
    conn.close()
    return res if res else 'Registro não encontrado'
# Inicializa o banco na primeira execução
if __name__ == '__main__':
    init_db()