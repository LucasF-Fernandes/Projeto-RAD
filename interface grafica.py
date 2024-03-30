import tkinter as tk
import sqlite3 as conn

def dados_clientes():
    cpf = cpf_entry.get()
    nome = nome_cliente_entry.get()
    nascimento = nascimento_entry.get()
    contato = contato_entry.get()
    cursor.execute('''INSERT INTO Cliente (cpf, nome, nascimento, contato) VALUES (?, ?, ?, ?);''', (cpf, nome, nascimento, contato))
    conn.commit()
    display_clientes()

def display_clientes():
    cursor.execute('''SELECT * FROM Cliente''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def dados_barbeiros():
    id = id_barbeiro_entry.get()
    nome = nome_barbeiro_horario_entry.get()
    nascimento = nascimento_barbeiro_entry.get()
    cursor.execute('''INSERT INTO Barbeiro (id, nome , nascimento) VALUES (?, ?, ?);''', (id, nome, nascimento))
    conn.commit()
    display_barbeiro()

def display_barbeiro():
    cursor.execute (''' SELECT * FROM Barbeiro''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def dados_agenda():
    id = id_barbeiro_entry.get()
    nome = nome_barbeiro_horario_entry.get()
    data = data_entry.get()
    hora = horario_entry.get()
    cursor.execute('''INSERT INTO Agenda (id, nome, data, hora) VALUES (?, ?, ?, ?);''' ,(id, nome, data, hora))
    conn.commit()
    display_agenda()

def display_agenda():
    cursor.execute ('''SELECT * FROM Agenda''')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

root= tk.Tk()
root.title('Coloque os Dados')

cpf_label = tk.Label(root, text='CPF: (ex.:"12345678900") ')
cpf_label.grid (row=0, column=0)
cpf_entry = tk.Entry(root)
cpf_entry.grid (row=0, column=1)

nome_cliente_label = tk.Label(root, text='Nome Cliente: ')
nome_cliente_label.grid(row=1, column=0)
nome_cliente_entry = tk.Entry(root)
nome_cliente_entry.grid(row=1, column=1)

nascimento_label = tk.Label(root, text='Nascimento: (ex.:"AAAA-MM-DD/2024-12-31") ')
nascimento_label.grid(row=2, column=0)
nascimento_entry = tk.Entry(root)
nascimento_entry.grid(row=2, column=1)

contato_label = tk.Label(root, text='Contato: ("ex.: 912345678")')
contato_label.grid(row=3, column=0)
contato_entry = tk.Entry(root)
contato_entry.grid(row=3, column=1)

insert_cliente_button = tk.Button(root, text='Inserir Cliente', command=dados_clientes)
insert_cliente_button.grid(row=4, columnspan=2)

id_barbeiro_label = tk.Label(root, text='ID Barbeiro:')
id_barbeiro_label.grid(row=5, column=0)
id_barbeiro_entry = tk.Entry(root)
id_barbeiro_entry.grid(row=5, column=1)

nome_barbeiro_label = tk.Label(root, text='Nome Barbeiro:')
nome_barbeiro_label.grid(row=6, column=0)
nome_barbeiro_entry = tk.Entry(root)
nome_barbeiro_entry.grid(row=6, column=1)

nascimento_barbeiro_label = tk.Label(root, text='Nascimento: (ex.:"AAAA-MM-DD/2024-12-31") ')
nascimento_barbeiro_label.grid(row=7,column=0)
nascimento_barbeiro_entry = tk.Entry(root)
nascimento_barbeiro_entry.grid(row=7, column=1)

insert_barbeiro_button = tk.Button(root, text='Inserir Barbeiro', command=dados_barbeiros)
insert_barbeiro_button.grid(row=8, columnspan=2)

id_barbeiro_label = tk.Label(root, text='ID Barbeiro:')
id_barbeiro_label.grid(row=9, column=0)
id_barbeiro_entry = tk.Entry(root)
id_barbeiro_entry.grid(row=9, column=1)

nome_barbeiro_horario_label = tk.Label(root, text='Nome Barbeiro:')
nome_barbeiro_horario_label.grid(row=10, column=0)
nome_barbeiro_horario_entry = tk.Entry(root)
nome_barbeiro_horario_entry.grid(row=10, column=1)

data_label = tk.Label(root, text='Data: (ex.:"AAAA-MM-DD/2024-12-31") ')
data_label.grid(row=11, column=0)
data_entry = tk.Entry(root)
data_entry.grid(row=11, column=1)

horario_label = tk.Label(root, text='Horário: (ex.: 08:00 ~ 20:00) ')
horario_label.grid(row=12, column=0)
horario_entry = tk.Entry(root)
horario_entry.grid(row=12, column=1)

insert_horario_button = tk.Button(root, text='Inserir Horário', command=dados_agenda)
insert_horario_button.grid(row=13, columnspan=2)

conn = conn.connect('./Barber.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Cliente (cpf INTEGER PRIMARY KEY, nome TEXT NOT NULL, nascimento DATE NOT NULL, contato INTEGER NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Barbeiro (id INTEGER PRIMARY KEY, nome TEXT NOT NULL)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS Agenda (id INTEGER NOT NULL, nome TEXT NOT NULL, data DATE NOT NULL, hora TEXT NOT NULL, FOREIGN KEY (id) REFERENCES Barbeiro(id), FOREIGN KEY (nome) REFERENCES Barbeiro(nome))''')

conn.commit()

root.mainloop()