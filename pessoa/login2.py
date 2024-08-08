import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry  # Importa o DateEntry da biblioteca tkcalendar
import json

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
    
    data_nascimento = data.get_date()  # Obtém a data selecionada usando get_date()

    treinos = {}
    for frame in tab1.winfo_children():
        if isinstance(frame, ttk.LabelFrame) and frame.winfo_children():
            grupo_muscular = frame.cget("text")
            exercicios = []
            for i in range(0, len(frame.winfo_children()), 5):
                exercicio = frame.winfo_children()[i].cget("text")
                repet = frame.winfo_children()[i+2].get()
                series = frame.winfo_children()[i+4].get()
                exercicios.append({"exercicio": exercicio, "repet": repet, "series": series})
            treinos[grupo_muscular] = exercicios

    dados = {
        "formulario": {
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone,
            "mensalidade": mensalidade,
            "data_nascimento": data_nascimento
        },
        "treinos": treinos
    }

    with open('dados.json', 'w') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

    print("Dados salvos com sucesso!")

def novo_cadastro(tab2):
    labelp = ttk.Label(tab1, text="Cadastro feito com sucesso!, vá para a próxima aba")
    labelp.grid(row=12, column=0, columnspan=4, padx=10, pady=5, sticky="w")

    nome = entry.get()
    label1 = ttk.Label(tab2, text="SEU NOME: ")
    texto = ttk.Label(tab2, text=nome)
    label1.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    texto.grid(row=0, column=1, padx=5, pady=5, sticky="w")

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
    date = data.get_date()  # Obtém a data selecionada usando get_date()
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

app = tk.Tk()
app.title("Login")
app.geometry("800x600")

notebook = ttk.Notebook(app)  # Removido bootstyle
notebook.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text="Cadastro")
notebook.add(tab2, text="Informações")

text = ttk.Label(tab1, text="NOME:")
text.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry = ttk.Entry(tab1)
entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

text1 = ttk.Label(tab1, text="ENDEREÇO:")
text1.grid(row=1, column=0, padx=5, pady=5, sticky="w") 
entry1 = ttk.Entry(tab1)
entry1.grid(row=1, column=1, padx=5, pady=5, sticky="w")

text2 = ttk.Label(tab1, text="TELEFONE")
text2.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry2 = ttk.Entry(tab1)
entry2.grid(row=2, column=1, padx=5, pady=5, sticky="w")

check1_var = tk.IntVar()
check2_var = tk.IntVar()
check3_var = tk.IntVar()
check4_var = tk.IntVar()

check1 = ttk.Checkbutton(tab1, text='"90/MÊS (3 VEZES NA SEMANA)"', variable=check1_var)
check1.grid(row=3, column=0, padx=5, pady=5, sticky="w")

check2 = ttk.Checkbutton(tab1, text='"130/MÊS (5 VEZES NA SEMANA)"', variable=check2_var)
check2.grid(row=4, column=0, padx=5, pady=5, sticky="w")

check3 = ttk.Checkbutton(tab1, text='ESPORTES', variable=check3_var)
check3.grid(row=5, column=0, padx=5, pady=5, sticky="w")

check4 = ttk.Checkbutton(tab1, text='FILMES', variable=check4_var)
check4.grid(row=6, column=0, padx=5, pady=5, sticky="w")

ttk.Label(tab1, text="Data de Nascimento:").grid(row=7, column=0, padx=5, pady=5, sticky="w")
data = DateEntry(tab1, width=12, background='darkblue', foreground='white', borderwidth=2)
data.grid(row=7, column=1, padx=5, pady=5, sticky="w")

botao_salvar = ttk.Button(tab1, text="Salvar", command=salvar_dados)
botao_salvar.grid(row=10, column=0, padx=10, pady=10, sticky="w")

botao_cadastrar = ttk.Button(tab1, text="Cadastrar", command=lambda: novo_cadastro(tab2))
botao_cadastrar.grid(row=9, column=0, padx=10, pady=10, sticky="w")

criar_ficha_treino(tab1)

app.mainloop()
