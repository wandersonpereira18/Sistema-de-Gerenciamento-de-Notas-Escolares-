import tkinter as tk
from tkinter import messagebox
import sqlite3

# Função para buscar as disciplinas do aluno por matrícula
def buscar_aluno():
    matricula = entrada_matricula.get().strip()
    conn = sqlite3.connect("Banco_alunos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM alunos WHERE matricula = ?", (matricula,))
    resultado_nome = cursor.fetchone()

    listbox_disciplinas.delete(0, tk.END)
    
    entrada_nome.config(state='normal')  # liberar edição temporária
    entrada_nome.delete(0, tk.END)
    entrada_disciplina.delete(0, tk.END)
    entrada_nota.delete(0, tk.END)

    if resultado_nome:
        entrada_nome.insert(0, resultado_nome[0])
        entrada_nome.config(state='readonly')  # voltar ao modo somente leitura

        cursor.execute("SELECT disciplina, nota FROM alunos WHERE matricula = ?", (matricula,))
        resultados = cursor.fetchall()

        for disciplina, nota in resultados:
            listbox_disciplinas.insert(tk.END, f"{disciplina} - Nota: {nota}")
    else:
        entrada_nome.config(state='readonly')  # garantir retorno ao estado anterior
        messagebox.showerror("Erro", "Matrícula não encontrada.")

    conn.close()

# Função para carregar a disciplina selecionada
def carregar_disciplina(event):
    selecao = listbox_disciplinas.curselection()
    if selecao:
        texto = listbox_disciplinas.get(selecao[0])
        disciplina, nota = texto.split(" - Nota: ")
        entrada_disciplina.delete(0, tk.END)
        entrada_nota.delete(0, tk.END)
        entrada_disciplina.insert(0, disciplina)
        entrada_nota.insert(0, nota)

# Função para salvar alterações da nota
def salvar_dados():
    matricula = entrada_matricula.get().strip()
    disciplina = entrada_disciplina.get().strip()
    nova_nota = entrada_nota.get().strip()

    try:
        nova_nota = float(nova_nota)
    except ValueError:
        messagebox.showerror("Erro", "Nota deve ser um número.")
        return

    conn = sqlite3.connect("Banco_alunos.db")  # Corrigido o nome do banco aqui também
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE alunos 
        SET nota = ? 
        WHERE matricula = ? AND disciplina = ?
    """, (nova_nota, matricula, disciplina))
    
    if cursor.rowcount > 0:
        conn.commit()
        messagebox.showinfo("Sucesso", "Nota atualizada com sucesso.")
        buscar_aluno()
    else:
        messagebox.showerror("Erro", "Não foi possível atualizar. Verifique os dados.")
    
    conn.close()

# Interface gráfica
janela = tk.Tk()
janela.title("Sistema de Notas Escolares")

tk.Label(janela, text="Matrícula:").grid(row=0, column=0, padx=10, pady=5)
entrada_matricula = tk.Entry(janela)
entrada_matricula.grid(row=0, column=1)
tk.Button(janela, text="Buscar", command=buscar_aluno).grid(row=0, column=2)

tk.Label(janela, text="Nome:").grid(row=1, column=0)
entrada_nome = tk.Entry(janela, state='readonly')  # fica readonly mas permite preenchimento programático
entrada_nome.grid(row=1, column=1, columnspan=2, sticky="we")

tk.Label(janela, text="Disciplinas e Notas:").grid(row=2, column=0, columnspan=3)
listbox_disciplinas = tk.Listbox(janela, width=50)
listbox_disciplinas.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
listbox_disciplinas.bind('<<ListboxSelect>>', carregar_disciplina)

tk.Label(janela, text="Disciplina Selecionada:").grid(row=4, column=0)
entrada_disciplina = tk.Entry(janela)
entrada_disciplina.grid(row=4, column=1, columnspan=2, sticky="we")

tk.Label(janela, text="Nova Nota:").grid(row=5, column=0)
entrada_nota = tk.Entry(janela)
entrada_nota.grid(row=5, column=1, columnspan=2, sticky="we")

tk.Button(janela, text="Salvar Alterações", command=salvar_dados).grid(row=6, column=0, columnspan=3, pady=10)

janela.mainloop()