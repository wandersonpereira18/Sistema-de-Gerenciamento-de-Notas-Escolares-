import sqlite3  # Importa o módulo que trabalha com bancos de dados SQLite
import random   # Importa o módulo que ajuda a sortear valores aleatórios (como notas)

# Cria ou abre um arquivo de banco de dados chamado "Banco_alunos.db"
conn = sqlite3.connect("Banco_alunos.db")

# Cria um cursor, que é como uma ferramenta para executar comandos no banco
cursor = conn.cursor()

# Apaga a tabela de alunos se ela já existir (para começar do zero)
cursor.execute("DROP TABLE IF EXISTS alunos")

# Cria a nova tabela chamada "alunos" com as colunas:
# - matricula (código do aluno)
# - nome (nome do aluno)
# - disciplina (nome da matéria)
# - nota (nota que ele tirou)
# - sala (número da sala onde ele estuda)
# - turma (letra da turma)
cursor.execute("""
CREATE TABLE alunos (
    matricula TEXT,
    nome TEXT,
    disciplina TEXT,
    nota REAL,
    sala INTEGER,
    turma TEXT
)
""")

# Lista com 10 nomes de alunos de exemplo
nomes = [
    "Ana Beatriz", "Bruno Souza", "Carlos Eduardo", "Daniela Lima", "Eduardo Ramos",
    "Fernanda Alves", "Gabriel Rocha", "Helena Martins", "Igor Fernandes", "Julia Castro"
]

# Lista com as disciplinas (matérias) que os alunos têm na escola
disciplinas = [
    "Matemática", "Português", "História", "Biologia", "Física",
    "Química", "Geografia", "Educação Física", "Artes", "Inglês",
    "Educação Moral e Cívica"
]

# Lista com salas disponíveis (agora como números)
salas = [101, 102, 103]

# Lista com turmas possíveis (letras A e B)
turmas = ["A", "B"]

# Para cada aluno da lista de nomes...
for i, nome in enumerate(nomes):
    # Gera uma matrícula automática no formato 9A001, 9A002, etc.
    matricula = f"9A{i+1:03d}"

    # Sorteia uma sala para o aluno
    sala = random.choice(salas)

    # Sorteia uma turma (A ou B)
    turma = random.choice(turmas)

    # Para cada disciplina...
    for disciplina in disciplinas:
        # Gera uma nota aleatória entre 5.0 e 10.0
        nota = round(random.uniform(5.0, 10.0), 1)

        # Insere as informações no banco de dados
        cursor.execute("""
            INSERT INTO alunos (matricula, nome, disciplina, nota, sala, turma)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (matricula, nome, disciplina, nota, sala, turma))

# Salva todas as mudanças feitas no banco de dados
conn.commit()

# Fecha a conexão com o banco de dados
conn.close()

# Mostra uma mensagem no terminal dizendo que tudo deu certo
print("Banco de dados 'Banco_alunos.db' criado com sucesso com todas as matérias!")
