import random

class User:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        else:
            print("Saldo insuficiente.")
            return False

class Game:
    def __init__(self, name):
        self.name = name

    def play(self, user, bet):
        pass

class SlotMachine(Game):
    def __init__(self):
        super().__init__("Slot Machine")

    def play(self, user, bet):
        if bet <= user.balance:
            symbols = ["Cherry", "Bell", "Bar", "Seven"]
            result = [random.choice(symbols) for _ in range(3)]
            print("Resultado:", result)
            if result.count("Cherry") == 3:
                winnings = bet * 10
            elif result.count("Cherry") == 2:
                winnings = bet * 5
            elif result.count("Bell") == 3:
                winnings = bet * 15
            elif result.count("Bar") == 3:
                winnings = bet * 20
            elif result.count("Seven") == 3:
                winnings = bet * 100
            else:
                winnings = 0
            user.balance += winnings - bet
            print("Ganhos:", winnings)
            print("Saldo:", user.balance)
        else:
            print("Aposta maior que o saldo.")

# Exemplo de uso:
user1 = User("joao123", "senha123", 100)
slot_machine = SlotMachine()

print("Usuário:", user1.username)
print("Saldo:", user1.balance)

bet_amount = 20
print("\nJogando Slot Machine com aposta de", bet_amount)
slot_machine.play(user1, bet_amount)

print("\nSaldo final:", user1.balance)
