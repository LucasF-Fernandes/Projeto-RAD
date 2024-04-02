import tkinter as tk #usando para criar a interface grafica
import sqlite3 as conn #usando para usar o SQLite
from tkinter import messagebox

def dados_clientes(): #função para pegar os dados do cliente
    cpf = cpf_entry.get()
    nome = nome_cliente_agenda_serviço_entry.get()
    nascimento = nascimento_entry.get()
    contato = contato_entry.get()
    try:
        cursor.execute('''INSERT INTO Cliente (cpf, nome, nascimento, contato) VALUES (?, ?, ?, ?);''', (cpf, nome, nascimento, contato))
        conn.commit()
        display_clientes()
    except conn.DatabaseError as err:
        messagebox.showerror('Erro', f'Erro ao inserir cliente: {err}')

def display_clientes(): #função para mostrar os dados já incluso na tabela clientes
    cursor.execute('''SELECT * FROM Cliente''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def dados_barbeiros(): #função para pegar os dados do barbeiros
    id = id_barbeiro_agenda_serviço_entry.get()
    nome = nome_barbeiro_entry.get()
    aniversario = aniversario_barbeiro_entry.get()
    try:
        cursor.execute('''INSERT INTO Barbeiro (id, nome , aniversario) VALUES (?, ?, ?);''', (id, nome, aniversario))
        conn.commit()
        display_barbeiro()
    except conn.DatabaseError as err:
        messagebox.showerror('Erro', f'Erro ao inserir barbeiro: {err}')

def display_barbeiro(): #função para mostrar os dados já incluso na tabela barbeiros
    cursor.execute (''' SELECT * FROM Barbeiro''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def dados_agenda(): #função para pegar os dados do agendamento
    id = id_barbeiro_agenda_serviço_entry.get()
    nome = nome_cliente_agenda_serviço_entry.get()
    data = data_entry.get()
    hora = horario_entry.get()
    
    try:
        id=int(id)
        cursor.execute('''INSERT INTO Agenda (id, nome, data, hora) VALUES (?, ?, ?, ?);''' ,(id, nome, data, hora))
        conn.commit()
        display_agenda()
    except conn.DatabaseError as err:
        messagebox.showerror('Erro', f'Erro ao agendar horário: {err}')

def display_agenda(): #função para mostrar os dados já inclusos na tabela agenda
    cursor.execute ('''SELECT * FROM Agenda''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def dados_serviço(): #função para pegar os dados do serviço
    id = id_barbeiro_agenda_serviço_entry.get()
    nome = nome_cliente_agenda_serviço_entry.get()
    serviço = serviço_entry.get()
    valor = valor_entry.get()
    try:
        cursor.execute('''INSERT INTO Serviços (id, nome, serviço, valor) VALUES (?, ?, ?, ?);''', (id, nome, serviço, valor))
        conn.commit()
        display_clientes()
    except conn.DatabaseError as err:
        messagebox.showerror('Erro', f'Erro ao inserir cliente: {err}')

def display_serviço(): #função para mostrar os dados já incluso na tabela serviço
    cursor.execute('''SELECT * FROM Serviços''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

###############################################################################################    

root= tk.Tk() #interface grafica
root.title('Plataforma de dados e agendamento')

cpf_label = tk.Label(root, text='CPF do Cliente: (somente números!) ')
cpf_label.grid (row=0, column=0)
cpf_entry = tk.Entry(root)
cpf_entry.grid (row=0, column=1)

nome_cliente_label = tk.Label(root, text='Nome Cliente: ')
nome_cliente_label.grid(row=1, column=0)
nome_cliente_agenda_serviço_entry = tk.Entry(root)
nome_cliente_agenda_serviço_entry.grid(row=1, column=1)

nascimento_label = tk.Label(root, text='Nascimento: (ex.: "AAAA-MM-DD/2024-12-31") ')
nascimento_label.grid(row=2, column=0)
nascimento_entry = tk.Entry(root)
nascimento_entry.grid(row=2, column=1)

contato_label = tk.Label(root, text='Contato: ("ex.: 912345678")')
contato_label.grid(row=3, column=0)
contato_entry = tk.Entry(root)
contato_entry.grid(row=3, column=1)

insert_cliente_button = tk.Button(root, text='Cadastrar Cliente', command=dados_clientes)
insert_cliente_button.grid(row=4, columnspan=2)

id_barbeiro_label = tk.Label(root, text='ID Barbeiro:')
id_barbeiro_label.grid(row=5, column=0)
id_barbeiro_agenda_serviço_entry = tk.Entry(root)
id_barbeiro_agenda_serviço_entry.grid(row=5, column=1)

nome_barbeiro_label = tk.Label(root, text='Nome Barbeiro:')
nome_barbeiro_label.grid(row=6, column=0)
nome_barbeiro_entry = tk.Entry(root)
nome_barbeiro_entry.grid(row=6, column=1)

aniversario_barbeiro_label = tk.Label(root, text='Nascimento: (ex.:"AAAA-MM-DD/2024-12-31") ')
aniversario_barbeiro_label.grid(row=7,column=0)
aniversario_barbeiro_entry = tk.Entry(root)
aniversario_barbeiro_entry.grid(row=7, column=1)

insert_barbeiro_button = tk.Button(root, text='Cadastrar Barbeiro', command=dados_barbeiros)
insert_barbeiro_button.grid(row=8, columnspan=2)

id_barbeiro_label = tk.Label(root, text='ID Barbeiro:')
id_barbeiro_label.grid(row=9, column=0)
id_barbeiro_agenda_serviço_entry = tk.Entry(root)
id_barbeiro_agenda_serviço_entry.grid(row=9, column=1)

nome_cliente_label = tk.Label(root, text='Nome do Cliente:')
nome_cliente_label.grid(row=10, column=0)
nome_cliente_entry = tk.Entry(root)
nome_cliente_entry.grid(row=10, column=1)

data_label = tk.Label(root, text='Data: (ex.:"AAAA-MM-DD/2024-12-31") ')
data_label.grid(row=11, column=0)
data_entry = tk.Entry(root)
data_entry.grid(row=11, column=1)

horario_label = tk.Label(root, text='Horário: (ex.: 08:00 ~ 20:00) ')
horario_label.grid(row=12, column=0)
horario_entry = tk.Entry(root)
horario_entry.grid(row=12, column=1)

insert_horario_button = tk.Button(root, text='Agendar Horário', command=dados_agenda)
insert_horario_button.grid(row=13, columnspan=2)

id_barbbeiro_label = tk.Label(root, text='ID do Barbeiro: ')
id_barbeiro_label.grid (row=14, column=0)
id_barbeiro_entry = tk.Entry(root)
id_barbeiro_agenda_serviço_entry.grid (row=14, column=1)

nome_cliente_label = tk.Label(root, text='Nome Cliente: ')
nome_cliente_label.grid(row=15, column=0)
nome_cliente_agenda_serviço_entry = tk.Entry(root)
nome_cliente_agenda_serviço_entry.grid(row=15, column=1)

serviço_label = tk.Label(root, text='1-Tesoura 2-Maquina 3-Barba 4-Cabelo/Barba')
serviço_label.grid(row=16, column=0)
serviço_entry = tk.Entry(root)
serviço_entry.grid(row=16, column=1)

valor_label = tk.Label(root, text='Valor: R$ ')
valor_label.grid(row=17, column=0)
valor_entry = tk.Entry(root)
valor_entry.grid(row=17, column=1)

insert_serviço_button = tk.Button(root, text='Incluir Serviço', command=dados_serviço)
insert_serviço_button.grid(row=18, columnspan=2)


#conecta ao meu BD e cria um cursor
conn = conn.connect('./Barber.db')
cursor = conn.cursor()
#utiliza o cursor para criar as tabelas caso ainda não tenha criado
cursor.execute('''CREATE TABLE IF NOT EXISTS Cliente (cpf INTEGER NOT NULL, nome TEXT NOT NULL, nascimento DATE NOT NULL, contato INTEGER NOT NULL, PRIMARY KEY(cpf))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Barbeiro (id INTEGER NOT NULL, nome TEXT NOT NULL, aniversario DATE NOT NULL, PRIMARY KEY (id))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Agenda (id INTEGER  NOT NULL, nome TEXT NOT NULL, data DATE NOT NULL, hora TEXT NOT NULL, FOREIGN KEY (id) REFERENCES Barbeiro(id), FOREIGN KEY (nome) REFERENCES Cliente(nome))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS  Serviços (id INTEGER NOT NULL, nome TEXTE NOT NULL, serviço INTEGER NOT NULL, valor REAL NOT NULL, FOREIGN KEY(id) REFERENCES Barbeiro(id), FOREIGN KEY (nome) REFERENCES Cliente(nome))''')
#salva os dados inseridos
conn.commit()

root.mainloop() 