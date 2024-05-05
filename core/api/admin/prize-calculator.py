from flask import Flask, jsonify, request

# Configuração do Flask
app = Flask(__name__)

# Dados de exemplo para apostas dos usuários
user_bets = {
    1: {'username': 'user1', 'bets': {'live_event_1': 20, 'live_event_2': 30}},
    2: {'username': 'user2', 'bets': {'live_event_1': 10}}
}

# Dados de exemplo para resultados dos eventos ao vivo
event_results = {
    'live_event_1': {'winner': 'Liverpool', 'odds': 2.0},
    'live_event_2': {'winner': 'Hamilton', 'odds': 1.5}
}

# Rota para calcular os prêmios e saldo total dos prêmios para o administrador
@app.route('/api/admin/prize-calculator')
def calculate_prizes():
    total_prizes = {}
    total_balance = 0

    for user_id, data in user_bets.items():
        for event_id, amount in data['bets'].items():
            if event_id in event_results:
                winner = event_results[event_id]['winner']
                odds = event_results[event_id]['odds']
                if winner == 'Liverpool':  # Exemplo de lógica de cálculo do prêmio (apenas para demonstração)
                    prize = amount * odds
                else:
                    prize = 0
                total_prizes[user_id] = total_prizes.get(user_id, 0) + prize

    total_balance = sum(total_prizes.values())

    return jsonify({'total_prizes': total_prizes, 'total_balance': total_balance})

if __name__ == '__main__':
    app.run(debug=True)
