import os
from db import conectar

# Função para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função para exibir o menu do funcionário
# Função gerada pelo copilot em chat e adaptada
def menu_funcionario(funcionario_id, nome):
    while True:
        print(F"\n\n#### Bem vindo(a), {nome} ####\n")
        print("1 - Registrar pedido de reembolso\n")
        print("2 - Listar meus pedidos\n")
        print("0 - Logout\n")

        opcao = input("\n>> Escolha uma opção: ")

        if opcao == "1":
            registrar_reembolso(funcionario_id)
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "2":
            listar_reembolsos(funcionario_id)
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "0":
            print("\nFazendo logout...")
            break
        else:
            print("\nOpção inválida!")
            input("\nPressione Enter para continuar...")
            limpar_tela()

# Função para o funcionário registrar um novo pedido de reembolso
# Função gerada pelo copilot em chat e adaptada
def registrar_reembolso(funcionario_id):
    conn = conectar()
    cursor = conn.cursor()

    print("\n=== NOVO REEMBOLSO ===\n\n")
    data = input("Data (YYYY-MM-DD): ")
    categoria = input("Categoria (Transporte/Alimentação/Hospedagem/Material/Outros): ")
    valor = input("Valor: ")
    comprovante = input("Caminho do comprovante (ex: /docs/comprovante.pdf): ")
    try:
        cursor.execute("""
            INSERT INTO reembolsos (funcionario_id, data_despesa, categoria, valor, comprovante)
            VALUES (%s, %s, %s, %s, %s)
        """, (funcionario_id, data, categoria, valor, comprovante))
        conn.commit()
        print("\nPedido de reembolso registrado com sucesso!")
    except Exception as e:
        print("\nErro ao registrar reembolso: ", e)
    finally:
        cursor.close()
        conn.close()

# Função para listar os pedidos de reembolso do funcionário
# Função gerada pelo copilot em chat e adaptada
def listar_reembolsos(funcionario_id):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT id, data_despesa, categoria, valor, status
            FROM reembolsos WHERE funcionario_id = %s
            ORDER BY data_despesa DESC
        """, (funcionario_id,))
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\nVocê ainda não possui nenhum pedido de reembolso.")

        else:
            print("\n=== MEUS PEDIDOS ===\n\n")
            for pedido in pedidos:
                print(f"ID: {pedido[0]} | Data: {pedido[1]} | Categoria: {pedido[2]} | Valor: {pedido[3]} | Status: {pedido[4]}\n")
        
            # Para alterar ou excluir apenas os pedidos sob análise:
            acao = input("\n>> Deseja alterar (A) ou excluir (E) algum pedido em análise? (digite A, E ou Enter para voltar): ").strip().upper()
            if [p for p in pedidos if p[4] == "em análise"]:
                if acao == "A":
                    id_alterar = input("\n>> Digite o ID do reembolso: ")
                    cursor.execute("""
                        SELECT id FROM reembolsos WHERE id = %s AND funcionario_id = %s AND status = 'em análise'
                    """, (id_alterar, funcionario_id))
                    if cursor.fetchone():
                        nova_data = input(">> Data (YYYY-MM-DD): ")
                        nova_categoria = input(">> Categoria (Transporte/Alimentação/Hospedagem/Material/Outros): ")
                        novo_valor = input(">> Valor: ")
                        novo_comprovante = input(">> Caminho do comprovante (ex: /docs/comprovante.pdf): ")
                        cursor.execute("""
                            UPDATE reembolsos
                            SET data_despesa = %s, categoria = %s, valor = %s, comprovante = %s
                            WHERE id = %s AND funcionario_id = %s AND status = 'em análise'
                        """, (nova_data, nova_categoria, novo_valor, novo_comprovante, id_alterar, funcionario_id))
                        conn.commit()
                        print("\nPedido alterado com sucesso!")
                    else:
                        print("\nID inválido ou o pedido não está em análise.")
                elif acao == "E":
                    id_excluir = input("\n>> Informe o ID do pedido que deseja excluir: ")
                    cursor.execute("""
                        SELECT id FROM reembolsos WHERE id = %s AND funcionario_id = %s AND status = 'em análise'
                    """, (id_excluir, funcionario_id))
                    if cursor.fetchone():
                        cursor.execute("""
                            DELETE FROM reembolsos
                            WHERE id = %s AND funcionario_id = %s AND status = 'em análise'
                        """, (id_excluir, funcionario_id))
                        conn.commit()
                        print("\nPedido excluído com sucesso!")
                    else:
                        print("\nID inválido ou pedido não está em análise.")
    except Exception as e:
        print("\nErro ao listar pedidos: ", e)
    finally:
        cursor.close()
        conn.close()
