from db import conectar

# Função para cadastrar um novo funcionário
# Função gerada pelo copilot em chat e adaptada
def cadastrar_funcionario(nome, setor, email, senha):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO funcionarios (nome, setor, email, senha)
            VALUES (%s, %s, %s, %s)
        """, (nome, setor, email, senha))
        conn.commit()
        print("\nUsuário cadastrado com sucesso!")
    except Exception as e:
        print("\nErro ao cadastrar funcionário: ", e)
    finally:
        cursor.close()
        conn.close()

# Função para login de funcionário
# Função gerada pelo copilot em chat e adaptada
def login_funcionario(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome FROM funcionarios 
        WHERE email = %s AND senha = %s
    """, (email, senha))
    funcionario = cursor.fetchone()
    conn.close()
    return funcionario

# Função para login do administrador
# Função gerada pelo copilot em chat e adaptada
def login_admin(email, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM administrador 
        WHERE email = %s AND senha = %s
    """, (email, senha))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return admin
