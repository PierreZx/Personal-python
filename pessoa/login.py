import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os


def cadastro():
    root1 = tk.Tk()
    root1.title("Tela de Login")
    root1.geometry("400x300")

    label_username1 = ttk.Label(root1, text="Usuário:")
    label_username1.pack(pady=5)
    entry_username1 = ttk.Entry(root1)
    entry_username1.pack(pady=5)

    label_password1 = ttk.Label(root1, text="Senha:")
    label_password1.pack(pady=5)
    entry_password1 = ttk.Entry(root1)
    entry_password1.pack(pady=5)

    label_confirm = ttk.Label(root1, text="Confirmar Senha")
    label_confirm.place(x=150, y=130)
    entry_confirm = ttk.Entry(root1)
    entry_confirm.place(x=138, y=160)

    btn_confirm = ttk.Button(root1, text="Cadastrar", width=10)
    btn_confirm.place(x=160, y=210)


def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == 'vinicius' and password == '142536':
        root.withdraw()
        create_main_interface()
    else:
        messagebox.showerror('login', 'Credenciais inválidas')


def salvar_dados():
    nome = entry.get()
    endereco = entry1.get()
    telefone = entry2.get()

    mensalidade = []
    if check1_var.get() == 1:
        mensalidade.append("90/MÊS (3 VEZES NA SEMANA)")
    if check2_var.get() == 1:
        mensalidade.append("130/MÊS (5 VEZES NA SEMANA)")
    if check3_var.get() == 1:
        mensalidade.append("ESPORTES")
    if check4_var.get() == 1:
        mensalidade.append("FILMES")

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

    print("Dados salvos com sucesso!")


def novo_cadastro(tab2):
    labelp = ttk.Label(tab1, text="Cadastro feito com sucesso!, vá para a próxima aba")
    labelp.grid(row=12, column=0, columnspan=4, padx=10, pady=5, sticky="w")

    nome = entry.get()
    tab3 = tab3.frame()
    label1 = ttk.Label(tab3, text="SEU NOME: ")
    texto = ttk.Label(tab2, text=nome)
    label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    texto.grid(row=0, column=1, padx=5, pady=5)

    endereco = entry1.get()
    label2 = ttk.Label(tab2, text="SEU ENDEREÇO: ")
    texto1 = ttk.Label(tab2, text=endereco)
    label2.grid(row=1, column=0, padx=5, pady=5, sticky="w")
    texto1.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    numero = entry2.get()
    label3 = ttk.Label(tab2, text="SEU NÚMERO: ")
    texto2 = ttk.Label(tab2, text=numero)
    label3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    texto2.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    a = check1_var.get()
    b = check2_var.get()
    c = check3_var.get()
    d = check4_var.get()

    label4 = ttk.Label(tab2, text="MENSALIDADE:")
    label4.grid(row=3, column=0, padx=5, pady=5, sticky="w")

    if a == 1:
        label9 = ttk.Label(tab2, text="90/MÊS (3 VEZES NA SEMANA)")
        label9.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    if b == 1:
        label9 = ttk.Label(tab2, text="130/MÊS (5 VEZES NA SEMANA)")
        label9.grid(row=5, column=0, padx=10, pady=5, sticky="w")

    if c == 1:
        label9 = ttk.Label(tab2, text="ESPORTES")
        label9.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    if d == 1:
        label9 = ttk.Label(tab2, text="FILMES")
        label9.grid(row=7, column=0, padx=10, pady=5, sticky="w")

    lf = ttk.LabelFrame(tab2, text="DATA DE NASCIMENTO")
    lf.grid(row=8, column=0, padx=5, pady=5, columnspan=2, sticky="nsew")
    date = data.get_date().strftime("%Y-%m-%d")
    label_data = ttk.Label(lf, text=date)
    label_data.grid(row=0, column=0, padx=5, pady=5, sticky="w")


def criar_ficha_treino(tab):
    exercicios = {
        "COXAS E GLÚTEOS": [
            ("AGACHAMENTO LIVRE", ""), ("LEG PRESS", ""), ("CADEIRA EXTENSORA", ""), ("CADEIRA FLEXORA", ""),
            ("ADUÇÃO", ""), ("ABDÇÃO", "")
        ],
        "BÍCEPS": [
            ("ROSCA DIRETA", ""), ("ROSCA ALTERNADA", ""), ("ROSCA SCOTT", ""), ("ROSCA MARTELO", "")
        ],
        "OMBROS": [
            ("DESENVOLVIMENTO", ""), ("ELEVAÇÃO FRONTAL", ""), ("ELEVAÇÃO LATERAL", ""), ("ENCOLHIMENTO", "")
        ],
        "PANTURRILHA": [
            ("ELEVAÇÃO DE PANTURRILHA EM PÉ", ""), ("ELEVAÇÃO DE PANTURRILHA SENTADO", "")
        ],
        "ANTEBRAÇO": [
            ("ROSCA INVERSA", ""), ("ROSCA PUNHO", "")
        ],
        "TRAPÉZIO": [("ENCOLHIMENTO", "")]
    }

    row_start = 20
    col = 0

    for grupo_muscular, lista_exercicios in exercicios.items():
        lf = ttk.LabelFrame(tab, text=grupo_muscular)
        lf.grid(row=row_start, column=col, padx=10, pady=10, sticky="nsew")

        for i, (exercicio, _) in enumerate(lista_exercicios):
            ttk.Label(lf, text=exercicio).grid(row=i, column=0, padx=5, pady=2, sticky="w")

            ttk.Label(lf, text="REPET").grid(row=i, column=1, padx=5, pady=2, sticky="w")
            ttk.Entry(lf, width=5).grid(row=i, column=2, padx=5, pady=2)

            ttk.Label(lf, text="SÉRIES").grid(row=i, column=3, padx=5, pady=2, sticky="w")
            ttk.Entry(lf, width=5).grid(row=i, column=4, padx=5, pady=2)

        col += 1
        if col == 3:
            col = 0
            row_start += 1


def create_main_interface():
    app = tk.Tk()
    app.title("Cadastro")
    app.geometry("800x600")

    notebook = ttk.Notebook(app)
    notebook.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    global tab1, tab2
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    notebook.add(tab1, text="Cadastro")
    notebook.add(tab2, text="Confirmar Cadastro")

    global entry, entry1, entry2, data, check1_var, check2_var, check3_var, check4_var
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
    check3_var = tk.IntVar()
    check4_var = tk.IntVar()

    ttk.Checkbutton(tab1, text="90/MÊS (3 VEZES NA SEMANA)", variable=check1_var).grid(row=3, column=0, padx=10, pady=5, sticky="w")
    ttk.Checkbutton(tab1, text="130/MÊS (5 VEZES NA SEMANA)", variable=check2_var).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    ttk.Checkbutton(tab1, text="ESPORTES", variable=check3_var).grid(row=5, column=0, padx=10, pady=5, sticky="w")
    ttk.Checkbutton(tab1, text="FILMES", variable=check4_var).grid(row=6, column=0, padx=10, pady=5, sticky="w")

    ttk.Label(tab1, text="Data de Nascimento:").grid(row=7, column=0, padx=10, pady=5, sticky="w")
    data = DateEntry(tab1, width=30, date_pattern="dd/mm/yyyy")
    data.grid(row=7, column=1, padx=10, pady=5)

    ttk.Button(tab1, text="Confirmar Cadastro", command=lambda: novo_cadastro(tab2)).grid(row=8, column=0, padx=10, pady=5, sticky="w")
    ttk.Button(tab1, text="Salvar Dados", command=salvar_dados).grid(row=8, column=1, padx=10, pady=5, sticky="e")

    criar_ficha_treino(tab1)

    app.mainloop()


root = tk.Tk()
root.title("Tela de Login")
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

btn_register = ttk.Button(root, text="Cadastre-se", command=cadastro)
btn_register.pack(pady=5)

root.mainloop()
