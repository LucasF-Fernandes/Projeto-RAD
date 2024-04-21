import sqlite3 as conn
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

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
        
        if usuario == 'a' and senha == 'a':
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.master.destroy()
            # Após o login bem-sucedido, abra a janela principal
            root = tk.Tk()
            app = BarberApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Login", "Nome de usuário ou senha incorretos!")

class BarberApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Barbearia App")

        # Configurações da janela principal
        self.master.geometry("600x400")  # Definindo o tamanho da janela

        # Adicionando um rótulo
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

        self.button_serviços = tk.Button(self.master, text="Serviços", command=self.open_janela_serviço)
        self.button_serviços.pack(pady=5)

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

    def open_janela_serviço(self):
        self.master.withdraw()
        janela_serviço = tk.Tk()      
        janela_serviço.title('Serviços')
        services_menu = ServicesMenu(janela_serviço)
        janela_serviço.mainloop()


class ClientesMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Clientes')
        self.master.geometry('600x400')

        self.button_add = tk.Button(self.master, text='Cadastrar Cliente', command=self.janela_de_cadastro)
        self.button_add.pack(pady=20)

        self.button_show = tk.Button(self.master, text='Buscar Clientes', command=self.janela_de_listar)
        self.button_show.pack(pady=10)
        
        label_message = tk.Label(self.master, text='Cliente')
        label_message.pack(padx=10, pady=10)
        
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

        self.nascimento_label = tk.Label(self.cadastro_window, text='Data de Nascimento: (ex.: AAAA-MM-DD) ')
        self.nascimento_label.grid(row=2, column=0)
        self.nascimento_entry = DateEntry (self.cadastro_window, width=12, backgorund='darkblue', foreground='white', borderwidth=2)
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
            conexao = conn.connect('C:\Users\lucas\Desktop\Faculdade\Projeto RAD Barber\Projeto-RAD\Barber.db')
            cursor = conexao.cursor()


            cursor.execute('''INSERT INTO Cliente (cpf, nome, nascimento, contato) VALUES (?, ?, ?, ?);''', (cpf, nome, nascimento, contato))
            conexao.commit()

            messagebox.showinfo('Sucesso', 'Cliente cadastrado com sucesso!')
            self.clear_entries()

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao inserir cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def clear_entries(self):
        self.cpf_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.nascimento_entry.set_date('')  
        self.contato_entry.delete(0, tk.END)
        
    def janela_de_listar(self):
        self.janela_listar = tk.Toplevel(self.master)
        self.janela_listar.title('Busca de Clientes')

        cpf_label =tk.Label(self.janela_listar, text='Buscar por CPF:')
        cpf_label.grid(row=0, column=0, padx=10, pady=10)
        self.cpf_entry = tk.Entry(self.janela_listar)
        self.cpf_entry.grid(row=0, column=1, padx=10, pady=10)

        buscar_button = tk.Button(self.janela_listar, text='Buscar', command=self.buscar_cliente)
        buscar_button.grid(row=0, column=2, padx=10, pady=10)

        atualizar_button = tk.Button(self.janela_listar, text='Atualizar', command=self.atualizar_cliente_selecionado)
        atualizar_button.grid(row=1, column=0, padx=10, pady=10)

        excluir_button = tk.Button(self.janela_listar, text='Excluir', command=self.excluir_cliente_selecionado)
        excluir_button.grid(row=1, column=1, padx=10, pady=10)

        self.button_back = tk.Button(self.master, text = 'Voltar', command = self.voltar)
        self.button_back.pack(pady=10)

    def buscar_cliente(self):
        cpf = self.cpf_entry.get()
        if not cpf:
            messagebox.showerror('Erro', 'Digite um CPF para buscar.')
            return

        try:
            conexao = conn.connect('./Barber.db')
            cursor = conexao.cursor()

            cursor.execute('''SELECT * FROM Cliente WHERE cpf = ?;''', (cpf,))
            cliente = cursor.fetchone()

            if cliente:
                self.result_text.delete('1.0', tk.END)  # Limpa o Text antes de exibir novo resultado
                self.result_text.insert(tk.END, f'CPF: {cliente[0]}\nNome: {cliente[1]}\nNascimento: {cliente[2]}\nContato: {cliente[3]}')
            else:
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, 'Cliente não encontrado.')

        except conn.DatabaseError as err:
            messagebox.showerror('Erro', f'Erro ao buscar cliente: {err}')

        finally:
            cursor.close()
            conexao.close()

    def voltar(self):
        # Destroi a janela atual e recria a janela de opções
        self.master.destroy()
        options_window = tk.Tk()
        options_app = BarberApp(options_window)
        options_window.mainloop()


class BarberMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Barbeiros')

        self.master.geometry('600x400')

        self.button_back = tk.Button(self.master, text = 'Voltar', command = self.back_to_menu)
        self.button_back.pack(pady=10)

        label_message = tk.label(self.master, text='Barbeiro')
        label_message.pack(padx=10, pady=10)

    def back_to_menu(self):
        # Destroi a janela atual e recria a janela de opções
        self.master.destroy()
        options_window = tk.Tk()
        options_app = BarberApp(options_window)
        options_window.mainloop()

class AgendaMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Agenda')

        self.master.geometry('600x400')
        
        self.button_back = tk.Button(self.master, text = 'Voltar', command = self.back_to_menu)
        self.button_back.pack(pady=10)

        label_message = tk.label(self.master, text='Agenda')
        label_message.pack(padx=10, pady=10)

    def back_to_menu(self):
        # Destroi a janela atual e recria a janela de opções
        self.master.destroy()
        options_window = tk.Tk()
        options_app = BarberApp(options_window)
        options_window.mainloop()

class ServicesMenu:
    def __init__(self, master):
        self.master = master
        self.master.title('Serviços')

        self.master.geometry('600x400')
        
        self.button_back = tk.Button(self.master, text = 'Voltar', command = self.back_to_menu)
        self.button_back.pack(pady=10)

        label_message = tk.label(self.master, text='Serviços')
        label_message.pack(padx=10, pady=10)

    def back_to_menu(self):
        # Destroi a janela atual e recria a janela de opções
        self.master.destroy()
        options_window = tk.Tk()
        options_app = BarberApp(options_window)
        options_window.mainloop()   

def main():
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
