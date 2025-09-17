import psycopg2
import time
import subprocess

# função para inicializar o container Docker do PostgreSQL
# função gerada com o auxílio do copilot e chatpgt
def iniciar_docker():
    try:
        subprocess.run(["docker", "start", "refund-db"], check=True)
        print("Banco de dados iniciado com sucesso!")
    except subprocess.CalledProcessError:
        print("Não foi possível iniciar o banco de dados, verifique se o Docker está rodando.")


# criar função conectar() para conectar ao banco de dados PostgreSQL "refunds" na porta 5432, usuário admin, senha 1234
# função gerada pelo copilot em comentário
def conectar():
    time.sleep(5)
    return psycopg2.connect(
        dbname="refunds",
        user="admin",
        password="1234",
        host="localhost",
        port="5432"
    )

# função para criar tabelas no banco de dados
# função gerada pelo copilot em comentário
def criar_tabelas():
    conn = conectar()
    cursor =conn.cursor()

    # criar tabela Funcionários com os atributos id (PK, auto-incremento), nome (NN, varchar), setor (varchar), email (NN, único, varchar), senha (NN, varchar)
    # gerado pelo copilot em comentário
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        setor VARCHAR(50),
        email VARCHAR(100) UNIQUE NOT NULL,
        senha VARCHAR(100) NOT NULL
    );
    """)

    # criar tabela Remmbolsos com os atributos id (PK, auto-incremento), funcionario_id (FK, NN, int), data (NN, date), categoria (NN, varchar), valor (NN, float), comprovante (varchar), status (varchar, default 'em análise')
    # gerado pelo copilot em comentário e adaptado com o uso de check para incluir as possibilidades de categoria e status
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reembolsos (
        id SERIAL PRIMARY KEY,
        funcionario_id INT NOT NULL REFERENCES funcionarios(id),
        data_despesa DATE NOT NULL,
        categoria VARCHAR(50) NOT NULL CHECK (categoria IN (
            'Transporte',
            'Alimentação',
            'Hospedagem',
            'Material',
            'Outros'
        )),
        valor NUMERIC(10,2) NOT NULL,
        comprovante TEXT,
        status VARCHAR(20) DEFAULT 'em análise' CHECK (status IN ('em análise', 'aprovado', 'rejeitado', 'pago')),
        data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

    # criar tabela Administrador com os atributos id (PK, auto-incremento), email (NN, único, varchar), senha (NN, varchar)
    # gerado pelo copilot em comentário
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administrador (
        id SERIAL PRIMARY KEY,
        email VARCHAR(100) UNIQUE NOT NULL,
        senha VARCHAR(100) NOT NULL
    );
    """)

    # inserir um administrador padrão se não existir nenhum
    # gerado pelo copilot em comentário
    cursor.execute("SELECT COUNT(*) FROM administrador;")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO administrador (email, senha)
            VALUES ('admin@empresa.com', 'admin123');
        """)

    conn.commit()
    conn.close()
    