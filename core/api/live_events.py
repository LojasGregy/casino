from flask import Flask, jsonify, request

# Configuração do Flask
app = Flask(__name__)

# Dados de exemplo para saldo e apostas dos usuários
user_data = {
    1: {'username': 'user1', 'balance': 100, 'bets': {'live_event_1': 20, 'live_event_2': 30}},
    2: {'username': 'user2', 'balance': 150, 'bets': {'live_event_1': 10}}
}

# Dados de exemplo para resultados dos eventos ao vivo
event_results = {
    'live_event_1': {'winner': 'Liverpool', 'odds': 2.0},
    'live_event_2': {'winner': 'Hamilton', 'odds': 1.5}
}

# Rota para obter saldo e valor das apostas por usuário em um evento ao vivo
@app.route('/api/live-event/<string:event_id>/user-info/<int:user_id>')
def get_user_info(event_id, user_id):
    user_info = user_data.get(user_id)
    if user_info:
        balance = user_info['balance']
        bets = user_info['bets'].get(event_id, 0)
        return jsonify({'username': user_info['username'], 'balance': balance, 'total_bet': bets})
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)
