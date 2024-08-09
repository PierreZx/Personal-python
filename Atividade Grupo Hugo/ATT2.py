import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os

def cadastro():
    root1 = tk.Toplevel()  # Use Toplevel para criar uma nova janela
    root1.title("Tela de Cadastro")
    root1.geometry("400x300")

    ttk.Label(root1, text="Usuário:").pack(pady=5)
    entry_username1 = ttk.Entry(root1)
    entry_username1.pack(pady=5)

    ttk.Label(root1, text="Senha:").pack(pady=5)
    entry_password1 = ttk.Entry(root1, show="*")
    entry_password1.pack(pady=5)

    ttk.Label(root1, text="Confirmar Senha").pack(pady=5)
    entry_confirm = ttk.Entry(root1, show="*")
    entry_confirm.pack(pady=5)

    def realizar_cadastro():
        usuario = entry_username1.get()
        senha = entry_password1.get()
        confirmar_senha = entry_confirm.get()

        if senha != confirmar_senha:
            messagebox.showerror('Erro', 'As senhas não coincidem!')
            return

        # Aqui você pode adicionar lógica para salvar o novo usuário, por exemplo, em um arquivo
        # Para simplificar, apenas mostramos uma mensagem de sucesso
        messagebox.showinfo('Cadastro', 'Cadastro realizado com sucesso!')
        root1.destroy()  # Fecha a janela de cadastro

    ttk.Button(root1, text="Cadastrar", command=realizar_cadastro).pack(pady=10)


def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == 'v' and password == '1':
        root.withdraw()  # Oculta a tela de login
        create_main_interface()  # Cria e exibe a interface principal
    else:
        messagebox.showerror('Login', 'Credenciais inválidas')


def salvar_dados():
    nome = entry.get()
    endereco = entry1.get()
    telefone = entry2.get()

    mensalidade = []
    if check1_var.get() == 1:
        mensalidade.append("90/MÊS (3 VEZES NA SEMANA)")
    if check2_var.get() == 1:
        mensalidade.append("130/MÊS (5 VEZES NA SEMANA)")

    data_nascimento = data.get_date().strftime("%Y-%m-%d")
    treinos = {}
    for frame in tab1.winfo_children():
        if isinstance(frame, ttk.LabelFrame) and frame.winfo_children():
            grupo_muscular = frame.cget("text")
            exercicios = []
            for i in range(0, len(frame.winfo_children()), 5):
                exercicio = frame.winfo_children()[i].cget("text")
                repet = frame.winfo_children()[i + 2].get()
                series = frame.winfo_children()[i + 4].get()
                exercicios.append({"exercicio": exercicio, "repet": repet, "series": series})
            treinos[grupo_muscular] = exercicios

    novo_dado = {
        "nome": nome,
        "endereco": endereco,
        "telefone": telefone,
        "mensalidade": mensalidade,
        "data_nascimento": data_nascimento,
        "treinos": treinos
    }

    if os.path.exists('dados.json'):
        with open('dados.json', 'r', encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict):
                dados = [dados]
    else:
        dados = []

    dados.append(novo_dado)

    with open('dados.json', 'w', encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    messagebox.showinfo("Salvar", "Dados salvos com sucesso!")

def carregar_dados():
    arquivo_json = 'dados.json'
    
    try:
        with open(arquivo_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except FileNotFoundError:
        dados = []
    except json.JSONDecodeError:
        dados = []

    # Limpa o conteúdo do tab2
    for widget in tab2.winfo_children():
        widget.destroy()

    # Adiciona os dados ao tab2
    for i, dado in enumerate(dados):
        ttk.Label(tab2, text=f"Nome: {dado.get('nome', 'N/A')}").grid(row=i*6, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(tab2, text=f"Endereço: {dado.get('endereco', 'N/A')}").grid(row=i*6+1, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(tab2, text=f"Telefone: {dado.get('telefone', 'N/A')}").grid(row=i*6+2, column=0, padx=5, pady=5, sticky="w")
        ttk.Label(tab2, text=f"Data de Nascimento: {dado.get('data_nascimento', 'N/A')}").grid(row=i*6+3, column=0, padx=5, pady=5, sticky="w")
        
        mensalidades = dado.get('mensalidade', [])
        ttk.Label(tab2, text="Mensalidade:").grid(row=i*6+4, column=0, padx=5, pady=5, sticky="w")
        for j, mensalidade in enumerate(mensalidades):
            ttk.Label(tab2, text=f"- {mensalidade}").grid(row=i*6+5+j, column=0, padx=10, pady=2, sticky="w")


def on_tab_change(event):
    if notebook.index(notebook.select()) == 1:  # Índice 1 é a aba "Informações do Aluno"
        carregar_dados()


def create_main_interface():
    global tab1, tab2, entry, entry1, entry2, data, check1_var, check2_var, notebook

    app = tk.Tk()
    app.title("Cadastro")
    app.geometry("800x600")

    notebook = ttk.Notebook(app)
    notebook.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    notebook.add(tab1, text="Cadastro")
    notebook.add(tab2, text="Informações do Aluno")

    entry = ttk.Entry(tab1, width=30)
    entry.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(tab1, text="Nome Completo:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    entry1 = ttk.Entry(tab1, width=30)
    entry1.grid(row=1, column=1, padx=10, pady=5)
    ttk.Label(tab1, text="Endereço:").grid(row=1, column=0, padx=10, pady=5, sticky="w")

    entry2 = ttk.Entry(tab1, width=30)
    entry2.grid(row=2, column=1, padx=10, pady=5)
    ttk.Label(tab1, text="Telefone:").grid(row=2, column=0, padx=10, pady=5, sticky="w")

    check1_var = tk.IntVar()
    check2_var = tk.IntVar()

    ttk.Checkbutton(tab1, text="90/MÊS (3 VEZES NA SEMANA)", variable=check1_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ttk.Checkbutton(tab1, text="130/MÊS (5 VEZES NA SEMANA)", variable=check2_var).grid(row=4, column=0, padx=10, pady=5, sticky="w")

    ttk.Label(tab1, text="Data de Nascimento:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    data = DateEntry(tab1, width=30, date_pattern="dd/mm/yyyy")
    data.grid(row=7, column=1, padx=10, pady=5)

    ttk.Button(tab1, text="Carregar Dados", command=carregar_dados).grid(row=8, column=0, padx=10, pady=5, sticky="w")
    ttk.Button(tab1, text="Salvar Dados", command=salvar_dados).grid(row=8, column=1, padx=10, pady=5, sticky="e")

    # Vincula a função de carregar dados ao evento de seleção da aba
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)

    app.mainloop()


# Tela de login
root = tk.Tk()
root.title("Tela de Login")
root.geometry("300x200")

entry_username = ttk.Entry(root)
entry_username.pack(pady=5)

entry_password = ttk.Entry(root, show="*")
entry_password.pack(pady=5)

ttk.Button(root, text="Login", command=login).pack(pady=10)
ttk.Button(root, text="Cadastre-se", command=cadastro).pack(pady=5)

root.mainloop()
