import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os


lista_exercicios = []

def adicionar_exercicio():
    exercicio = entry_exercicio.get()
    series = entry_series.get()
    repeticoes = entry_repeticoes.get()

    if exercicio and series and repeticoes:
        lista_exercicios.append({"exercicio": exercicio, "series": series, "repeticoes": repeticoes})
        atualizar_lista_exercicios()
        entry_exercicio.delete(0, tk.END)
        entry_series.delete(0, tk.END)
        entry_repeticoes.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos do exercício!")

def atualizar_lista_exercicios():
    lista_exercicios_texto.config(state=tk.NORMAL)
    lista_exercicios_texto.delete(1.0, tk.END)
    for exercicio in lista_exercicios:
        lista_exercicios_texto.insert(tk.END, f"Exercício: {exercicio['exercicio']}, Séries: {exercicio['series']}, Repetições: {exercicio['repeticoes']}\n")
    lista_exercicios_texto.config(state=tk.DISABLED)

def salvar_dados():
    nome = entry_nome.get()
    endereco = entry_endereco.get()
    telefone = entry_telefone.get()
    mensalidade = mensalidade_var.get()
    data_nascimento = data.get_date().strftime("%Y-%m-%d")
    treinos = carregar_treinos()

    novo_dado = {
        "nome": nome,
        "endereco": endereco,
        "telefone": telefone,
        "mensalidade": mensalidade,
        "data_nascimento": data_nascimento,
        "treinos": treinos
    }


    salvar_mensalidade(nome, mensalidade)

    if os.path.exists('dados.json'):
        with open('dados.json', 'r', encoding="utf-8") as f:
            try:
                dados = json.load(f)
                if isinstance(dados, dict):
                    dados = [dados]
            except json.JSONDecodeError:
                dados = []
    else:
        dados = []


    dados = [dado for dado in dados if dado['nome'] != nome]
    dados.append(novo_dado)


    with open('dados.json', 'w', encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    atualizar_combobox()
    atualizar_lista_pessoas()
    messagebox.showinfo('Sucesso', 'Dados salvos com sucesso!')

def salvar_mensalidade(nome, mensalidade):
    if os.path.exists('mensalidade.json'):
        with open('mensalidade.json', 'r', encoding="utf-8") as f:
            try:
                dados_mensalidade = json.load(f)
            except json.JSONDecodeError:
                dados_mensalidade = {}
    else:
        dados_mensalidade = {}

    dados_mensalidade[nome] = mensalidade

    with open('mensalidade.json', 'w', encoding="utf-8") as f:
        json.dump(dados_mensalidade, f, indent=4, ensure_ascii=False)

def carregar_treinos():
    treinos = {}
    for frame in tab1.winfo_children():
        if isinstance(frame, ttk.LabelFrame) and frame.winfo_children():
            grupo_muscular = frame.cget("text")
            exercicios = []
            for i in range(0, len(frame.winfo_children()), 5):
                widgets = frame.winfo_children()
                if i + 4 < len(widgets):
                    exercicio = widgets[i].cget("text")
                    repet = widgets[i + 2].get()
                    series = widgets[i + 4].get()
                    exercicios.append({"exercicio": exercicio, "repet": repet, "series": series})
            if exercicios:
                treinos[grupo_muscular] = exercicios
    return treinos

def atualizar_combobox():
    dados = carregar_dados()
    combobox['values'] = [dado['nome'] for dado in dados]
    atualizar_lista_pessoas()

def mostrar_informacoes(event):
    nome_selecionado = combobox.get()
    dados = carregar_dados()
    for dado in dados:
        if dado['nome'] == nome_selecionado:
            atualizar_info_pessoa(dado)
            return

def carregar_dados():
    if os.path.exists('dados.json'):
        with open('dados.json', 'r', encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def carregar_mensalidade(nome):
    if os.path.exists('mensalidade.json'):
        with open('mensalidade.json', 'r', encoding="utf-8") as f:
            try:
                dados_mensalidade = json.load(f)
                return dados_mensalidade.get(nome, "Nenhuma mensalidade encontrada")
            except json.JSONDecodeError:
                return "Nenhuma mensalidade encontrada"
    return "Nenhuma mensalidade encontrada"

def atualizar_info_pessoa(dado):
    for widget in info_frame.winfo_children():
        widget.destroy()

    ttk.Label(info_frame, text=f"Nome: {dado['nome']}").pack(pady=2)
    ttk.Label(info_frame, text=f"Endereço: {dado['endereco']}").pack(pady=2)
    ttk.Label(info_frame, text=f"Telefone: {dado['telefone']}").pack(pady=2)
    ttk.Label(info_frame, text=f"Data de Nascimento: {dado['data_nascimento']}").pack(pady=2)
    
    mensalidade = carregar_mensalidade(dado['nome'])
    ttk.Label(info_frame, text=f"Mensalidade: {mensalidade}").pack(pady=2)
    
    ttk.Label(info_frame, text="Treinos:").pack(pady=2)
    if dado['treinos']:
        for grupo_muscular, exercicios in dado['treinos'].items():
            ttk.Label(info_frame, text=f"{grupo_muscular}:").pack(pady=2)
            for exercicio in exercicios:
                ttk.Label(info_frame, text=f"Exercício: {exercicio['exercicio']}, Séries: {exercicio['series']}, Repetições: {exercicio['repet']}").pack(pady=2)
    else:
        ttk.Label(info_frame, text="Nenhum treino registrado").pack(pady=2)

def atualizar_lista_pessoas():
    for widget in lista_pessoas_frame.winfo_children():
        widget.destroy()

    dados = carregar_dados()
    for dado in dados:
        nome = dado['nome']
        nome_label = ttk.Label(lista_pessoas_frame, text=nome, foreground='red')
        nome_label.pack(anchor='w', padx=10)
        
        pago_button = ttk.Button(lista_pessoas_frame, text="Pago", command=lambda n=nome: marcar_pago(n, nome_label))
        pago_button.pack(anchor='w', padx=10, pady=2)

def marcar_pago(nome, label):
    label.config(foreground='green')


def criar_interface_principal():
    global combobox, info_frame, entry_nome, entry_endereco, entry_telefone, data, mensalidade_var
    global entry_exercicio, entry_series, entry_repeticoes, lista_exercicios_texto
    global lista_pessoas_frame

    lista_exercicios = []

    app = tk.Tk()
    app.title("Cadastro")
    app.geometry("800x600")

    notebook = ttk.Notebook(app)
    notebook.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    global tab1, tab2
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)
    notebook.add(tab1, text="Cadastro")
    notebook.add(tab2, text="Confirmar Cadastro")
    notebook.add(tab3, text="Lista de Pessoas")

    entry_nome = ttk.Entry(tab1, width=30)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)
    ttk.Label(tab1, text="Nome Completo:").grid(row=0, column=0, padx=10, pady=5, sticky="w")

    entry_endereco = ttk.Entry(tab1, width=30)
    entry_endereco.grid(row=1, column=1, padx=10, pady=5)
    ttk.Label(tab1, text="Endereço:").grid(row=1, column=0, padx=10, pady=5, sticky="w")

    entry_telefone = ttk.Entry(tab1, width=30)
    entry_telefone.grid(row=2, column=1, padx=10, pady=5)
    ttk.Label(tab1, text="Telefone:").grid(row=2, column=0, padx=10, pady=5, sticky="w")

    mensalidade_var = tk.StringVar()
    mensalidade_var.set("")

    ttk.Radiobutton(tab1, text="90/MÊS (3 VEZES NA SEMANA)", variable=mensalidade_var, value="90/MÊS (3 VEZES NA SEMANA)").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ttk.Radiobutton(tab1, text="130/MÊS (5 VEZES NA SEMANA)", variable=mensalidade_var, value="130/MÊS (5 VEZES NA SEMANA)").grid(row=4, column=0, padx=10, pady=5, sticky="w")

    ttk.Label(tab1, text="Data de Nascimento:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
    data = DateEntry(tab1, width=30, date_pattern="dd/mm/yyyy")
    data.grid(row=5, column=1, padx=10, pady=5)

    ttk.Label(tab1, text="Exercício:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
    entry_exercicio = ttk.Entry(tab1, width=30)
    entry_exercicio.grid(row=6, column=1, padx=10, pady=5)

    ttk.Label(tab1, text="Séries:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    entry_series = ttk.Entry(tab1, width=30)
    entry_series.grid(row=7, column=1, padx=10, pady=5)

    ttk.Label(tab1, text="Repetições:").grid(row=8, column=0, padx=10, pady=5, sticky="w")
    entry_repeticoes = ttk.Entry(tab1, width=30)
    entry_repeticoes.grid(row=8, column=1, padx=10, pady=5)

    ttk.Button(tab1, text="Adicionar Exercício", command=adicionar_exercicio).grid(row=9, column=0, padx=10, pady=5, sticky="w")

    ttk.Label(tab1, text="Lista de Exercícios:").grid(row=10, column=0, padx=10, pady=5, sticky="w")
    lista_exercicios_texto = tk.Text(tab1, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
    lista_exercicios_texto.grid(row=11, column=0, columnspan=2, padx=10, pady=5)

    ttk.Button(tab1, text="Salvar Tudo", command=salvar_dados).grid(row=12, column=1, padx=10, pady=5, sticky="e")

    combobox = ttk.Combobox(tab2)
    combobox.grid(row=0, column=0, padx=10, pady=5)
    combobox.bind("<<ComboboxSelected>>", mostrar_informacoes)

    info_frame = ttk.Frame(tab2)
    info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    lista_pessoas_frame = ttk.Frame(tab3)
    lista_pessoas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    atualizar_combobox()

    app.mainloop()

def salvar_usuario(username, password):
    if not os.path.exists('usuarios.json'):
        with open('usuarios.json', 'w', encoding="utf-8") as f:
            json.dump([], f)

    with open('usuarios.json', 'r+', encoding="utf-8") as f:
        usuarios = json.load(f)
        if any(usuario['username'] == username for usuario in usuarios):
            return False
        usuarios.append({"username": username, "password": password})
        f.seek(0)
        json.dump(usuarios, f, indent=4, ensure_ascii=False)
        return True

def confirmar_cadastro():
    username = entry_username1.get()
    password = entry_password1.get()
    confirm_password = entry_confirm.get()

    if password == confirm_password:
        if salvar_usuario(username, password):
            messagebox.showinfo("Cadastro", "Cadastro realizado com sucesso!")
            root1.destroy()
        else:
            messagebox.showerror("Cadastro", "Usuário já existe.")
    else:
        messagebox.showerror("Erro", "As senhas não coincidem")

def cadastro():
    global entry_username1, entry_password1, entry_confirm, root1
    root1 = tk.Tk()
    root1.title("Tela de Cadastro")
    root1.geometry("400x300")

    label_username1 = ttk.Label(root1, text="Usuário:")
    label_username1.pack(pady=5)
    entry_username1 = ttk.Entry(root1)
    entry_username1.pack(pady=5)

    label_password1 = ttk.Label(root1, text="Senha:")
    label_password1.pack(pady=5)
    entry_password1 = ttk.Entry(root1, show="*")
    entry_password1.pack(pady=5)

    label_confirm = ttk.Label(root1, text="Confirmar Senha")
    label_confirm.pack(pady=5)
    entry_confirm = ttk.Entry(root1, show="*")
    entry_confirm.pack(pady=5)

    btn_confirm = ttk.Button(root1, text="Cadastrar", command=confirmar_cadastro)
    btn_confirm.pack(pady=20)

    root1.mainloop()

def login():
    username = entry_username.get()
    password = entry_password.get()

    if verificar_login(username, password):
        root.withdraw()
        criar_interface_principal()
    else:
        messagebox.showerror('Login', 'Credenciais inválidas')

def verificar_login(username, password):
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r', encoding="utf-8") as f:
            usuarios = json.load(f)
            for usuario in usuarios:
                if usuario['username'] == username and usuario['password'] == password:
                    return True
    return False

root = tk.Tk()
root.title("Login")
root.geometry("300x200")

label_username = ttk.Label(root, text="Usuário:")
label_username.pack(pady=5)
entry_username = ttk.Entry(root)
entry_username.pack(pady=5)

label_password = ttk.Label(root, text="Senha:")
label_password.pack(pady=5)
entry_password = ttk.Entry(root, show="*")
entry_password.pack(pady=5)

btn_login = ttk.Button(root, text="Login", command=login)
btn_login.pack(pady=10)

btn_cadastro = ttk.Button(root, text="Cadastro", command=cadastro)
btn_cadastro.pack(pady=5)

root.mainloop()
