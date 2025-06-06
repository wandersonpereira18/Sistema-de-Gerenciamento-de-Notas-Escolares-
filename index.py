import tkinter as tk  # Importa a biblioteca Tkinter para criar interfaces gráficas
from tkinter import messagebox  # Importa a parte de mensagens do Tkinter para mostrar caixas de diálogo
import sqlite3  # Importa o módulo SQLite para trabalhar com banco de dados

# Lista das disciplinas ordenadas alfabeticamente
disciplinas = sorted([
    "Artes",
    "Biologia",
    "Educação Física",
    "Educação Moral e Cívica",
    "Física",
    "Geografia",
    "História",
    "Inglês",
    "Matemática",
    "Português",
    "Química",
])

cor_fundo = "#f0f4ff"  # Define a cor de fundo para as janelas

# Função que muda a cor do botão quando o mouse passa sobre ele
def on_enter(e):
    e.widget['background'] = '#a0a0ff'  # Cor azul clara ao entrar com o mouse

# Função que retorna a cor do botão ao padrão quando o mouse sai dele
def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'  # Cor padrão do sistema

# Função para estilizar um botão, aplicando aparência e efeitos de mouse
def estilizar_botao(btn):
    btn.config(
        relief="raised",  # Botão com relevo
        bd=3,  # Largura da borda
        bg='SystemButtonFace',  # Cor de fundo padrão
        highlightthickness=1,  # Espessura do destaque
        highlightbackground='#999',  # Cor do destaque da borda
        font=("Arial", 10, "bold"),  # Fonte do texto do botão
        padx=10, pady=5,  # Espaçamento interno horizontal e vertical
        borderwidth=2  # Largura da borda
    )
    # Associa os eventos de mouse para mudar cor ao passar/retirar mouse
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Função para criar o banco de dados e as tabelas, se ainda não existirem
def criar_banco():
    conn = sqlite3.connect("Banco_alunos.db")  # Abre (ou cria) o arquivo do banco
    c = conn.cursor()  # Cria o cursor para executar comandos SQL
    # Cria tabela 'alunos' com colunas matricula, nome, sala e turma
    c.execute('''
    CREATE TABLE IF NOT EXISTS alunos(
        matricula TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        sala INTEGER NOT NULL,
        turma TEXT NOT NULL
    )
    ''')
    # Cria tabela 'notas' com id, matricula (chave estrangeira), disciplina e nota
    c.execute('''
    CREATE TABLE IF NOT EXISTS notas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT NOT NULL,
        disciplina TEXT NOT NULL,
        nota REAL NOT NULL,
        FOREIGN KEY(matricula) REFERENCES alunos(matricula)
    )
    ''')
    conn.commit()  # Salva as alterações no banco
    conn.close()  # Fecha a conexão com o banco

# Função que cria a janela principal do sistema
def criar_menu_principal():
    global janela_menu  # Variável global para a janela principal
    janela_menu = tk.Tk()  # Cria a janela principal
    janela_menu.title("Sistema Escolar")  # Define o título da janela
    janela_menu.geometry("500x300")  # Define o tamanho da janela
    janela_menu.configure(bg=cor_fundo)  # Aplica cor de fundo definida
    janela_menu.resizable(False, False)  # Impede redimensionamento da janela

    # Texto do rodapé com nomes e RGMs dos desenvolvedores
    rodape_texto = """Wanderson pereira do nascimento RGM: 39088863
Renato Miranda de Souza Araujo Alves RGM: 38989611
Ryan Gabriel Gomes Vieira RGM: 39261913
Victor Silva Amador RGM: 38136104"""

    # Cria botões principais da janela com texto, largura e função ao clicar
    btn_cadastrar = tk.Button(
        janela_menu, text="Cadastrar Aluno", width=20, command=criar_janela_cadastro)
    btn_consultar = tk.Button(
        janela_menu, text="Consultar/Atualizar Notas", width=20, command=criar_janela_consulta)
    btn_sair = tk.Button(janela_menu, text="Sair",
                         width=20, command=janela_menu.destroy)  # Fecha a janela

    # Aplica estilo e efeitos aos botões criados
    for btn in (btn_cadastrar, btn_consultar, btn_sair):
        estilizar_botao(btn)

    # Posiciona os botões na janela com espaçamento vertical
    btn_cadastrar.pack(pady=15)
    btn_consultar.pack(pady=15)
    btn_sair.pack(pady=15)

    # Label no rodapé exibindo os nomes e RGMs, alinhado ao fundo da janela
    label_rodape = tk.Label(janela_menu, text=rodape_texto, font=(
        "Arial", 10), justify="center", bg=cor_fundo)
    label_rodape.pack(side="bottom", fill="x", pady=5, padx=10, anchor="w")

    janela_menu.mainloop()  # Inicia o loop principal da janela para ficar visível

# Função que cria a janela de cadastro de alunos
def criar_janela_cadastro():
    cadastro = tk.Toplevel()  # Cria uma nova janela filha da principal
    cadastro.title("Cadastro de Novo Aluno")  # Título da janela
    cadastro.geometry("650x720")  # Tamanho da janela
    cadastro.resizable(False, False)  # Impede redimensionamento
    cadastro.configure(bg=cor_fundo)  # Cor de fundo

    frame = tk.Frame(cadastro, bg=cor_fundo)  # Cria um frame para organizar widgets
    frame.pack(padx=15, pady=15, fill='both', expand=True)  # Posiciona o frame

    # Label título para seção de dados pessoais
    tk.Label(frame, text="Dados Pessoais", font=("Arial", 14, "bold"), bg=cor_fundo).grid(
        row=0, column=0, columnspan=5, sticky='w', pady=(0, 10))

    # Label e campo de entrada para matrícula
    tk.Label(frame, text="Matrícula:", bg=cor_fundo).grid(
        row=1, column=0, sticky='w', padx=5, pady=5)
    entrada_matricula = tk.Entry(frame)
    entrada_matricula.grid(row=1, column=1, sticky='we', padx=5, pady=5)

    # Botão para buscar aluno pelo número da matrícula
    btn_buscar = tk.Button(frame, text="Buscar")
    btn_buscar.grid(row=1, column=2, padx=5, pady=5)
    estilizar_botao(btn_buscar)  # Aplica estilo ao botão buscar

    # Label e campo para nome do aluno
    tk.Label(frame, text="Nome:", bg=cor_fundo).grid(
        row=1, column=3, sticky='w', padx=5, pady=5)
    entrada_nome = tk.Entry(frame)
    entrada_nome.grid(row=1, column=4, sticky='we', padx=5, pady=5)

    # Label e campo para número da sala
    tk.Label(frame, text="Sala:", bg=cor_fundo).grid(
        row=2, column=0, sticky='w', padx=5, pady=5)
    entrada_sala = tk.Entry(frame)
    entrada_sala.grid(row=2, column=1, sticky='we', padx=5, pady=5)

    # Label e campo para turma
    tk.Label(frame, text="Turma:", bg=cor_fundo).grid(
        row=2, column=3, sticky='w', padx=5, pady=5)
    entrada_turma = tk.Entry(frame)
    entrada_turma.grid(row=2, column=4, sticky='we', padx=5, pady=5)

    # Label título para seção de matérias
    tk.Label(frame, text="Matérias", font=("Arial", 14, "bold"), bg=cor_fundo).grid(
        row=3, column=0, columnspan=5, sticky='w', pady=(20, 10))

    entradas_notas = {}  # Dicionário para guardar entradas de notas
    linhas = (len(disciplinas) + 1) // 2  # Número de linhas para distribuir colunas

    # Loop para criar labels e campos de entrada para cada disciplina e nota
    for i, disc in enumerate(disciplinas):
        row = 4 + (i % linhas)  # Calcula linha
        col = (i // linhas) * 2  # Calcula coluna (duas colunas de disciplinas)
        tk.Label(frame, text=f"{disc}:", bg=cor_fundo).grid(
            row=row, column=col, sticky='w', padx=5, pady=3)
        entrada = tk.Entry(frame, width=10)
        entrada.grid(row=row, column=col + 1, sticky='we', padx=5, pady=3)
        entradas_notas[disc] = entrada  # Guarda a entrada no dicionário

    # Função para salvar os dados digitados no banco de dados
    def salvar_dados():
        matricula = entrada_matricula.get().strip()  # Lê matrícula e remove espaços
        nome = entrada_nome.get().strip()  # Lê nome e remove espaços
        sala = entrada_sala.get().strip()  # Lê sala e remove espaços
        turma = entrada_turma.get().strip()  # Lê turma e remove espaços

        # Verifica se campos pessoais obrigatórios foram preenchidos
        if not matricula or not nome or not sala or not turma:
            messagebox.showerror("Erro", "Por favor, preencha todos os dados pessoais.")
            return

        try:
            sala_int = int(sala)  # Converte sala para inteiro
        except ValueError:
            messagebox.showerror("Erro", "Sala deve ser um número inteiro.")
            return

        # Abre conexão com banco
        conn = sqlite3.connect("Banco_alunos.db")
        c = conn.cursor()

        # Insere ou atualiza dados na tabela alunos
        c.execute('''
            INSERT OR REPLACE INTO alunos (matricula, nome, sala, turma)
            VALUES (?, ?, ?, ?)
        ''', (matricula, nome, sala_int, turma))

        # Apaga as notas antigas para esta matrícula
        c.execute('DELETE FROM notas WHERE matricula = ?', (matricula,))

        # Insere as notas para cada disciplina
        for disc, entrada in entradas_notas.items():
            nota_text = entrada.get().strip()
            if nota_text:
                try:
                    nota_float = float(nota_text)  # Tenta converter nota para float
                    c.execute('INSERT INTO notas (matricula, disciplina, nota) VALUES (?, ?, ?)',
                              (matricula, disc, nota_float))
                except ValueError:
                    messagebox.showerror("Erro", f"Nota inválida para {disc}.")
                    conn.rollback()
                    conn.close()
                    return

        conn.commit()  # Salva as alterações
        conn.close()  # Fecha conexão

        messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

    # Botão para salvar dados, chama a função salvar_dados ao clicar
    btn_salvar = tk.Button(frame, text="Salvar", command=salvar_dados)
    btn_salvar.grid(row=20, column=0, pady=15, padx=5)
    estilizar_botao(btn_salvar)  # Aplica estilo ao botão salvar

    # Botão para fechar janela de cadastro e voltar ao menu
    btn_voltar = tk.Button(frame, text="Voltar ao Menu", command=cadastro.destroy)
    btn_voltar.grid(row=20, column=1, pady=15, padx=5)
    estilizar_botao(btn_voltar)

# Função para criar janela de consulta e atualização de notas
def criar_janela_consulta():
    consulta = tk.Toplevel()  # Cria janela filha
    consulta.title("Consultar e Atualizar Notas")  # Título da janela
    consulta.geometry("700x500")  # Tamanho
    consulta.resizable(False, False)  # Sem redimensionar
    consulta.configure(bg=cor_fundo)  # Fundo

    frame = tk.Frame(consulta, bg=cor_fundo)  # Frame para organizar widgets
    frame.pack(padx=15, pady=15, fill='both', expand=True)

    # Label e campo de entrada para matrícula do aluno
    tk.Label(frame, text="Matrícula:", bg=cor_fundo).grid(
        row=0, column=0, sticky='w', padx=5, pady=5)
    entrada_matricula = tk.Entry(frame)
    entrada_matricula.grid(row=0, column=1, sticky='we', padx=5, pady=5)

    # Botão para buscar notas do aluno por matrícula
    btn_buscar = tk.Button(frame, text="Buscar")
    btn_buscar.grid(row=0, column=2, padx=5, pady=5)
    estilizar_botao(btn_buscar)

    # Label para mostrar o nome do aluno (vazio inicialmente)
    label_nome = tk.Label(frame, text="", font=("Arial", 12, "bold"), bg=cor_fundo)
    label_nome.grid(row=1, column=0, columnspan=3, sticky='w', pady=5)

    # Frame para listar disciplinas e notas
    frame_notas = tk.Frame(frame, bg=cor_fundo)
    frame_notas.grid(row=2, column=0, columnspan=3, sticky='nsew')

    # Adiciona cabeçalhos
    tk.Label(frame_notas, text="Disciplina", bg=cor_fundo,
             font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame_notas, text="Nota", bg=cor_fundo,
             font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)

    entradas_notas = {}  # Dicionário para guardar campos de nota por disciplina

    # Cria labels para disciplinas e entradas para notas (inicialmente vazias)
    for i, disc in enumerate(disciplinas, start=1):
        tk.Label(frame_notas, text=disc, bg=cor_fundo).grid(row=i, column=0, sticky='w', padx=5, pady=3)
        entrada = tk.Entry(frame_notas, width=10)
        entrada.grid(row=i, column=1, sticky='we', padx=5, pady=3)
        entradas_notas[disc] = entrada

    # Função para buscar as notas no banco e preencher os campos
    def buscar_notas():
        matricula = entrada_matricula.get().strip()  # Lê matrícula digitada
        if not matricula:
            messagebox.showerror("Erro", "Digite uma matrícula para buscar.")
            return

        conn = sqlite3.connect("Banco_alunos.db")
        c = conn.cursor()

        # Busca dados do aluno
        c.execute("SELECT nome FROM alunos WHERE matricula = ?", (matricula,))
        aluno = c.fetchone()
        if not aluno:
            messagebox.showerror("Erro", "Aluno não encontrado.")
            conn.close()
            return
        label_nome.config(text=f"Nome: {aluno[0]}")  # Exibe nome na label

        # Busca notas do aluno
        c.execute("SELECT disciplina, nota FROM notas WHERE matricula = ?", (matricula,))
        notas = c.fetchall()

        # Limpa as entradas antes de preencher
        for entrada in entradas_notas.values():
            entrada.delete(0, tk.END)

        # Preenche os campos com as notas encontradas
        for disc, nota in notas:
            if disc in entradas_notas:
                entradas_notas[disc].insert(0, str(nota))

        conn.close()

    btn_buscar.config(command=buscar_notas)  # Associa a função ao botão buscar

    # Função para atualizar as notas no banco
    def atualizar_notas():
        matricula = entrada_matricula.get().strip()
        if not matricula:
            messagebox.showerror("Erro", "Digite uma matrícula para atualizar.")
            return

        conn = sqlite3.connect("Banco_alunos.db")
        c = conn.cursor()

        # Verifica se aluno existe
        c.execute("SELECT * FROM alunos WHERE matricula = ?", (matricula,))
        if not c.fetchone():
            messagebox.showerror("Erro", "Aluno não encontrado.")
            conn.close()
            return

        # Atualiza as notas, removendo as antigas e inserindo as novas
        c.execute("DELETE FROM notas WHERE matricula = ?", (matricula,))
        for disc, entrada in entradas_notas.items():
            nota_text = entrada.get().strip()
            if nota_text:
                try:
                    nota_float = float(nota_text)
                    c.execute("INSERT INTO notas (matricula, disciplina, nota) VALUES (?, ?, ?)",
                              (matricula, disc, nota_float))
                except ValueError:
                    messagebox.showerror("Erro", f"Nota inválida para {disc}.")
                    conn.rollback()
                    conn.close()
                    return

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Notas atualizadas com sucesso!")

    # Botão para atualizar as notas, chama a função atualizar_notas
    btn_atualizar = tk.Button(frame, text="Atualizar Notas", command=atualizar_notas)
    btn_atualizar.grid(row=3, column=0, pady=15, padx=5)
    estilizar_botao(btn_atualizar)

    # Botão para fechar janela de consulta e voltar ao menu principal
    btn_voltar = tk.Button(frame, text="Voltar ao Menu", command=consulta.destroy)
    btn_voltar.grid(row=3, column=1, pady=15, padx=5)
    estilizar_botao(btn_voltar)

# Cria o banco de dados e tabelas, caso não existam
criar_banco()

# Inicia a aplicação mostrando o menu principal
criar_menu_principal()

