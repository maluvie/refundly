import os
from db import criar_tabelas, iniciar_docker
from auth import cadastrar_funcionario, login_funcionario, login_admin
from funcionario import menu_funcionario
from administrador import menu_administrador

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def menu_principal():
    while True:
        print("\n\n#### REFUNDLY ####\n")
        print("1 - Funcionário: cadastrar\n")
        print("2 - Funcionário: login\n")
        print("3 - Administrador: login\n")
        print("0 - Sair\n")

        opcao = input(">> Escolha uma opção: ")

        if opcao == "1":
            print("\n\n=== CADASTRAR NOVO USUÁRIO ===\n")
            nome = input(">> Nome completo: ")
            setor = input("> Setor: ")
            email = input(">> Email: ")
            senha = input(">> Senha: ")
            cadastrar_funcionario(nome, setor, email, senha)
            input("\nPressione Enter para continuar...")
            limpar_tela()
        
        elif opcao == "2":
            print("\n\n=== LOGIN DO FUNCIONÁRIO ===\n")
            email = input(">> Email: ")
            senha = input(">> Senha: ")
            funcionario = login_funcionario(email, senha)
            if funcionario:
                funcionario_id, nome = funcionario
                menu_funcionario(funcionario_id, nome)
            else:
                print("\nEmail ou senha inválidos!")
            input("\nPressione Enter para continuar...")
            limpar_tela()

        elif opcao == "3":
            print("\n\n=== LOGIN DO ADMINISTRADOR ===\n")
            email = input(">> Email: ")
            senha = input(">> Senha: ")
            admin = login_admin(email, senha)
            if admin:
                menu_administrador()
            else:
                print("\nCredenciais inválidas!")
            input("\nPressione Enter para continuar...")
            limpar_tela()
        
        elif opcao == "0":
            print("\nEncerrando aplicação...")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")
            limpar_tela()

if __name__ == "__main__":
    print("\nIniciando aplicação...")
    iniciar_docker()
    criar_tabelas()
    menu_principal()