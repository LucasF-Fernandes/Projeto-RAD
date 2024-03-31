import sqlite3 as conn #integrar o banco de dados

try:
#abre uma conexão com o banco de dados e cria um cursor para conseguir mexer no BD
    conexao = conn.connect('./Barber.db')
    cursor = conexao.cursor()
#ação para criar a tabela Cliente
    cursor.execute ('''CREATE TABLE IF NOT EXISTS Cliente (
                    cpf INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    nascimento DATE NOT NULL,
                    contato INTEGER NOT NULL,
                    PRIMARY KEY (cpf)
                    );  ''')
#ação para criar a tabela Barbeiro    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS Barbeiro (
                    id INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    nascimento DATE NOT NULL,
                    PRIMARY KEY (id)
                    );  ''')
#ação para criar a tabela Agenda
    cursor.execute ('''CREATE TABLE IF NOT EXISTS Agenda (
                    id INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    data DATE NOT NULL,
                    hora TEXT NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (nome) REFERENCES Cliente(nome)
                    );  ''')
#aplica as ações e mostra uma mensagem caso funcione    
    conexao.commit
    print ('Banco de Dados criado com sucesso.')
#cria as tabelas somente se a conexão com o BD não apresentar erro, caso não crie apresenta um mensagem de erro
except conn.DatabaseError as err:        
        print ('Erro de Banco de Dados.', err)
#finaliza a conexão com o BD
finally:
    if conexao:
        cursor.close()
        conexao.close()
