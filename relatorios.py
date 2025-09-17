from db import conectar
from datetime import datetime, date
import csv
import os

# Função para limpar a tela
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

# Função para exibir o menu de relatórios
def menu_relatorios():
    while True:
        print("\n=== RELATÓRIOS DE REEMBOLSO ===")
        print("\n1 - Relatório mensal")
        print("2 - Relatório anual")
        print("3 - Relatório por funcionário")
        print("0 - Voltar\n")

        opcao = input(">> Escolha uma opção: ")

        if opcao == "1":
            relatorio_mensal()
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "2":
            relatorio_anual()
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "3":
            relatorio_funcionario()
            input("\nPressione Enter para continuar...")
            limpar_tela()
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida.")
            input("\nPressione Enter para continuar...")
            limpar_tela()

# Função para gerar relatório mensal
# Função gerada automaticamente pelo copilot e adaptada para incluir a formatação do relatório e integração com a função de exportação CSV
def relatorio_mensal():
    conn = conectar()
    cursor = conn.cursor()

    mes = input(">> Digite o mês (MM): ")
    ano = input(">> Digite o ano (AAAA): ")

    try:
        cursor.execute("""
            SELECT r.data_registro, f.nome, r.data_despesa, r.categoria, r.valor, r.status
            FROM reembolsos r
            JOIN funcionarios f ON r.funcionario_id = f.id
            WHERE EXTRACT(MONTH FROM r.data_registro) = %s 
              AND EXTRACT(YEAR FROM r.data_registro) = %s
            ORDER BY r.data_registro ASC;
        """, (mes, ano))
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\nNenhum reembolso encontrado para o período informado.")
            return

        # Impressão do relatório
        print(f"\n=== RELATÓRIO MENSAL DE REEMBOLSOS - {mes}/{ano} ===\n")
        print("Data de Registro | Funcionário | Data da Despesa | Categoria | Valor | Status")
        for p in pedidos:
            print(f"{p[0].strftime('%d/%m/%Y %H:%M:%S')} | {p[1]} | {p[2].strftime('%d/%m/%Y')} | {p[3]} | R$ {p[4]:.2f} | {p[5]}")

        # Estatísticas
        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(valor),0) 
            FROM reembolsos
            WHERE EXTRACT(MONTH FROM data_registro) = %s 
              AND EXTRACT(YEAR FROM data_registro) = %s;
        """, (mes, ano))
        total_pedidos, total_valor = cursor.fetchone()

        cursor.execute("""
            SELECT status, COUNT(*), COALESCE(SUM(valor),0)
            FROM reembolsos
            WHERE EXTRACT(MONTH FROM data_registro) = %s 
              AND EXTRACT(YEAR FROM data_registro) = %s
            GROUP BY status;
        """, (mes, ano))
        resumo_status = cursor.fetchall()

        print("\n=== RESUMO DO PERÍODO ===")
        print(f"Total de pedidos: {total_pedidos}")
        print(f"Valor total: R$ {total_valor:.2f}")
        for status, qtd, valor in resumo_status:
            print(f"Total {status}: {qtd} pedidos | R$ {valor:.2f}")

        # Exportação CSV
        resposta = input("\n>> Deseja exportar este relatório para CSV? (s/n): ").strip().lower()
        if resposta != "n":
            nome_arquivo = f"relatorio_mensal_{ano}_{mes}.csv"
            exportar_csv(
                nome_arquivo,
                ["Data Registro", "Funcionário", "Data Despesa", "Categoria", "Valor", "Status"],
                pedidos,
                (total_pedidos, total_valor),
                resumo_status
            )

    except Exception as e:
        print("\nErro ao gerar relatório mensal:", e)
    finally:
        cursor.close()
        conn.close()

# Função para gerar relatório anual
# Adaptada a partir da função relatorio_mensal
def relatorio_anual():
    conn = conectar()
    cursor = conn.cursor()

    ano = input(">> Digite o ano (AAAA): ")

    try:
        cursor.execute("""
            SELECT r.data_registro, f.nome, r.data_despesa, r.categoria, r.valor, r.status
            FROM reembolsos r
            JOIN funcionarios f ON r.funcionario_id = f.id
            WHERE EXTRACT(YEAR FROM r.data_registro) = %s
            ORDER BY r.data_registro ASC;
        """, (ano,))
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\nNenhum reembolso encontrado para o período informado.")
            return

        print(f"\n=== RELATÓRIO ANUAL DE REEMBOLSOS - {ano} ===\n")
        print("Data de Registro | Funcionário | Data da Despesa | Categoria | Valor | Status")
        for p in pedidos:
            print(f"{p[0].strftime('%d/%m/%Y %H:%M:%S')} | {p[1]} | {p[2].strftime('%d/%m/%Y')} | {p[3]} | R$ {p[4]:.2f} | {p[5]}")

        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(valor),0)
            FROM reembolsos
            WHERE EXTRACT(YEAR FROM data_registro) = %s;
        """, (ano,))
        total_pedidos, total_valor = cursor.fetchone()

        cursor.execute("""
            SELECT status, COUNT(*), COALESCE(SUM(valor),0)
            FROM reembolsos
            WHERE EXTRACT(YEAR FROM data_registro) = %s
            GROUP BY status;
        """, (ano,))
        resumo_status = cursor.fetchall()

        print("\n=== RESUMO DO PERÍODO ===")
        print(f"Total de pedidos: {total_pedidos}")
        print(f"Valor total: R$ {total_valor:.2f}")
        for status, qtd, valor in resumo_status:
            print(f"Total {status}: {qtd} pedidos | R$ {valor:.2f}")

        resposta = input("\n>> Deseja exportar este relatório para CSV? (s/n): ").strip().lower()
        if resposta != "n":
            nome_arquivo = f"relatorio_anual_{ano}.csv"
            exportar_csv(
                nome_arquivo,
                ["Data Registro", "Funcionário", "Data Despesa", "Categoria", "Valor", "Status"],
                pedidos,
                (total_pedidos, total_valor),
                resumo_status
            )

    except Exception as e:
        print("\nErro ao gerar relatório anual:", e)
    finally:
        cursor.close()
        conn.close()

# Função para gerar relatório por funcionário
# Função gerada pelo copilot em chat e adaptada
def relatorio_funcionario():
    conn = conectar()
    cursor = conn.cursor()

    email = input(">> Digite o email do funcionário: ").strip()

    try:
        cursor.execute("SELECT id, nome FROM funcionarios WHERE email = %s", (email,))
        funcionario = cursor.fetchone()
        if not funcionario:
            print("\nFuncionário não encontrado.")
            return

        funcionario_id, nome = funcionario

        cursor.execute("""
            SELECT r.data_registro, r.data_despesa, r.categoria, r.valor, r.status
            FROM reembolsos r
            WHERE r.funcionario_id = %s
            ORDER BY r.data_registro ASC
        """, (funcionario_id,))
        pedidos = cursor.fetchall()
        if not pedidos:
            print("\nNão há pedidos para este funcionário.")
            return

        print(f"\n=== RELATÓRIO DE REEMBOLSOS - {nome} ({email}) ===\n")
        print("Data Registro | Data Despesa | Categoria | Valor | Status")
        for p in pedidos:
            print(f"{p[0].strftime('%d/%m/%Y %H:%M:%S')} | {p[1].strftime('%d/%m/%Y')} | {p[2]} | R$ {p[3]:.2f} | {p[4]}")

        cursor.execute("""
            SELECT COUNT(*), COALESCE(SUM(valor),0)
            FROM reembolsos
            WHERE funcionario_id = %s
        """, (funcionario_id,))
        total_pedidos, total_valor = cursor.fetchone()

        cursor.execute("""
            SELECT status, COUNT(*), COALESCE(SUM(valor),0)
            FROM reembolsos
            WHERE funcionario_id = %s
            GROUP BY status;
        """, (funcionario_id,))
        resumo_status = cursor.fetchall()

        print("\n=== RESUMO DO FUNCIONÁRIO ===")
        print(f"Total de pedidos: {total_pedidos}")
        print(f"Valor total: R$ {total_valor:.2f}")
        for status, qtd, valor in resumo_status:
            print(f"Total {status}: {qtd} pedidos | R$ {valor:.2f}")

        resposta = input("\n>> Deseja exportar este relatório para CSV? (s/n): ").strip().lower()
        if resposta != "n":
            nome_arquivo = f"relatorio_funcionario_{nome.replace(' ', '_')}.csv"
            exportar_csv(
                nome_arquivo,
                ["Data Registro", "Data Despesa", "Categoria", "Valor", "Status"],
                pedidos,
                (total_pedidos, total_valor),
                resumo_status
            )

    except Exception as e:
        print("\nErro ao gerar relatório do funcionário:", e)
    finally:
        cursor.close()
        conn.close()

# Função para exportar relatórios em CSV (adaptados às funções acima))
# Função gerada pelo chatgpt
def exportar_csv(nome_arquivo, cabecalho, pedidos, resumo_totais, resumo_status=None):
    with open(nome_arquivo, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile, delimiter=";")

        # Cabeçalho
        writer.writerow(cabecalho)

        # Linhas de pedidos
        for p in pedidos:
            linha = []
            for valor in p:
                if isinstance(valor, datetime):
                    linha.append(valor.strftime('%d/%m/%Y %H:%M:%S'))
                elif isinstance(valor, date):
                    linha.append(valor.strftime('%d/%m/%Y'))
                elif isinstance(valor, float):
                    linha.append(f"{valor:.2f}")
                else:
                    linha.append(valor)
            writer.writerow(linha)

        # Resumo formatado
        writer.writerow([])
        writer.writerow(["Resumo do Período"])
        writer.writerow(["Indicador", "Quantidade", "Valor Total (R$)"])
        writer.writerow(["Total de pedidos", resumo_totais[0], f"{resumo_totais[1]:.2f}"])

        if resumo_status:
            for status, qtd, valor in resumo_status:
                writer.writerow([status, qtd, f"{valor:.2f}"])

    print(f"\nRelatório exportado para {nome_arquivo}")