import os
import getpass

# Função para carregar todos os plugins
def load_plugins():
    plugins = {}
    plugin_dir = 'plugins'
    for plugin_name in os.listdir(plugin_dir):
        if os.path.isdir(os.path.join(plugin_dir, plugin_name)):
            plugin_module = __import__('plugins.' + plugin_name, fromlist=[''])
            plugins[plugin_name] = plugin_module
    return plugins

# Função para autenticar o administrador
def authenticate_admin():
    username = input("Admin Username: ")
    password = getpass.getpass("Admin Password: ")
    # Lógica de autenticação do administrador aqui
    if username == 'admin' and password == 'admin123':
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
    plugins = load_plugins()
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
    main()
