import os
import getpass

# Função para autenticar o administrador
def authenticate_admin():
    admin_username = input("Admin Username: ")
    admin_password = getpass.getpass("Admin Password: ")
    # Lógica de autenticação do administrador aqui
    if admin_username == 'admin' and admin_password == 'admin123':
        return True
    else:
        return False

# Função para aumentar a dificuldade do jogo
def increase_difficulty():
    if authenticate_admin():
        # Lógica para aumentar a dificuldade aqui
        print("Dificuldade aumentada com sucesso!")
    else:
        print("Apenas o administrador pode aumentar a dificuldade.")

# Função para diminuir a dificuldade do jogo
def decrease_difficulty():
    if authenticate_admin():
        # Lógica para diminuir a dificuldade aqui
        print("Dificuldade diminuída com sucesso!")
    else:
        print("Apenas o administrador pode diminuir a dificuldade.")

# Função principal
def main():
    while True:
        print("1. Aumentar dificuldade do jogo (Apenas admin)")
        print("2. Diminuir dificuldade do jogo (Apenas admin)")
        print("3. Sair")
        choice = input("Escolha uma opção: ")
        if choice == '1':
            increase_difficulty()
        elif choice == '2':
            decrease_difficulty()
        elif choice == '3':
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()qqqqq
