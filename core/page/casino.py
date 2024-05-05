class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount
        print(f"Depósito de ${amount} realizado. Novo saldo: ${self.balance}")

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            print(f"Saque de ${amount} realizado. Novo saldo: ${self.balance}")
        else:
            print("Saldo insuficiente para o saque.")

class Casino:
    def __init__(self):
        self.users = {}

    def register(self, username, password):
        if username in self.users:
            print("Nome de usuário já existe. Por favor, escolha outro.")
        else:
            self.users[username] = User(username, password)
            print("Usuário registrado com sucesso.")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            print("Login bem-sucedido.")
            return self.users[username]
        else:
            print("Credenciais inválidas. Por favor, tente novamente.")
            return None

def main():
    casino = Casino()

    while True:
        print("\nBem-vindo ao Casino Online!")
        print("1. Registrar")
        print("2. Login")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == "1":
            username = input("Digite um nome de usuário: ")
            password = input("Digite uma senha: ")
            casino.register(username, password)
        elif choice == "2":
            username = input("Nome de usuário: ")
            password = input("Senha: ")
            user = casino.login(username, password)
            if user:
                while True:
                    print("\nMenu do Usuário:")
                    print("1. Depositar")
                    print("2. Sacar")
                    print("3. Sair")

                    user_choice = input("Escolha uma opção: ")

                    if user_choice == "1":
                        amount = float(input("Digite o valor do depósito: "))
                        user.deposit(amount)
                    elif user_choice == "2":
                        amount = float(input("Digite o valor do saque: "))
                        user.withdraw(amount)
                    elif user_choice == "3":
                        break
        elif choice == "3":
            print("Obrigado por jogar! Até mais.")
            break
        else:
            print("Opção inválida. Por favor, escolha novamente.")

if __name__ == "__main__":
    main()
