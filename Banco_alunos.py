import sqlite3
import random

# Conectar (ou criar) o banco de dados
conn = sqlite3.connect("Banco_alunos.db")
cursor = conn.cursor()

# Criar a tabela
cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    matricula TEXT,
    nome TEXT,
    disciplina TEXT,
    nota REAL
)
""")

# Lista de nomes e disciplinas
nomes = [
    "Ana Beatriz", "Bruno Souza", "Carlos Eduardo", "Daniela Lima", "Eduardo Ramos",
    "Fernanda Alves", "Gabriel Rocha", "Helena Martins", "Igor Fernandes", "Julia Castro"
]

disciplinas = ["Matemática", "Português", "História", "Geografia", "Ciências", "Inglês"]

# Limpar registros anteriores (opcional)
cursor.execute("DELETE FROM alunos")

# Inserir dados simulados: cada aluno com todas as disciplinas
for i, nome in enumerate(nomes):
    matricula = f"9A{i+1:03d}"  # Ex: 9A001
    for disciplina in disciplinas:
        nota = round(random.uniform(5.0, 10.0), 1)  # Nota aleatória de 5.0 a 10.0
        cursor.execute("""
            INSERT INTO alunos (matricula, nome, disciplina, nota)
            VALUES (?, ?, ?, ?)
        """, (matricula, nome, disciplina, nota))

# Salvar e fechar
conn.commit()
conn.close()

print("Banco de dados 'Banco_alunos.db' criado com sucesso!")