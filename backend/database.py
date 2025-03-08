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
            nome VARCHR(050) NOT NULL
        )
        '''
    )
    # Incluir os primeiros Planos de Saúde caso tabela esteja vazia
    c.execute('SELECT COUNT(*) FROM planosSaude')
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO planosSaude (nome) VALUES (?)', [
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
            historigo VARCHAR(800)
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
    
    
# Inicializa o banco na primeira execução
if __name__ == '__main__':
    init_db()