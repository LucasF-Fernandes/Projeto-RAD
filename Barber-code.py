import sqlite3 as connector

try:

    conexao = connector.connect('./Barber.db')
    cursor = conexao.cursor()

    cursor.execute ('''CREATE TABLE IF NOT EXISTS Cliente (
                    cpf INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    nascimento DATE NOT NULL,
                    contato INTEGER NOT NULL,
                    PRIMARY KEY (cpf)
                    );  ''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS Barbeiro (
                    id INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    nascimento DATE NOT NULL,
                    PRIMARY KEY (cpf)
                    );  ''')
    
    cursor.execute ('''CREATE TABLE IF NOT EXISTS Agenda (
                    id INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    data DATE NOT NULL,
                    hora TEXT NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (nome) REFERENCES Barbeiro(nome)
                    );  ''')
        
    conexao.commit
    print ('Banco de Dados criado com sucesso.')

except connector.DatabaseError as err:        
        print ('Erro de Bando de Dados.', err)

finally:
    if conexao:
        cursor.close()
        conexao.close()
    
