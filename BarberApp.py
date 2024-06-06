
import sqlite3 as conn
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime, timedelta

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry('600x400')
        
        self.label_usuario = tk.Label(self.master, text="Nome de usuário:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(self.master)
        self.entry_usuario.pack()
        
        self.label_senha = tk.Label(self.master, text="Senha:")
        self.label_senha.pack()
        self.entry_senha = tk.Entry(self.master, show="*")
        self.entry_senha.pack()
        
        self.button_login = tk.Button(self.master, text="Login", command=self.login)
        self.button_login.pack()

    def login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if usuario == 'Admin' and senha == 'admin':
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.master.destroy()
            root = tk.Tk()
            app = BarberApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos!")

    def criar_tabs(self):
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS Cliente (cpf INTEGER NOT NULL, nome TEXT NOT NULL, nascimento TEXT NOT NULL, contato INTEGER NOT NULL, PRIMARY KEY(cpf))''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Barbeiro (id INTEGER NOT NULL, nome TEXT NOT NULL, aniversario DATE NOT NULL, PRIMARY KEY (id))''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Agenda (id INTEGER  NOT NULL, nome TEXT NOT NULL, data DATE NOT NULL, hora TEXT NOT NULL, FOREIGN KEY (id) REFERENCES Barbeiro(id), FOREIGN KEY (nome) REFERENCES Cliente(nome))''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS Serviços (id INTEGER NOT NULL, nome TEXT NOT NULL, serviço INTEGER NOT NULL, valor REAL NOT NULL, FOREIGN KEY(id) REFERENCES Barbeiro(id), FOREIGN KEY (nome) REFERENCES Cliente(nome))''')

            conexao.commit()
        
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'erro ao criar tabelas: {err}')

        finally:
            cursor.close()
            conexao.close()

class ClientesMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Clientes')
        self.master.geometry('600x400')

        self.button_add = tk.Button(self.master, text='Cadastrar Cliente', command=self.janela_de_cadastro)
        self.button_add.pack(pady=20)

        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack(pady=10)

        self.search_entry_label = tk.Label(self.search_frame, text='Digite o CPF ou Nome:')
        self.search_entry_label.grid(row=1, column=0)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=1, column=1)

        self.result_text = tk.Text(self.master, height=10, width=60)
        self.result_text.pack(pady=10)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, "Para buscar todos, deixe a caixa acima vazia.\n\n")
        self.result_text.config(state=tk.DISABLED)

        self.search_button = tk.Button(self.search_frame, text='Buscar', command=self.buscar_cliente)
        self.search_button.grid(row=1, column=2)

        self.button_edit = tk.Button(self.master, text='Editar Cadastro', command=self.abrir_janela_edicao)
        self.button_edit.pack(pady=10)

        self.button_back = tk.Button(self.master, text='Voltar', command=self.voltar)
        self.button_back.pack(pady=10)

    def janela_de_cadastro(self):
        self.cadastro_window = tk.Toplevel(self.master)
        self.cadastro_window.title('Cadastro de Cliente')

        self.cpf_label = tk.Label(self.cadastro_window, text='CPF do Cliente: (somente números!) ')
        self.cpf_label.grid(row=0, column=0)
        self.cpf_entry = tk.Entry(self.cadastro_window)
        self.cpf_entry.grid(row=0, column=1)

        self.nome_label = tk.Label(self.cadastro_window, text='Nome do Cliente: ')
        self.nome_label.grid(row=1, column=0)
        self.nome_entry = tk.Entry(self.cadastro_window)
        self.nome_entry.grid(row=1, column=1)

        self.nascimento_label = tk.Label(self.cadastro_window, text='Data de Nascimento: ')
        self.nascimento_label.grid(row=2, column=0)
        self.nascimento_entry = DateEntry(self.cadastro_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.nascimento_entry.grid(row=2, column=1)

        self.contato_label = tk.Label(self.cadastro_window, text='Contato: (ex.: 912345678)')
        self.contato_label.grid(row=3, column=0)
        self.contato_entry = tk.Entry(self.cadastro_window)
        self.contato_entry.grid(row=3, column=1)

        self.button_cadastrar = tk.Button(self.cadastro_window, text='Cadastrar', command=self.cadastrar_cliente)
        self.button_cadastrar.grid(row=4, columnspan=2, pady=10)

    def cadastrar_cliente(self):
        cpf = self.cpf_entry.get()
        nome = self.nome_entry.get()
        nascimento = self.nascimento_entry.get()
        contato = self.contato_entry.get()

        if not cpf or not nome or not nascimento or not contato:
            messagebox.showerror('Erro', 'Preencha todos os campos.')
            return

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''INSERT INTO Cliente (cpf, nome, nascimento, contato) VALUES (?, ?, ?, ?);''', (cpf, nome, nascimento, contato))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Cliente cadastrado com sucesso!')
            self.zerar()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao inserir cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def zerar(self):
        self.cpf_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.nascimento_entry.delete(0, tk.END)  
        self.contato_entry.delete(0, tk.END)
        
    def janela_de_listar(self):
        self.master.title('Lista de Clientes')
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            cursor.execute('''SELECT * FROM Cliente''')
            clientes = cursor.fetchall()

            for cliente in clientes:
                cpf = cliente[0]
                nome = cliente[1]
                # Adiciona os dados do cliente ao widget de texto
                self.result_text.insert(tk.END, f"CPF: {cpf}\tNome: {nome}\n")
            
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()
            
        self.result_text.config(state=tk.DISABLED)
    
    def buscar_cliente(self):
        termo = self.search_entry.get()
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            if not termo:
                cursor.execute('''SELECT * FROM Cliente''')  # Consulta SQL para selecionar todos os clientes
            else:
                cursor.execute('''SELECT * FROM Cliente WHERE nome LIKE ? OR cpf = ?''', ('%' + termo + '%', termo))
            
            clientes = cursor.fetchall()

            if self.result_text:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
            
            for cliente in clientes:
                cpf = cliente[0]
                nome = cliente[1]
                nascimento = cliente[2]
                contato = cliente[3]
                texto_formatado = f"CPF: {cpf}\nNome: {nome}\nNascimento: {nascimento}\nContato: {contato}\n\n"
                self.result_text.insert(tk.END, texto_formatado)
            
            self.result_text.config(state=tk.DISABLED)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()
    
    def abrir_janela_edicao(self):
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title('Edição de Cadastros')

        # Result Text
        self.result_text_edit = tk.Text(self.edit_window, height=10, width=50)
        self.result_text_edit.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.result_text_edit.config(state=tk.NORMAL)
        self.result_text_edit.insert(tk.END, 'Cliente a ser alterado')
        self.result_text_edit.config(state=tk.DISABLED)

        # Labels e Entradas
        self.cpf_label = tk.Label(self.edit_window, text='CPF do Cliente:')
        self.cpf_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.cpf_entry = tk.Entry(self.edit_window)
        self.cpf_entry.grid(row=1, column=1, padx=10, pady=5)

        self.nome_label = tk.Label(self.edit_window, text='Nome do Cliente:')
        self.nome_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.nome_entry = tk.Entry(self.edit_window)
        self.nome_entry.grid(row=2, column=1, padx=10, pady=5)

        self.nascimento_label = tk.Label(self.edit_window, text='Data de Nascimento:')
        self.nascimento_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.nascimento_entry = tk.Entry(self.edit_window)
        self.nascimento_entry.grid(row=3, column=1, padx=10, pady=5)

        self.contato_label = tk.Label(self.edit_window, text='Contato:')
        self.contato_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.contato_entry = tk.Entry(self.edit_window)
        self.contato_entry.grid(row=4, column=1, padx=10, pady=5)

        # Botões
        self.search_button = tk.Button(self.edit_window, text='Buscar', command=self.buscar_cpf)
        self.search_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        self.button_atualizar = tk.Button(self.edit_window, text='Atualizar', command=self.atualizar_cliente)
        self.button_atualizar.grid(row=5, column=1, padx=10, pady=10)

        self.button_excluir = tk.Button(self.edit_window, text='Excluir', command=self.excluir_cliente)
        self.button_excluir.grid(row=5, column=2, padx=10, pady=10)

    def buscar_cpf(self):
        # Obtém o CPF digitado
        cpf = self.cpf_entry.get()
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            # Consulta o banco de dados para obter os detalhes do cliente com o CPF fornecido
            cursor.execute('''SELECT * FROM Cliente WHERE cpf = ? LIMIT 1''', (cpf,))
            cliente = cursor.fetchone()
            
            if cliente:
                # Se o cliente existir, preenche os campos de entrada com os detalhes do cliente
                self.nome_entry.delete(0, tk.END)
                self.nome_entry.insert(tk.END, cliente[1])

                self.nascimento_entry.delete(0, tk.END)
                self.nascimento_entry.insert(tk.END, cliente[2])

                self.contato_entry.delete(0, tk.END)
                self.contato_entry.insert(tk.END, cliente[3])

                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, f"CPF: {cliente[0]}\nNome: {cliente[1]}\nNascimento: {cliente[2]}\nContato: {cliente[3]}\n")
                self.result_text.config(state=tk.DISABLED)
                
            else:
                messagebox.showinfo('Cliente não encontrado', 'Cliente com o CPF fornecido não encontrado.')
        
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def editar_cadastro(self):
        termo = self.search_entry.get()
                

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            if not termo:
                cursor.execute('''SELECT * FROM Cliente''')  # Consulta SQL para selecionar todos os clientes
            else:
                cursor.execute('''SELECT * FROM Cliente WHERE nome LIKE ? OR cpf = ?''', ('%' + termo + '%', termo))
            
            clientes = cursor.fetchall()

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            for cliente in clientes:
                cpf = cliente[0]
                nome = cliente[1]
                nascimento = cliente[2]
                contato = cliente[3]
                texto_formatado = f"CPF: {cpf}\nNome: {nome}\nNascimento: {nascimento}\nContato: {contato}\n\n"
                self.result_text_edit.insert(tk.END, texto_formatado)
            self.result_text_edit.config(state=tk.DISABLED)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def atualizar_cliente(self):
        cpf = self.cpf_entry.get()
        nome = self.nome_entry.get()  # Substitua 'nome_entry' pelo nome do Entry onde você digita o nome do cliente
        nascimento = self.nascimento_entry.get()  # Substitua 'nascimento_entry' pelo nome do Entry onde você digita a data de nascimento do cliente
        contato = self.contato_entry.get()

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''UPDATE Cliente SET nome=?, nascimento=?, contato=? WHERE cpf=?''', (nome, nascimento, contato, cpf))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Cliente atualizado com sucesso!')

            self.buscar_cliente()
            self.zerar()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao atualizar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def excluir_cliente(self):
        cpf = self.cpf_entry.get()
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cliente?")
        if confirmar:
            try:
                conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
                cursor = conexao.cursor()
                cursor.execute('''DELETE FROM Cliente WHERE cpf=?''', (cpf,))
                conexao.commit()
                messagebox.showinfo('Sucesso', 'Cliente excluído com sucesso!')
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
                self.result_text.config(state=tk.DISABLED)
            except conn.DatabaseError as err:
                messagebox.showerror('Erro', f'Erro ao excluir cliente: {err}')
            finally:
                cursor.close()
                conexao.close()
                
    def deletar_cliente(self, cpf):
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''DELETE FROM Cliente WHERE cpf=?''', (cpf,))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Cliente excluído com sucesso!')
            self.buscar_cliente()  # Atualiza a lista de clientes após exclusão

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao excluir cliente: {err}')

        finally:
            cursor.close()
            conexao.close()
        
    def voltar(self):
        self.master.destroy()
        root = tk.Tk()
        app = BarberApp(root)
        root.mainloop()

class BarberApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Barbearia App")
        self.master.geometry("600x400")

        self.label = tk.Label(self.master, text="Bem-vindo à Barbearia App", font=("Arial", 18))
        self.label.pack(pady=20)

        self.label_options = tk.Label(self.master, text="Selecione uma opção:")
        self.label_options.pack(pady=10)

        self.button_clients = tk.Button(self.master, text="Clientes", command=self.open_janela_cliente)
        self.button_clients.pack(pady=5)

        self.button_barbers = tk.Button(self.master, text="Barbeiros", command=self.open_janela_barber)
        self.button_barbers.pack(pady=5)

        self.button_agenda = tk.Button(self.master, text="Agenda", command=self.open_janela_agenda)
        self.button_agenda.pack(pady=5)

        self.button_servicos = tk.Button(self.master, text="Serviços", command=self.open_janela_servico)
        self.button_servicos.pack(pady=5)

        self.button_exit = tk.Button(self.master, text="Sair", command=self.master.destroy)
        self.button_exit.pack(pady=10)

    def open_janela_cliente(self):
        self.master.withdraw()
        janela_cliente = tk.Tk()
        janela_cliente.title('Clientes')
        clientes_menu = ClientesMenu(janela_cliente)
        janela_cliente.mainloop()

    def open_janela_barber(self):
        self.master.withdraw()
        janela_barber = tk.Tk()
        janela_barber.title('Barbeiros')
        barbers_menu = BarberMenu(janela_barber)
        janela_barber.mainloop()
        
    def open_janela_agenda(self):
        self.master.withdraw()
        janela_agenda = tk.Tk()
        janela_agenda.title('Agenda')
        agenda_menu = AgendaMenu(janela_agenda)
        janela_agenda.mainloop()

    def open_janela_servico(self):
        self.master.withdraw()
        janela_serviço = tk.Tk()      
        janela_serviço.title('Serviços')
        services_menu = ServicesMenu(janela_serviço)
        janela_serviço.mainloop()

class BarberMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Barbeiros')
        self.master.geometry('600x400')

        self.button_add = tk.Button(self.master, text='Cadastrar Barbeiro', command=self.cadastro_barbeiro)
        self.button_add.pack(pady=20)

        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack(pady=20)

        self.search_entry_label = tk.Label(self.search_frame, text='Digite o ID ou Nome:')
        self.search_entry_label.grid(row=1, column=0)

        self.search_entry_entry = tk.Entry(self.search_frame)
        self.search_entry_entry.grid(row=1, column=1)

        self.result_text = tk.Text(self.master, height=10, width=60)
        self.result_text.pack(pady=10)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, 'Para buscar todos, deixe a caixa acima vazia.\n\n')
        self.result_text.config(state=tk.DISABLED)

        self.search_button = tk.Button(self.search_frame, text='Buscar', command=self.buscar_barbeiro)
        self.search_button.grid (row=1, column=2)

        self.button_edit = tk.Button(self.master, text='Editar Cadastro', command=self.janela_edicao_barbeiro)
        self.button_edit.pack(pady=10)

        self.button_back = tk.Button(self.master, text='Voltar', command=self.voltar)
        self.button_back.pack(pady=10)

    def cadastro_barbeiro(self):
        self.cadastrob_window = tk.Toplevel(self.master)
        self.cadastrob_window.title('Cadastro de Barbeiro')

        self.id_label = tk.Label(self.cadastrob_window, text='ID do Barbeiro:')
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(self.cadastrob_window)
        self.id_entry.grid(row=0, column=1)

        self.nomeb_label = tk.Label(self.cadastrob_window, text='Nome do Barbeiro: ')
        self.nomeb_label.grid(row=1, column=0)
        self.nomeb_entry = tk.Entry(self.cadastrob_window)
        self.nomeb_entry.grid(row=1, column=1)       

        self.aniversario_label = tk.Label(self.cadastrob_window, text='Data de Nascimento: ')
        self.aniversario_label.grid(row=2, column=0)
        self.aniversario_entry = DateEntry(self.cadastrob_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.aniversario_entry.grid(row=2, column=1)

        self.button_cadastrar = tk.Button(self.cadastrob_window, text='Cadastrar', command=self.cadastrar_barbeiro)
        self.button_cadastrar.grid(row=4, columnspan=2, pady=10)

    def cadastrar_barbeiro(self):
        id = self.id_entry.get()
        nomeb = self.nomeb_entry.get()
        aniversario = self.aniversario_entry.get()

        if not id or not nomeb or not aniversario:
            messagebox.showerror('Erro', 'Preencha todos os campos.')
            return
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''INSERT INTO Barbeiro (id, nome, aniversario) VALUES (?, ?, ?);''', (id, nomeb, aniversario))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Cliente cadastrado com sucesso!')
            self.zerar()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao inserir cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def zerar(self):
        self.id_entry.delete(0, tk.END)
        self.nomeb_entry.delete(0, tk.END)
        self.aniversario_entry.delete(0, tk.END)  

    def listar_barbeiro(self):
        self.master.title('Lista de Barbeiros')
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            cursor.execute('''SELECT * FROM Barbeiro''')
            barbeiros = cursor.fetchall()

            for barbeiro in barbeiros:
                id = barbeiro[0]
                nomeb = barbeiro[1]
                # Adiciona os dados do cliente ao widget de texto
                self.result_text.insert(tk.END, f"ID: {id}\tNome: {nomeb}\n")
            
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()
            
        self.result_text.config(state=tk.DISABLED)

    def buscar_barbeiro(self):
        termo = self.search_entry_entry.get()

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            if not termo:
                cursor.execute('''SELECT * FROM Barbeiro''')  # Consulta SQL para selecionar todos os clientes
            else:
                cursor.execute('''SELECT * FROM Barbeiro WHERE nome LIKE ? OR id = ?''', ('%' + termo + '%', termo))
            
            barbeiros = cursor.fetchall()

            if self.result_text:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)

            for barbeiro in barbeiros:
                id = barbeiro[0]
                nomeb = barbeiro[1]
                aniversario = barbeiro[2]
                texto_formatado = f"ID: {id}\nNome: {nomeb}\nNascimento: {aniversario}\n\n"
                self.result_text.insert(tk.END, texto_formatado)
            
            self.result_text.config(state=tk.DISABLED)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar barbeiro: {err}')

        finally:
            cursor.close()
            conexao.close()

    def janela_edicao_barbeiro(self):
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title('Edição de Cadastros')

        self.result_text_edit = tk.Text(self.edit_window, height=10, width=50)
        self.result_text_edit.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.result_text_edit.config(state=tk.NORMAL)
        self.result_text_edit.insert(tk.END, 'Barbeiro a ser alterado')
        self.result_text_edit.config(state=tk.DISABLED)

        self.id_label = tk.Label(self.edit_window, text='ID do Barbeiro:')
        self.id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.id_entry = tk.Entry(self.edit_window)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.nomeb_label = tk.Label(self.edit_window, text='Nome do Barbeiro:')
        self.nomeb_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.nomeb_entry = tk.Entry(self.edit_window)
        self.nomeb_entry.grid(row=2, column=1, padx=10, pady=5)

        self.aniversario_label = tk.Label(self.edit_window, text='Data de Nascimento:')
        self.aniversario_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.aniversario_entry = tk.Entry(self.edit_window)
        self.aniversario_entry.grid(row=3, column=1, padx=10, pady=5)

        self.search_button = tk.Button(self.edit_window, text='Buscar', command=self.buscar_id)
        self.search_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        self.button_atualizar = tk.Button(self.edit_window, text='Atualizar', command=self.atualizar_barbeiro)
        self.button_atualizar.grid(row=5, column=1, padx=10, pady=10)

        self.button_excluir = tk.Button(self.edit_window, text='Excluir', command=self.excluir_barbeiro)
        self.button_excluir.grid(row=5, column=2, padx=10, pady=10)

    def buscar_id(self):
        id = self.id_entry.get()

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            # Consulta o banco de dados para obter os detalhes do cliente com o CPF fornecido
            cursor.execute('''SELECT * FROM Barbeiro WHERE id = ? LIMIT 1''', (id,))
            barbeiro = cursor.fetchone()
            
            if barbeiro:
                # Se o cliente existir, preenche os campos de entrada com os detalhes do cliente
                self.nomeb_entry.delete(0, tk.END)
                self.nomeb_entry.insert(tk.END, barbeiro[1])

                self.aniversario_entry.delete(0, tk.END)
                self.aniversario_entry.insert(tk.END, barbeiro[2])

                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, f"CPF: {barbeiro[0]}\nNome: {barbeiro[1]}\nNascimento: {barbeiro[2]}\n")
                self.result_text.config(state=tk.DISABLED)
                
            else:
                messagebox.showinfo('Barbeiro não encontrado', 'ID fornecido não encontrado.')
        
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar barbeiro: {err}')

        finally:
            cursor.close()
            conexao.close()

    def editar_barbeiro(self):
        termo = self.search_entry.get()
                

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            if not termo:
                cursor.execute('''SELECT * FROM Barbeiro''')  # Consulta SQL para selecionar todos os clientes
            else:
                cursor.execute('''SELECT * FROM Barbeiro WHERE nome LIKE ? OR id = ?''', ('%' + termo + '%', termo))
            
            barbeiros = cursor.fetchall()

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)
            for barbeiro in barbeiros:
                id = barbeiro[0]
                nomeb = barbeiro[1]
                aniversario = barbeiro[2]
                texto_formatado = f"CPF: {id}\nNome: {nomeb}\nNascimento: {aniversario}\n\n"
                self.result_text_edit.insert(tk.END, texto_formatado)
            self.result_text_edit.config(state=tk.DISABLED)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar Barbeiro: {err}')

        finally:
            cursor.close()
            conexao.close()

    def atualizar_barbeiro(self):
        id = self.id_entry.get()
        nomeb = self.nomeb_entry.get()  # Substitua 'nome_entry' pelo nome do Entry onde você digita o nome do cliente
        aniversario = self.aniversario_entry.get()  # Substitua 'nascimento_entry' pelo nome do Entry onde você digita a data de nascimento do cliente

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''UPDATE Barbeiro SET nome=?, aniversario=? WHERE id=?''', (nomeb, aniversario, id))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Barbeiro atualizado com sucesso!')

            self.buscar_barbeiro()
            self.zerar()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao atualizar Barbeiro: {err}')

        finally:
            cursor.close()
            conexao.close()

    def excluir_barbeiro(self):
        id = self.id_entry.get()
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este barbeiro?")
        if confirmar:
            try:
                conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
                cursor = conexao.cursor()
                cursor.execute('''DELETE FROM Barbeiro WHERE id=?''', (id,))
                conexao.commit()
                messagebox.showinfo('Sucesso', 'Barbeiro excluído com sucesso!')
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
                self.result_text.config(state=tk.DISABLED)
            except conn.DatabaseError as err:
                messagebox.showerror('Erro', f'Erro ao excluir cliente: {err}')
            finally:
                cursor.close()
                conexao.close()

    def deletar_barbeiro(self, id):
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''DELETE FROM Barbeiro WHERE id=?''', (id,))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Barbeiro excluído com sucesso!')
            self.buscar_barbeiro()  # Atualiza a lista de clientes após exclusão

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao excluir barbeiro: {err}')

        finally:
            cursor.close()
            conexao.close()

    def voltar(self):
        self.master.destroy()
        root = tk.Tk()
        app = BarberApp(root)
        root.mainloop()

class AgendaMenu:

    def __init__(self, master):
        self.master = master
        self.master.title('Agenda')
        self.master.geometry('600x400')

        self.button_add = tk.Button(self.master, text='Agendar Serviço', command=self.agenda_servico)
        self.button_add.pack(pady=20)

        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack(pady=20)

        self.search_entry_label = tk.Label(self.search_frame, text='Digite o ID ou Nome:')
        self.search_entry_label.grid(row=1, column=0)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=1, column=1)

        self.result_text = tk.Text(self.master, height=10, width=60)
        self.result_text.pack(pady=10)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, 'Para buscar todos, deixe a caixa acima vazia.\n\n')
        self.result_text.config(state=tk.DISABLED)

        self.search_button = tk.Button(self.search_frame, text='Buscar', command=self.buscar_agenda)
        self.search_button.grid (row=1, column=2)

        self.button_edit = tk.Button(self.master, text='Editar Agenda', command=self.janela_edicao_agenda)
        self.button_edit.pack(pady=10)

        self.button_back = tk.Button(self.master, text='Voltar', command=self.voltar)
        self.button_back.pack(pady=10)

    def agenda_servico(self):
        self.agenda_window = tk.Toplevel(self.master)
        self.agenda_window.title('Agendamento')

        self.id_label = tk.Label(self.agenda_window, text='ID do Barbeiro:')
        self.id_label.grid(row=0, column=0)
        self.id_entry = tk.Entry(self.agenda_window)
        self.id_entry.grid(row=0, column=1)

        self.nome_label = tk.Label(self.agenda_window, text='Nome do Cliente:')
        self.nome_label.grid(row=1, column=0)
        self.nome_entry = tk.Entry(self.agenda_window)
        self.nome_entry.grid(row=1, column=1)       

        self.data_label = tk.Label(self.agenda_window, text='Data:')
        self.data_label.grid(row=2, column=0)
        self.data_entry = DateEntry(self.agenda_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.data_entry.grid(row=2, column=1)

        self.hora_label = tk.Label(self.agenda_window, text='Hora:')
        self.hora_label.grid(row=3, column=0)
        self.hora_combobox = ttk.Combobox(self.agenda_window)
        self.hora_combobox.grid(row=3, column=1)

        todos_horarios = self.obter_todos_horarios()
        self.hora_combobox['values'] = todos_horarios
        
        self.button_agendar = tk.Button(self.agenda_window, text='Agendar', command=self.agendar_servico)
        self.button_agendar.grid(row=4, columnspan=2, pady=10)
    
    def obter_todos_horarios(self):
        # Lista de todos os horários possíveis das 8h às 20h com intervalos de uma hora
        horarios_possiveis = [f"{str(h).zfill(2)}:00" for h in range(8, 21)]
        return horarios_possiveis
    
    def obter_horarios_disponiveis(self):
        id_barbeiro = self.id_entry.get()
        data = self.data_entry.get()

        print("ID do barbeiro:", id_barbeiro)
        print("Data:", data)
        
        if not id_barbeiro or not data:
            messagebox.showerror('Erro', 'Preencha o ID do barbeiro e a data.')
            return []

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            cursor.execute('''SELECT hora FROM Agenda WHERE id = ? AND data = ?''', (id_barbeiro, data))
            horarios_agendados = [resultado[0] for resultado in cursor.fetchall()]

            print("Horários agendados:", horarios_agendados)

            horarios_disponiveis = []
            hora_atual = datetime.strptime('08:00', '%H:%M')
            hora_final = datetime.strptime('20:00', '%H:%M')

            while hora_atual <= hora_final:
                hora_formatada = datetime.strftime(hora_atual, '%H:%M')
                if hora_formatada not in horarios_agendados:
                    horarios_disponiveis.append(hora_formatada)
                hora_atual += timedelta(hours=1)

            print("Horários disponíveis:", horarios_disponiveis)

            return horarios_disponiveis

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao obter horários disponíveis: {err}')

        finally:
            cursor.close()
            conexao.close()
    
    def agendar_servico(self):
        id_barbeiro = self.id_entry.get()
        nome_cliente = self.nome_entry.get()
        data = self.data_entry.get()
        hora = self.hora_combobox.get()

        if not id_barbeiro or not nome_cliente or not data or not hora:
            messagebox.showerror('Erro', 'Preencha todos os campos.')
            return

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''SELECT * FROM Barbeiro WHERE id=?''', (id_barbeiro,))
            barbeiro = cursor.fetchone()
            cursor.execute('''SELECT * FROM Cliente WHERE nome=?''', (nome_cliente,))
            cliente = cursor.fetchone()

            if not barbeiro:
                messagebox.showerror('Erro', 'Barbeiro não cadastrado.')
                return
            if not cliente:
                messagebox.showerror('Erro', 'Cliente não cadastrado.')
                return
            
            cursor.execute('''SELECT * FROM Agenda WHERE id = ? AND data = ? AND hora = ?''', (id_barbeiro, data, hora))
            servico_existente = cursor.fetchone()

            if servico_existente:
                messagebox.showerror('Erro', f'Já existe um serviço agendado para o barbeiro {id_barbeiro} nesta hora e data')

            cursor.execute('''INSERT INTO Agenda (id, nome, data, hora) VALUES (?, ?, ?, ?);''', (id_barbeiro, nome_cliente, data, hora))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Agendamento cadastrado com sucesso!')
            self.zerar()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao inserir agendamento: {err}')

        finally:
            cursor.close()
            conexao.close()

    def zerar(self):
        self.id_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.data_entry.delete(0, tk.END)  
        self.hora_combobox.delete(0, tk.END)

    def janela_de_listar(self):
        self.master.title('Agendamentos')
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            cursor.execute('''SELECT * FROM Agenda''')
            agendado = cursor.fetchall()

            for agenda in agendado:
                id = agenda[0]
                nome = agenda[1]
                # Adiciona os dados do cliente ao widget de texto
                self.result_text.insert(tk.END, f"ID: {id}\tNome: {nome}\n")
            
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()
            
        self.result_text.config(state=tk.DISABLED)

    def buscar_agenda(self):
        termo = self.search_entry.get()
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            if not termo:
                cursor.execute('''SELECT * FROM Agenda''')  # Consulta SQL para selecionar todos os clientes
            else:
                cursor.execute('''SELECT * FROM Agenda WHERE nome LIKE ? OR id = ?''', ('%' + termo + '%', termo))
            
            agendado = cursor.fetchall()

            if not agendado:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, 'Barbeiro inexistente')
                self.result_text.config(state=tk.DISABLED)
                return

            if self.result_text:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
            
            for agenda in agendado:
                id_barbeiro = agenda[0]
                nome_cliente = agenda[1]
                data = agenda[2]
                hora = agenda[3]
                texto_formatado = f"ID: {id_barbeiro}\nNome: {nome_cliente}\nData: {data}\nHora: {hora}\n\n"
                self.result_text.insert(tk.END, texto_formatado)
            
            self.result_text.config(state=tk.DISABLED)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar Agendamento: {err}')

        finally:
            cursor.close()
            conexao.close()

    def buscar_agenda_edit(self):
        # Obtém o CPF digitado
        id_barbeiro = self.id_entry_edit.get()
        nome_cliente = self.nome_entry_edit.get()
        
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            # Consulta o banco de dados para obter os detalhes do cliente com o CPF fornecido
            cursor.execute('''SELECT * FROM Agenda WHERE id = ? AND nome = ? LIMIT 1''', (id_barbeiro, nome_cliente))
            agenda = cursor.fetchone()

            if not agenda:
                self.result_text_edit.config(state=tk.NORMAL)
                self.result_text_edit.delete('1.0', tk.END)
                self.result_text_edit.insert(tk.END, 'Agendamento inexistente')
                self.result_text_edit.config(state=tk.DISABLED)
                return
            
            if agenda:
                # Se o cliente existir, preenche os campos de entrada com os detalhes do cliente
                self.nome_entry_edit.delete(0, tk.END)
                self.nome_entry_edit.insert(tk.END, agenda[1])

                self.data_entry_edit.delete(0, tk.END)
                self.data_entry_edit.insert(tk.END, agenda[2])

                self.hora_entry_edit.delete(0, tk.END)
                self.hora_entry_edit.insert(tk.END, agenda[3])

                self.result_text_edit.config(state=tk.NORMAL)
                self.result_text_edit.delete('1.0', tk.END)
                self.result_text_edit.insert(tk.END, f"ID: {agenda[0]}\nNome: {agenda[1]}\nData: {agenda[2]}\nHora: {agenda[3]}\n")
                self.result_text_edit.config(state=tk.DISABLED)
                
            else:
                messagebox.showinfo('Agendamento não encontrado', 'ID fornecido não encontrado.')
        
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar Agendamento: {err}')

        finally:
            cursor.close()
            conexao.close()

    def janela_edicao_agenda(self):
        self.edit_window = tk.Toplevel(self.master)
        self.edit_window.title('Edição de Agendamento')

        # Result Text
        self.result_text_edit = tk.Text(self.edit_window, height=10, width=50)
        self.result_text_edit.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.result_text_edit.config(state=tk.NORMAL)
        self.result_text_edit.insert(tk.END, 'Agenda a ser alterado')
        self.result_text_edit.config(state=tk.DISABLED)

        # Labels e Entradas
        self.id_label = tk.Label(self.edit_window, text='ID do Barbeiro:')
        self.id_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.id_entry_edit = tk.Entry(self.edit_window)
        self.id_entry_edit.grid(row=1, column=1, padx=10, pady=5)

        self.nome_label = tk.Label(self.edit_window, text='Nome do Cliente:')
        self.nome_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.nome_entry_edit = tk.Entry(self.edit_window)
        self.nome_entry_edit.grid(row=2, column=1, padx=10, pady=5)

        self.data_label = tk.Label(self.edit_window, text='Data:')
        self.data_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.data_entry_edit = tk.Entry(self.edit_window)
        self.data_entry_edit.grid(row=3, column=1, padx=10, pady=5)

        self.hora_label = tk.Label(self.edit_window, text='hora:')
        self.hora_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        self.hora_entry_edit = tk.Entry(self.edit_window)
        self.hora_entry_edit.grid(row=4, column=1, padx=10, pady=5)

        # Botões
        self.search_button = tk.Button(self.edit_window, text='Buscar', command=self.buscar_agenda_edit)
        self.search_button.grid(row=1, column=2, padx=10, pady=5, sticky=tk.W)

        self.button_atualizar = tk.Button(self.edit_window, text='Atualizar', command=self.atualizar_agenda)
        self.button_atualizar.grid(row=5, column=1, padx=10, pady=10)

        self.button_excluir = tk.Button(self.edit_window, text='Excluir', command=self.excluir_agenda)
        self.button_excluir.grid(row=5, column=2, padx=10, pady=10)

    def editar_agenda(self):
        termo = self.search_entry.get()
                

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()
            
            if not termo:
                cursor.execute('''SELECT * FROM Agenda''')  # Consulta SQL para selecionar todos os clientes
            else:
                cursor.execute('''SELECT * FROM Agenda WHERE nome LIKE ? OR id = ?''', ('%' + termo + '%', termo))
            
            agendamento = cursor.fetchall()

            self.result_text_edit.config(state=tk.NORMAL)
            self.result_text_edit.delete('1.0', tk.END)
            for agenda in agendamento:
                id = agenda[0]
                nome = agenda[1]
                data = agenda[2]
                hora = agenda[3]
                texto_formatado = f"ID: {id}\nNome: {nome}\nData: {data}\nHora: {hora}\n\n"
                self.result_text_edit.insert(tk.END, texto_formatado)
            self.result_text_edit.config(state=tk.DISABLED)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar Agendamento: {err}')

        finally:
            cursor.close()
            conexao.close()

    def atualizar_agenda(self):
        id_barbeiro = self.id_entry_edit.get()
        nome_cliente = self.nome_entry_edit.get()  
        data = self.data_entry_edit.get()  
        hora = self.hora_entry_edit.get()

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''UPDATE Agenda SET nome=?, data=?, hora=? WHERE id=?''', (nome_cliente, data, hora, id_barbeiro))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Agendamento atualizado com sucesso!')

            self.buscar_agenda()
            self.zerar()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao atualizar Agendamento: {err}')

        finally:
            cursor.close()
            conexao.close()

    def excluir_agenda(self):
        id_barbeiro = self.id_entry_edit.get()
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este agendamento?")
        
        if confirmar:
            try:
                conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
                cursor = conexao.cursor()
                cursor.execute('''DELETE FROM Agenda WHERE id=?''', (id_barbeiro,))
                conexao.commit()
                messagebox.showinfo('Sucesso', 'Agendamento excluído com sucesso!')
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete('1.0', tk.END)
                self.result_text.config(state=tk.DISABLED)
            except conn.DatabaseError as err:
                messagebox.showerror('Erro', f'Erro ao excluir Agendamento: {err}')
            finally:
                cursor.close()
                conexao.close()

    def deletar_agenda(self, id):
        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''DELETE FROM Agenda WHERE id=?''', (id,))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Agendamento excluído com sucesso!')
            self.buscar_agenda()  # Atualiza a lista de clientes após exclusão

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao excluir agendamento: {err}')

        finally:
            cursor.close()
            conexao.close()

    def voltar(self):
        self.master.destroy()
        root = tk.Tk()
        app = BarberApp(root)
        root.mainloop()

class ServicesMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Menu de Serviços')
        self.master.geometry('600x400')

        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack(pady=20)

        self.search_entry_label = tk.Label(self.search_frame, text='Digite o Nome do Cliente:')
        self.search_entry_label.grid(row=0, column=0)

        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.grid(row=0, column=1)
        
        self.search_button = tk.Button(self.search_frame, text='Buscar', command=self.buscar_servicos)
        self.search_button.grid(row=0, column=2, padx=10)

        self.result_frame = tk.Frame(self.master)
        self.result_frame.pack(pady=20)

        self.result_text = tk.Text(self.result_frame, height=3, width=60)
        self.result_text.pack()

        self.services_frame = tk.Frame(self.master)
        self.services_frame.pack(pady=20)

        self.services_label = tk.Label(self.services_frame, text='Selecione o(s) Serviço(s):')
        self.services_label.grid(row=0, column=0, columnspan=2)

        self.service_options = [('Corte de Tesoura', 50), ('Corte de Máquina', 40), ('Tesoura e Máquina', 60), ('Barba', 30)]
        self.selected_services = []

        num_cols = 2

        self.boolean_vars = [tk.BooleanVar() for _ in range(len(self.service_options))]

        for i, (service, value) in enumerate(self.service_options):
            row = i // num_cols  # Calcula o número da linha
            col = i % num_cols   # Calcula o número da coluna
            var = self.boolean_vars[i]  # Usa a variável de controle criada anteriormente
            checkbox = tk.Checkbutton(self.services_frame, text=service, variable=var, onvalue=True, offvalue=False, command=self.atualizar_valor)
            checkbox.grid(row=row+1, column=col, sticky='w', padx=10, pady=5)
            self.selected_services.append((var, value))  # Armazena a variável de controle e o valor do serviço

        self.valor_label = tk.Label(self.services_frame, text='Valor do Serviço:')
        self.valor_label.grid(row=len(self.service_options)+1, column=0, sticky='w', pady=(10, 0))

        self.valor_entry = tk.Entry(self.services_frame)
        self.valor_entry.grid(row=len(self.service_options)+1, column=1, pady=(10, 0))

        self.finalizar_button = tk.Button(self.services_frame, text='Finalizar', command=self.finalizar_servicos)
        self.finalizar_button.grid(row=len(self.service_options)+2, columnspan=2, pady=10)

        self.voltar_button = tk.Button(self.master, text='Voltar', command=self.voltar)
        self.voltar_button.pack(pady=10) 

    def atualizar_valor(self):
        total = 0
        for var, value in self.selected_services:
            if var.get():
                total += value
        self.valor_entry.delete(0, tk.END)
        self.valor_entry.insert(0, str(total))

    def buscar_servicos(self):
        nome_cliente = self.search_entry.get()

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''SELECT * FROM Agenda WHERE nome = ?''', (nome_cliente,))
            servicos_agendados = cursor.fetchall()

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)  # Limpa o conteúdo existente
            self.result_text.insert(tk.END, "Resultado da Busca:\n\n")

            if servicos_agendados:
                for registro in servicos_agendados:
                    id_barbeiro, nome_cliente, data, hora = registro
                    self.result_text.insert(tk.END, f'ID Barbeiro: {id_barbeiro}, Cliente: {nome_cliente}, Data: {data}, Hora: {hora}\n')
            else:
                self.result_text.insert(tk.END, f'Nenhum serviço agendado para {nome_cliente}.\n')
            self.result_text.config(state=tk.DISABLED)
                    
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar serviços agendados: {err}')

        finally:
            cursor.close()
            conexao.close()


    def finalizar_servicos(self):
        nome_cliente = self.search_entry.get()

        # Obtém o valor total dos serviços
        valor_total = self.valor_entry.get()

        # Verifica se o cliente e os serviços foram selecionados
        if not nome_cliente:
            messagebox.showerror('Erro', 'Por favor, selecione o cliente.')
            return

        # Verifica se o valor do serviço foi inserido
        if not valor_total:
            messagebox.showerror('Erro', 'Por favor, insira o valor do serviço.')
            return
        
        servicos_selecionados = []
        for var, value in self.selected_services:
            if var.get():
                servico_nome = next(service for service, _ in self.service_options if service == var.get())
                servicos_selecionados.append((servico_nome, value))

        if not servicos_selecionados:
            messagebox.showerror('Erro', 'Por favor, selecione pelo menos um serviço.')
            return

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            for servico_nome, valor_servico in servicos_selecionados:
                cursor.execute('''INSERT INTO Servicos (id, nome, servico, valor) VALUES (?, ?, ?, ?)''', (id_barbeiro, nome_cliente, servico_nome, valor_servico))
            
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Serviço finalizado com sucesso!')

            # Limpa os campos de entrada após finalizar os serviços
            self.search_entry.delete(0, tk.END)
            self.valor_entry.delete(0, tk.END)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao finalizar serviços: {err}')

        finally:
            cursor.close()
            conexao.close()  

    def voltar(self):
        self.master.destroy()
        root = tk.Tk()
        app = BarberApp(root)
        root.mainloop()
    def __init__(self, master):
        self.master = master
        self.master.title('Menu de Serviços')
        self.master.geometry('600x400')

        self.search_frame = tk.Frame(self.master)
        self.search_frame.pack(pady=20)

        self.search_entry_label = tk.Label(self.search_frame, text='Digite o Nome do Cliente:')
        self.search_entry_label.grid(row=0, column=0)

        self.search_entry = tk.Entry(self.search_frame, width=30)
        self.search_entry.grid(row=0, column=1)
        
        self.search_button = tk.Button(self.search_frame, text='Buscar', command=self.buscar_servicos)
        self.search_button.grid(row=0, column=2, padx=10)

        self.result_frame = tk.Frame(self.master)
        self.result_frame.pack(pady=20)

        self.result_text = tk.Text(self.result_frame, height=3, width=60)
        self.result_text.pack()

        self.services_frame = tk.Frame(self.master)
        self.services_frame.pack(pady=20)

        self.services_label = tk.Label(self.services_frame, text='Selecione o(s) Serviço(s):')
        self.services_label.grid(row=0, column=0, columnspan=2)

        self.service_options = [('Corte de Tesoura', 50), ('Corte de Máquina', 40), ('Tesoura e Máquina', 60), ('Barba', 30)]
        self.selected_services = []

        num_cols = 2

        self.boolean_vars = [tk.BooleanVar() for _ in range(len(self.service_options))]

        for i, (service, value) in enumerate(self.service_options):
            row = i // num_cols  # Calcula o número da linha
            col = i % num_cols   # Calcula o número da coluna
            var = tk.BooleanVar()  # Crie uma nova variável booleana para cada botão
            checkbox = tk.Checkbutton(self.services_frame, text=service, variable=var, onvalue=True, offvalue=False, command=self.atualizar_valor)
            checkbox.grid(row=row+1, column=col, sticky='w', padx=10, pady=5)
            self.selected_services.append((var, value))  # Armazena a variável de controle e o valor do serviço

        self.valor_label = tk.Label(self.services_frame, text='Valor do Serviço:')
        self.valor_label.grid(row=3, column=0, sticky='w', pady=(10, 0))

        self.valor_entry = tk.Entry(self.services_frame)
        self.valor_entry.grid(row=3, column=1, pady=(10, 0))

        self.finalizar_button = tk.Button(self.services_frame, text='Finalizar', command=self.finalizar_servicos)
        self.finalizar_button.grid(row=4, columnspan=2, pady=10)

        self.voltar_button = tk.Button(self.master, text='Voltar', command=self.voltar)
        self.voltar_button.pack(pady=10)

    def atualizar_valor(self):
        total = sum(value for var, value in self.selected_services if var.get())
        self.valor_entry.delete(0, tk.END)
        self.valor_entry.insert(0, total)

    def buscar_servicos(self):
        nome_cliente = self.search_entry.get()

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''SELECT * FROM Agenda WHERE nome = ?''', (nome_cliente,))
            servicos_agendados = cursor.fetchall()

            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete('1.0', tk.END)  # Limpa o conteúdo existente
            self.result_text.insert(tk.END, "Resultado da Busca:\n\n")

            if servicos_agendados:
                for registro in servicos_agendados:
                    id_barbeiro, nome_cliente, data, hora = registro
                    self.result_text.insert(tk.END, f'ID Barbeiro: {id_barbeiro}, Cliente: {nome_cliente}, Data: {data}, Hora: {hora}\n')
            else:
                self.result_text.insert(tk.END, f'Nenhum serviço agendado para {nome_cliente}.\n')
            self.result_text.config(state=tk.DISABLED)
                    
        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar serviços agendados: {err}')

        finally:
            cursor.close()
            conexao.close()


    def finalizar_servicos(self):
        nome_cliente = self.search_entry.get()

        # Obtém o valor total dos serviços
        valor_total = self.valor_entry.get()

        # Verifica se o cliente e os serviços foram selecionados
        if not nome_cliente:
            messagebox.showerror('Erro', 'Por favor, selecione o cliente.')
            return

        # Verifica se o valor do serviço foi inserido
        if not valor_total:
            messagebox.showerror('Erro', 'Por favor, insira o valor do serviço.')
            return
        
        servicos_selecionados = []
        for var, value in self.selected_services:
            if var.get():
                servico_nome = next(service for service, _ in self.service_options if service == var.get())
                servicos_selecionados.append((servico_nome, value))

        if not servicos_selecionados:
            messagebox.showerror('Erro', 'Por favor, selecione pelo menos um serviço.')
            return

        try:
            conexao = conn.connect('C:/Users/lucas/Desktop/Faculdade/Projeto RAD Barber/Projeto-RAD/Barber.db')
            cursor = conexao.cursor()

            for servico_nome, valor_servico in servicos_selecionados:
                cursor.execute('''INSERT INTO Servicos (id, nome, servico, valor) VALUES (?, ?, ?, ?)''', (id_barbeiro, nome_cliente, servico_nome, valor_servico))
            
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Serviço finalizado com sucesso!')

            # Limpa os campos de entrada após finalizar os serviços
            self.search_entry.delete(0, tk.END)
            self.valor_entry.delete(0, tk.END)

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao finalizar serviços: {err}')

        finally:
            cursor.close()
            conexao.close()  
        
    def voltar(self):
        self.master.destroy()
        root = tk.Tk()
        app = BarberApp(root)
        root.mainloop()

def main():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
