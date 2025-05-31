# Importa as ferramentas que vamos usar
import tkinter as tk  # Usamos para criar janelas e botões
from tkinter import messagebox  # Usamos para mostrar mensagens (como alerta)
# Usamos para falar com o banco de dados (onde guardamos as informações)
import sqlite3

# Lista de matérias da escola, em ordem alfabética
disciplinas = sorted([
    "Matemática",
    "Português",
    "História",
    "Biologia",
    "Física",
    "Química",
    "Geografia",
    "Educação Física",
    "Artes",
    "Inglês",
    "Educação Moral e Cívica"
])

# --- EFEITO DE COR QUANDO PASSA O MOUSE NO BOTÃO ---


def on_enter(e):
    # Quando o mouse entra, o botão fica azul claro
    e.widget['background'] = '#a0a0ff'


def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'  # Quando sai, volta ao normal


# Cor do fundo da tela
cor_fundo = "#f0f4ff"

# Deixando os botões bonitinhos


def estilizar_botao(btn):
    btn.config(
        relief="raised",  # deixa o botão com efeito de relevo
        bd=3,  # espessura da borda
        bg='SystemButtonFace',  # cor do botão
        highlightthickness=1,  # brilho da borda
        highlightbackground='#999',
        font=("Arial", 10, "bold"),  # fonte do texto do botão
        padx=10, pady=5,  # espaço interno do botão
        borderwidth=2  # espessura da borda
    )
    # Quando o mouse entra e sai do botão, muda a cor
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ---------- JANELA DE CADASTRAR ALUNO ----------


def criar_janela_cadastro():
    # Criamos uma nova janelinha
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Novo Aluno")
    cadastro.geometry("600x700")  # Tamanho da janela
    cadastro.resizable(False, False)  # Não pode mudar de tamanho

    # Faz a janela aparecer no meio da tela
    x = cadastro.winfo_screenwidth() // 2 - 300
    y = cadastro.winfo_screenheight() // 2 - 350
    cadastro.geometry(f"+{x}+{y}")
    cadastro.configure(bg=cor_fundo)  # Deixa com fundo azul claro

    frame = tk.Frame(cadastro, bg=cor_fundo)
    frame.pack(padx=15, pady=15, fill='both', expand=True)

    # --- Parte onde escreve o nome e sala do aluno ---
    titulo_dados = tk.Label(frame, text="Dados Pessoais",
                            font=("Arial", 14, "bold"), bg=cor_fundo)
    titulo_dados.grid(row=0, column=0, columnspan=5, sticky='w', pady=(0, 10))

    # Campo da matrícula
    tk.Label(frame, text="Matrícula:", bg=cor_fundo).grid(
        row=1, column=0, sticky='w', padx=5, pady=5)
    entrada_matricula = tk.Entry(frame)
    entrada_matricula.grid(row=1, column=1, sticky='we', padx=5, pady=5)

    # Botão para buscar matrícula
    btn_buscar = tk.Button(frame, text="Buscar")
    btn_buscar.grid(row=1, column=2, padx=5, pady=5)
    estilizar_botao(btn_buscar)

    # Campo do nome
    tk.Label(frame, text="Nome:", bg=cor_fundo).grid(
        row=1, column=3, sticky='w', padx=5, pady=5)
    entrada_nome = tk.Entry(frame)
    entrada_nome.grid(row=1, column=4, sticky='we', padx=5, pady=5)

    # Campo da sala
    tk.Label(frame, text="Sala:", bg=cor_fundo).grid(
        row=2, column=0, sticky='w', padx=5, pady=5)
    entrada_sala = tk.Entry(frame)
    entrada_sala.grid(row=2, column=1, sticky='we', padx=5, pady=5)

    # Campo da turma
    tk.Label(frame, text="Turma:", bg=cor_fundo).grid(
        row=2, column=3, sticky='w', padx=5, pady=5)
    entrada_turma = tk.Entry(frame)
    entrada_turma.grid(row=2, column=4, sticky='we', padx=5, pady=5)

    # --- Parte onde escreve as notas do aluno ---
    titulo_materias = tk.Label(frame, text="Matérias", font=(
        "Arial", 14, "bold"), bg=cor_fundo)
    titulo_materias.grid(row=3, column=0, columnspan=5,
                         sticky='w', pady=(20, 10))

    entradas_notas = {}  # Guardar os campos das notas
    linhas = (len(disciplinas) + 1) // 2  # Distribui matérias em colunas

    for i, disc in enumerate(disciplinas):
        row = 4 + (i % linhas)
        col = (i // linhas) * 2
        tk.Label(frame, text=f"{disc}:", bg=cor_fundo).grid(
            row=row, column=col, sticky='w', padx=5, pady=3)
        entrada = tk.Entry(frame, width=10)
        entrada.grid(row=row, column=col + 1, sticky='we', padx=5, pady=3)
        entradas_notas[disc] = entrada

    # Função para buscar o aluno no banco de dados
    def buscar_aluno():
        matricula = entrada_matricula.get().strip()
        if not matricula:
            messagebox.showerror("Erro", "Digite uma matrícula para buscar.")
            return
        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nome, sala, turma FROM alunos WHERE matricula = ?", (matricula,))
        aluno = cursor.fetchone()
        if aluno:
            nome, sala, turma = aluno
            entrada_nome.delete(0, tk.END)
            entrada_nome.insert(0, nome)
            entrada_sala.delete(0, tk.END)
            entrada_sala.insert(0, str(sala))
            entrada_turma.delete(0, tk.END)
            entrada_turma.insert(0, turma)

            # Agora busca as notas
            cursor.execute(
                "SELECT disciplina, nota FROM notas WHERE matricula = ?", (matricula,))
            notas = cursor.fetchall()
            for disc in disciplinas:
                entradas_notas[disc].delete(0, tk.END)
            for disc, nota in notas:
                if disc in entradas_notas:
                    entradas_notas[disc].insert(0, str(nota))
        else:
            messagebox.showinfo("Aviso", "Matrícula não encontrada.")
            entrada_nome.delete(0, tk.END)
            entrada_sala.delete(0, tk.END)
            entrada_turma.delete(0, tk.END)
            for entrada in entradas_notas.values():
                entrada.delete(0, tk.END)
        conn.close()

    btn_buscar.config(command=buscar_aluno)  # Diz o que o botão buscar faz

    # Botões de baixo da tela: salvar, voltar e sair
    btn_frame = tk.Frame(cadastro, bg=cor_fundo)
    btn_frame.pack(pady=20)

    # O que acontece quando clica em salvar
    def salvar_cadastro():
        matricula = entrada_matricula.get().strip()
        nome = entrada_nome.get().strip()
        sala = entrada_sala.get().strip()
        turma = entrada_turma.get().strip()

        # Verifica se está tudo preenchido
        if not matricula or not nome or not sala or not turma:
            messagebox.showerror(
                "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            sala_num = int(sala)
        except ValueError:
            messagebox.showerror("Erro", "Sala deve ser um número.")
            return

        # Pega todas as notas
        notas_val = {}
        for disc, entrada in entradas_notas.items():
            val = entrada.get().strip()
            if val == "":
                messagebox.showerror(
                    "Erro", f"Preencha a nota da disciplina {disc}.")
                return
            try:
                nota = float(val)
                if nota < 0 or nota > 10:
                    raise ValueError
                notas_val[disc] = nota
            except ValueError:
                messagebox.showerror("Erro", f"Nota inválida para {disc}.")
                return

        # Salva no banco de dados
        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT matricula FROM alunos WHERE matricula = ?", (matricula,))
        existe = cursor.fetchone()

        try:
            if existe:
                cursor.execute("UPDATE alunos SET nome=?, sala=?, turma=? WHERE matricula=?",
                               (nome, sala_num, turma, matricula))
                for disc, nota in notas_val.items():
                    cursor.execute("UPDATE notas SET nota=? WHERE matricula=? AND disciplina=?",
                                   (nota, matricula, disc))
            else:
                cursor.execute("INSERT INTO alunos (matricula, nome, sala, turma) VALUES (?, ?, ?, ?)",
                               (matricula, nome, sala_num, turma))
                for disc, nota in notas_val.items():
                    cursor.execute("INSERT INTO notas (matricula, disciplina, nota) VALUES (?, ?, ?)",
                                   (matricula, disc, nota))

            conn.commit()
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            cadastro.destroy()  # Fecha a tela
            janela_menu.deiconify()  # Volta para o menu
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        finally:
            conn.close()

    # Parte que mostra as últimas matrículas cadastradas
    frame_matriculas = tk.Frame(frame, bg=cor_fundo)
    frame_matriculas.grid(row=row + 1, column=0,
                          columnspan=5, pady=(20, 10), sticky='w')

    titulo_ultimas = tk.Label(frame_matriculas, text="Últimas Matrículas Cadastradas:",
                              font=("Arial", 12, "bold"), bg=cor_fundo)
    titulo_ultimas.pack(anchor='w')

    lista_matriculas = tk.Listbox(
        frame_matriculas, height=3, width=20, bg="white", font=("Courier New", 10))
    lista_matriculas.pack(pady=(5, 0), anchor='w')

    label_proxima = tk.Label(frame_matriculas, text="", font=(
        "Arial", 11, "italic"), bg=cor_fundo, fg="blue")
    label_proxima.pack(pady=(5, 0), anchor='w')

    def carregar_matriculas_recentes():
        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT matricula FROM alunos ORDER BY matricula DESC LIMIT 3")
        resultados = cursor.fetchall()
        conn.close()

        lista_matriculas.delete(0, tk.END)
        ultimas = [r[0] for r in resultados]
        for mat in ultimas:
            lista_matriculas.insert(tk.END, mat)

        if ultimas:
            ultima = ultimas[0]
            prefixo = ''.join(filter(str.isalpha, ultima))
            numero = ''.join(filter(str.isdigit, ultima))
            try:
                novo_numero = int(numero) + 1
                proxima = f"{prefixo}{str(novo_numero).zfill(len(numero))}"
                label_proxima.config(
                    text=f"Próxima matrícula sugerida: {proxima}")
            except:
                label_proxima.config(
                    text="Não foi possível sugerir próxima matrícula.")
        else:
            label_proxima.config(
                text="Nenhuma matrícula encontrada. Sugestão: 9A001")

    carregar_matriculas_recentes()

    # Botões para salvar, voltar e sair
    btn_salvar = tk.Button(btn_frame, text="Salvar Aluno",
                           command=salvar_cadastro, width=15)
    btn_voltar = tk.Button(btn_frame, text="Voltar ao Menu", command=lambda: [
                           cadastro.destroy(), janela_menu.deiconify()], width=15)
    btn_sair = tk.Button(btn_frame, text="Sair",
                         command=janela_menu.destroy, width=15)

    btn_salvar.pack(side='left', padx=10)
    btn_voltar.pack(side='left', padx=10)
    btn_sair.pack(side='left', padx=10)

    for btn in (btn_salvar, btn_voltar, btn_sair):
        estilizar_botao(btn)

# ---------- JANELA DE CONSULTA DE NOTAS ----------


def criar_janela_consulta():
    consulta = tk.Toplevel()  # Abre uma nova janelinha
    consulta.title("Consultar e Atualizar Notas")
    consulta.geometry("800x500")  # Tamanho da tela
    consulta.resizable(False, False)  # Não pode mudar o tamanho

    # Centraliza a janela no meio da tela
    x = consulta.winfo_screenwidth() // 2 - 400
    y = consulta.winfo_screenheight() // 2 - 250
    consulta.geometry(f"+{x}+{y}")
    consulta.configure(bg=cor_fundo)

    janela_menu.withdraw()  # Esconde o menu principal enquanto essa janela está aberta

    consulta.after(100, lambda: messagebox.showinfo(
        "Aviso", "As matrículas ser iniciam em 9A001."))  # Mostra uma mensagem rápida

    # Quando o botão "Buscar Notas" for clicado
    def buscar_notas():
        matricula = entrada_matricula.get().strip()
        if not matricula:
            messagebox.showerror("Erro", "Digite uma matrícula para buscar.")
            return
        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nome, sala, turma FROM alunos WHERE matricula = ?", (matricula,))
        aluno = cursor.fetchone()
        if aluno:
            nome, sala, turma = aluno
            entrada_nome.delete(0, tk.END)
            entrada_nome.insert(0, nome)
            entrada_sala.delete(0, tk.END)
            entrada_sala.insert(0, str(sala))
            entrada_turma.delete(0, tk.END)
            entrada_turma.insert(0, turma)

            cursor.execute(
                "SELECT disciplina, nota FROM notas WHERE matricula = ?", (matricula,))
            notas = cursor.fetchall()
            for disc in disciplinas:
                entradas_notas[disc].delete(0, tk.END)
            for disc, nota in notas:
                if disc in entradas_notas:
                    entradas_notas[disc].insert(0, str(nota))
        else:
            messagebox.showinfo("Aviso", "Matrícula não encontrada.")
            entrada_nome.delete(0, tk.END)
            entrada_sala.delete(0, tk.END)
            entrada_turma.delete(0, tk.END)
            for entrada in entradas_notas.values():
                entrada.delete(0, tk.END)
        conn.close()

    # Função para atualizar as notas no banco
    def atualizar_notas():
        matricula = entrada_matricula.get().strip()
        if not matricula:
            messagebox.showerror(
                "Erro", "Digite uma matrícula para atualizar.")
            return

        notas_val = {}
        for disc, entrada in entradas_notas.items():
            val = entrada.get().strip()
            if val == "":
                messagebox.showerror(
                    "Erro", f"Preencha a nota da disciplina {disc}.")
                return
            try:
                nota = float(val)
                if nota < 0 or nota > 10:
                    raise ValueError
                notas_val[disc] = nota
            except ValueError:
                messagebox.showerror(
                    "Erro", f"Nota inválida para {disc}. Deve ser entre 0 e 10.")
                return

        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()
        for disc, nota in notas_val.items():
            cursor.execute("""
                UPDATE notas SET nota=? WHERE matricula=? AND disciplina=?
            """, (nota, matricula, disc))

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Notas atualizadas com sucesso!")

    # Parte da tela que mostra as informações
    frame = tk.Frame(consulta, bg=cor_fundo)
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    tk.Label(frame, text="Matrícula:", bg=cor_fundo).grid(
        row=0, column=0, sticky='w', padx=5, pady=5)
    entrada_matricula = tk.Entry(frame)
    entrada_matricula.grid(row=0, column=1, sticky='we', padx=5, pady=5)

    btn_buscar = tk.Button(frame, text="Buscar Notas",
                           command=buscar_notas, width=15)
    btn_buscar.grid(row=0, column=2, padx=5, pady=5)
    estilizar_botao(btn_buscar)

    # Dados pessoais do aluno
    titulo_dados = tk.Label(frame, text="Dados Pessoais",
                            font=("Arial", 14, "bold"), bg=cor_fundo)
    titulo_dados.grid(row=1, column=0, columnspan=6, sticky='w', pady=(15, 5))

    tk.Label(frame, text="Nome:", bg=cor_fundo).grid(
        row=2, column=0, sticky='w', padx=5, pady=5)
    entrada_nome = tk.Entry(frame)
    entrada_nome.grid(row=2, column=1, sticky='we', padx=5, pady=5)

    tk.Label(frame, text="Sala:", bg=cor_fundo).grid(
        row=2, column=2, sticky='w', padx=5, pady=5)
    entrada_sala = tk.Entry(frame)
    entrada_sala.grid(row=2, column=3, sticky='we', padx=5, pady=5)

    tk.Label(frame, text="Turma:", bg=cor_fundo).grid(
        row=2, column=4, sticky='w', padx=5, pady=5)
    entrada_turma = tk.Entry(frame)
    entrada_turma.grid(row=2, column=5, sticky='we', padx=5, pady=5)

    # Parte das matérias e notas
    titulo_materias = tk.Label(frame, text="Matérias", font=(
        "Arial", 14, "bold"), bg=cor_fundo)
    titulo_materias.grid(row=3, column=0, columnspan=6,
                         sticky='w', pady=(15, 10))

    entradas_notas = {}
    linhas = (len(disciplinas) + 1) // 2
    base_row = 4
    for i, disc in enumerate(disciplinas):
        row = base_row + (i % linhas)
        col = (i // linhas) * 2
        tk.Label(frame, text=f"{disc}:", bg=cor_fundo).grid(
            row=row, column=col, sticky='w', padx=5, pady=3)
        entrada = tk.Entry(frame, width=10)
        entrada.grid(row=row, column=col + 1, sticky='we', padx=5, pady=3)
        entradas_notas[disc] = entrada

    # Botões de ação
    btn_frame = tk.Frame(consulta, bg=cor_fundo)
    btn_frame.pack(pady=20)

    btn_atualizar = tk.Button(
        btn_frame, text="Atualizar Notas", command=atualizar_notas, width=15)
    btn_voltar = tk.Button(btn_frame, text="Voltar ao Menu", command=lambda: [
                           consulta.destroy(), janela_menu.deiconify()], width=15)
    btn_sair = tk.Button(btn_frame, text="Sair",
                         command=janela_menu.destroy, width=15)

    btn_atualizar.pack(side='left', padx=10)
    btn_voltar.pack(side='left', padx=10)
    btn_sair.pack(side='left', padx=10)

    for btn in (btn_atualizar, btn_voltar, btn_sair):
        estilizar_botao(btn)

# ---------- JANELA DO MENU PRINCIPAL ----------


janela_menu = tk.Tk()  # Cria a janela principal
janela_menu.title("Menu Principal")
janela_menu.geometry("400x300")  # Tamanho
janela_menu.configure(bg=cor_fundo)

# Centraliza a janela
x = janela_menu.winfo_screenwidth() // 2 - 200
y = janela_menu.winfo_screenheight() // 2 - 150
janela_menu.geometry(f"+{x}+{y}")

# Botão para cadastrar aluno
btn_cadastrar = tk.Button(janela_menu, text="Cadastrar Novo Aluno", command=lambda: [
    janela_menu.withdraw(), criar_janela_cadastro()], width=25)

# Botão para consultar notas
btn_consultar = tk.Button(
    janela_menu, text="Consultar e Atualizar Notas", command=criar_janela_consulta, width=25)

# Botão para sair
btn_sair = tk.Button(janela_menu, text="Sair",
                     command=janela_menu.destroy, width=25)

# Coloca os botões na tela
for btn in (btn_cadastrar, btn_consultar, btn_sair):
    btn.pack(pady=10)
    estilizar_botao(btn)

janela_menu.mainloop()  # Inicia o programa
