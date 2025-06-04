import tkinter as tk
from tkinter import messagebox
import sqlite3

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

cor_fundo = "#f0f4ff"


def on_enter(e):
    e.widget['background'] = '#a0a0ff'


def on_leave(e):
    e.widget['background'] = 'SystemButtonFace'


def estilizar_botao(btn):
    btn.config(
        relief="raised",
        bd=3,
        bg='SystemButtonFace',
        highlightthickness=1,
        highlightbackground='#999',
        font=("Arial", 10, "bold"),
        padx=10, pady=5,
        borderwidth=2
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Criar banco se não existir


def criar_banco():
    conn = sqlite3.connect("Banco_alunos.db")
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS alunos(
        matricula TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        sala INTEGER NOT NULL,
        turma TEXT NOT NULL
    )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS notas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula TEXT NOT NULL,
        disciplina TEXT NOT NULL,
        nota REAL NOT NULL,
        FOREIGN KEY(matricula) REFERENCES alunos(matricula)
    )
    ''')
    conn.commit()
    conn.close()

# Janela principal


def criar_menu_principal():
    global janela_menu
    janela_menu = tk.Tk()
    janela_menu.title("Sistema Escolar")
    janela_menu.geometry("500x300")
    janela_menu.configure(bg=cor_fundo)
    janela_menu.resizable(False, False)

    rodape_texto = """Wanderson pereira do nascimento RGM: 39088863
Renato Miranda de Souza Araujo Alves RGM: 38989611
Ryan Gabriel Gomes Vieira RGM: 39261913
Victor Silva Amador RGM: 38136104"""

    btn_cadastrar = tk.Button(
        janela_menu, text="Cadastrar Aluno", width=20, command=criar_janela_cadastro)
    btn_consultar = tk.Button(
        janela_menu, text="Consultar/Atualizar Notas", width=20, command=criar_janela_consulta)
    btn_sair = tk.Button(janela_menu, text="Sair",
                         width=20, command=janela_menu.destroy)

    for btn in (btn_cadastrar, btn_consultar, btn_sair):
        estilizar_botao(btn)

    btn_cadastrar.pack(pady=15)
    btn_consultar.pack(pady=15)
    btn_sair.pack(pady=15)

    label_rodape = tk.Label(janela_menu, text=rodape_texto, font=(
        "Arial", 10), justify="center", bg=cor_fundo)
    label_rodape.pack(side="bottom", fill="x", pady=5, padx=10, anchor="w")

    janela_menu.mainloop()

# Tela de cadastro


def criar_janela_cadastro():
    cadastro = tk.Toplevel()
    cadastro.title("Cadastro de Novo Aluno")
    cadastro.geometry("650x720")
    cadastro.resizable(False, False)
    cadastro.configure(bg=cor_fundo)

    frame = tk.Frame(cadastro, bg=cor_fundo)
    frame.pack(padx=15, pady=15, fill='both', expand=True)

    # Dados pessoais
    tk.Label(frame, text="Dados Pessoais", font=("Arial", 14, "bold"), bg=cor_fundo).grid(
        row=0, column=0, columnspan=5, sticky='w', pady=(0, 10))

    tk.Label(frame, text="Matrícula:", bg=cor_fundo).grid(
        row=1, column=0, sticky='w', padx=5, pady=5)
    entrada_matricula = tk.Entry(frame)
    entrada_matricula.grid(row=1, column=1, sticky='we', padx=5, pady=5)

    btn_buscar = tk.Button(frame, text="Buscar")
    btn_buscar.grid(row=1, column=2, padx=5, pady=5)
    estilizar_botao(btn_buscar)

    tk.Label(frame, text="Nome:", bg=cor_fundo).grid(
        row=1, column=3, sticky='w', padx=5, pady=5)
    entrada_nome = tk.Entry(frame)
    entrada_nome.grid(row=1, column=4, sticky='we', padx=5, pady=5)

    tk.Label(frame, text="Sala:", bg=cor_fundo).grid(
        row=2, column=0, sticky='w', padx=5, pady=5)
    entrada_sala = tk.Entry(frame)
    entrada_sala.grid(row=2, column=1, sticky='we', padx=5, pady=5)

    tk.Label(frame, text="Turma:", bg=cor_fundo).grid(
        row=2, column=3, sticky='w', padx=5, pady=5)
    entrada_turma = tk.Entry(frame)
    entrada_turma.grid(row=2, column=4, sticky='we', padx=5, pady=5)

    # Matérias e notas
    tk.Label(frame, text="Matérias", font=("Arial", 14, "bold"), bg=cor_fundo).grid(
        row=3, column=0, columnspan=5, sticky='w', pady=(20, 10))

    entradas_notas = {}
    linhas = (len(disciplinas) + 1) // 2

    for i, disc in enumerate(disciplinas):
        row = 4 + (i % linhas)
        col = (i // linhas) * 2
        tk.Label(frame, text=f"{disc}:", bg=cor_fundo).grid(
            row=row, column=col, sticky='w', padx=5, pady=3)
        entrada = tk.Entry(frame, width=10)
        entrada.grid(row=row, column=col + 1, sticky='we', padx=5, pady=3)
        entradas_notas[disc] = entrada

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

    btn_buscar.config(command=buscar_aluno)

    def salvar_cadastro():
        matricula = entrada_matricula.get().strip()
        nome = entrada_nome.get().strip()
        sala = entrada_sala.get().strip()
        turma = entrada_turma.get().strip()

        if not matricula or not nome or not sala or not turma:
            messagebox.showerror(
                "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            sala_num = int(sala)
        except ValueError:
            messagebox.showerror("Erro", "Sala deve ser um número.")
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
                messagebox.showerror("Erro", f"Nota inválida para {disc}.")
                return

        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT matricula FROM alunos WHERE matricula = ?", (matricula,))
        existe = cursor.fetchone()

        try:
            if existe:
                cursor.execute("UPDATE alunos SET nome=?, sala=?, turma=? WHERE matricula=?",
                               (nome, sala_num, turma, matricula))
            else:
                cursor.execute("INSERT INTO alunos (matricula, nome, sala, turma) VALUES (?, ?, ?, ?)",
                               (matricula, nome, sala_num, turma))
            # Excluir notas antigas e inserir as novas
            cursor.execute(
                "DELETE FROM notas WHERE matricula = ?", (matricula,))
            for disc, nota in notas_val.items():
                cursor.execute("INSERT INTO notas (matricula, disciplina, nota) VALUES (?, ?, ?)",
                               (matricula, disc, nota))

            conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro salvo com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar cadastro: {e}")
        finally:
            conn.close()

    btn_salvar = tk.Button(cadastro, text="Salvar", command=salvar_cadastro)
    btn_voltar = tk.Button(
        cadastro, text="Voltar ao Menu", command=cadastro.destroy)

    estilizar_botao(btn_salvar)
    estilizar_botao(btn_voltar)

    btn_salvar.pack(side="left", padx=40, pady=20)
    btn_voltar.pack(side="right", padx=40, pady=20)

# Tela de consulta/atualização


def criar_janela_consulta():
    consulta = tk.Toplevel()
    consulta.title("Consultar e Atualizar Notas")
    consulta.geometry("650x720")
    consulta.resizable(False, False)
    consulta.configure(bg=cor_fundo)

    frame = tk.Frame(consulta, bg=cor_fundo)
    frame.pack(padx=15, pady=15, fill='both', expand=True)

    tk.Label(frame, text="Consulta de Notas", font=("Arial", 14, "bold"), bg=cor_fundo).grid(
        row=0, column=0, columnspan=4, sticky='w', pady=(0, 10))

    tk.Label(frame, text="Matrícula:", bg=cor_fundo).grid(
        row=1, column=0, sticky='w', padx=5, pady=5)
    entrada_matricula = tk.Entry(frame)
    entrada_matricula.grid(row=1, column=1, sticky='we', padx=5, pady=5)

    btn_buscar = tk.Button(frame, text="Buscar")
    btn_buscar.grid(row=1, column=2, padx=5, pady=5)
    estilizar_botao(btn_buscar)

    # Disciplinas e notas (lista)
    tk.Label(frame, text="Disciplinas", font=("Arial", 14, "bold"), bg=cor_fundo).grid(
        row=2, column=0, columnspan=4, sticky='w', pady=(20, 10))

    tk.Label(frame, text="Disciplina", bg=cor_fundo).grid(
        row=3, column=0, padx=5)
    tk.Label(frame, text="Nota", bg=cor_fundo).grid(row=3, column=1, padx=5)

    tree_notas = {}

    linhas = len(disciplinas)
    for i, disc in enumerate(disciplinas):
        tk.Label(frame, text=disc, bg=cor_fundo).grid(
            row=4+i, column=0, sticky='w', padx=5, pady=2)
        entrada = tk.Entry(frame, width=10)
        entrada.grid(row=4+i, column=1, padx=5, pady=2)
        entrada.config(state="readonly")
        tree_notas[disc] = entrada

    # Editar uma nota
    tk.Label(frame, text="Disciplina para editar:", bg=cor_fundo).grid(
        row=4+linhas, column=0, sticky='w', padx=5, pady=(20, 5))
    combo_disciplina = tk.StringVar()
    opcoes_disc = tk.OptionMenu(frame, combo_disciplina, *disciplinas)
    opcoes_disc.config(width=20)
    opcoes_disc.grid(row=4+linhas, column=1, sticky='we', padx=5, pady=(20, 5))

    tk.Label(frame, text="Nova Nota:", bg=cor_fundo).grid(
        row=5+linhas, column=0, sticky='w', padx=5, pady=5)
    entrada_nova_nota = tk.Entry(frame, width=10)
    entrada_nova_nota.grid(row=5+linhas, column=1, sticky='we', padx=5, pady=5)

    def buscar_notas():
        matricula = entrada_matricula.get().strip()
        if not matricula:
            messagebox.showerror("Erro", "Digite uma matrícula para buscar.")
            return
        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT matricula FROM alunos WHERE matricula = ?", (matricula,))
        aluno = cursor.fetchone()
        if not aluno:
            messagebox.showinfo("Aviso", "Matrícula não encontrada.")
            for ent in tree_notas.values():
                ent.config(state="normal")
                ent.delete(0, tk.END)
                ent.config(state="readonly")
            return

        cursor.execute(
            "SELECT disciplina, nota FROM notas WHERE matricula = ?", (matricula,))
        notas = cursor.fetchall()

        for disc in disciplinas:
            tree_notas[disc].config(state="normal")
            tree_notas[disc].delete(0, tk.END)
            tree_notas[disc].config(state="readonly")

        for disc, nota in notas:
            if disc in tree_notas:
                tree_notas[disc].config(state="normal")
                tree_notas[disc].delete(0, tk.END)
                tree_notas[disc].insert(0, str(nota))
                tree_notas[disc].config(state="readonly")

        conn.close()

    btn_buscar.config(command=buscar_notas)

    def atualizar_nota():
        matricula = entrada_matricula.get().strip()
        disc = combo_disciplina.get()
        nova_nota = entrada_nova_nota.get().strip()

        if not matricula or not disc or not nova_nota:
            messagebox.showerror(
                "Erro", "Preencha todos os campos para atualizar a nota.")
            return

        try:
            nota_val = float(nova_nota)
            if nota_val < 0 or nota_val > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Erro", "Digite uma nota válida entre 0 e 10.")
            return

        conn = sqlite3.connect("Banco_alunos.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT matricula FROM alunos WHERE matricula = ?", (matricula,))
        aluno = cursor.fetchone()
        if not aluno:
            messagebox.showerror("Erro", "Matrícula não encontrada.")
            conn.close()
            return

        cursor.execute(
            "SELECT id FROM notas WHERE matricula = ? AND disciplina = ?", (matricula, disc))
        nota_existente = cursor.fetchone()
        try:
            if nota_existente:
                cursor.execute(
                    "UPDATE notas SET nota = ? WHERE matricula = ? AND disciplina = ?", (nota_val, matricula, disc))
            else:
                cursor.execute(
                    "INSERT INTO notas (matricula, disciplina, nota) VALUES (?, ?, ?)", (matricula, disc, nota_val))
            conn.commit()
            messagebox.showinfo("Sucesso", "Nota atualizada com sucesso.")
            entrada_nova_nota.delete(0, tk.END)
            buscar_notas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar nota: {e}")
        finally:
            conn.close()

    btn_atualizar = tk.Button(
        frame, text="Atualizar Nota", command=atualizar_nota)
    btn_voltar = tk.Button(frame, text="Voltar ao Menu",
                           command=consulta.destroy)

    estilizar_botao(btn_atualizar)
    estilizar_botao(btn_voltar)

    btn_atualizar.grid(row=6+linhas, column=0, pady=20, padx=10)
    btn_voltar.grid(row=6+linhas, column=1, pady=20, padx=10)


# Executar sistema
if __name__ == "__main__":
    criar_banco()
    criar_menu_principal()
