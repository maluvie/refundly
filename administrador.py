import os
from db import conectar
from relatorios import menu_relatorios

# Função para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função para exibir o menu do administrador
def menu_administrador():
    while True:
        print(F"\n\n#### Bem vindo(a), administrador! ####\n")
        print("1 - Pedidos sob análise\n")
        print("2 - Pedidos analisados\n")
        print("3 - Gerar relatório\n")
        print("0 - Logout\n")

        opcao = input("\n>> Escolha uma opção: ")

        if opcao == "1":
            pedidos_em_analise()
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "2":
            pedidos_analisados()
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "3":
            menu_relatorios()
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "0":
            print("\nFazendo logout...")
            break
        else:
            print("\nOpção inválida!")
            input("\nPressione Enter para continuar...")
            limpar_tela()

# Função para listar os pedidos em análise e permitir análise (aprovar, pagar, rejeitar)
# Função gerada pelo copilot em chat e adaptada
def pedidos_em_analise():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT f.nome, r.data_despesa, r.categoria, r.valor, r.comprovante, r.id 
            FROM reembolsos r
            JOIN funcionarios f ON r.funcionario_id = f.id
            WHERE r.status = 'em análise'
            ORDER BY r.data_despesa DESC
        """)
        pedidos = cursor.fetchall()
        if not pedidos:
            print("\nNão há pedidos em análise.")
        else:
            print("\n=== PEDIDOS SOB ANÁLISE ===\n\n")
            for pedido in pedidos:
                print(f"ID: {pedido[5]} | Funcionário: {pedido[0]} | Data da Despesa: {pedido[1]} | Categoria: {pedido[2]} | Valor: {pedido[3]} | Comprovante: {pedido[4]}")
        
            # Análise do pedido
            while True:
                id_pedido = input("\n>> Digite o ID do pedido para analisar (ou Enter para voltar): ").strip()
                if not id_pedido:
                    break
                cursor.execute("""
                    SELECT r.id, f.nome, r.data_despesa, r.categoria, r.valor, r.comprovante
                    FROM reembolsos r
                    JOIN funcionarios f ON r.funcionario_id = f.id
                    WHERE r.id = %s AND r.status = 'em análise'
                """, (id_pedido,))
                pedido = cursor.fetchone()
                if not pedido:
                    print("ID inválido ou pedido já analisado.")
                    continue
                print(f"\nPedido selecionado:\nID: {pedido[0]}\nFuncionário: {pedido[1]}\n Data da Despesa: {pedido[2]}\nCategoria: {pedido[3]}\nValor: {pedido[4]}\nComprovante: {pedido[5]}")
                print("\nEscolha o novo status para este pedido:")
                print("1 - Aprovado")
                print("2 - Pago")
                print("3 - Rejeitado")
                status_opcao = input(">> ")
                novo_status = None
                if status_opcao == "1":
                    novo_status = "aprovado"
                elif status_opcao == "2":
                    novo_status = "pago"
                elif status_opcao == "3":
                    novo_status = "rejeitado"
                else:
                    print("Opção inválida.")
                    continue
                cursor.execute("""
                    UPDATE reembolsos SET status = %s WHERE id = %s
                """, (novo_status, id_pedido))
                conn.commit()
                print(f"Status do pedido {id_pedido} alterado para '{novo_status}'.")
    except Exception as e:
        print("\nErro ao listar pedidos em análise:", e)
    finally:
        cursor.close()
        conn.close()

# Função para listar os pedidos já analisados
# Função gerada pelo copilot em chat e adaptada
def pedidos_analisados():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT f.nome, r.data_despesa, r.categoria, r.valor, r.comprovante, r.status
            FROM reembolsos r
            JOIN funcionarios f ON r.funcionario_id = f.id
            WHERE r.status IN ('aprovado', 'rejeitado', 'pago')
            ORDER BY r.data_despesa DESC
        """)
        pedidos = cursor.fetchall()
        if not pedidos:
            print("\nNão há pedidos analisados.")
        else:
            print("\n=== PEDIDOS ANALISADOS ===\n")
            for pedido in pedidos:
                print(f"Funcionário: {pedido[0]} | Data da despesa: {pedido[1]} | Categoria: {pedido[2]} | Valor: {pedido[3]} | Comprovante: {pedido[4]} | Status: {pedido[5]}")
    except Exception as e:
        print("\nErro ao listar pedidos analisados:", e)
    finally:
        cursor.close()
        conn.close()