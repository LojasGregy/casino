from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from functools import wraps

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
app.config['SECRET_KEY'] = 'chave_secreta'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

# Modelo de dados para usuários
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    balance = db.Column(db.Float, default=0)
    bets = db.relationship('Bet', backref='user', lazy=True)

# Modelo de dados para apostas dos usuários
class Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Middleware para autenticar usuários
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Rota para autenticação de usuários
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login bem-sucedido'}), 200
    else:
        return jsonify({'error': 'Credenciais inválidas'}), 401

# Rota para logout de usuários
@app.route('/api/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout bem-sucedido'}), 200

# Rota para obter informações sobre a galeria de jogos
@app.route('/api/games')
@login_required
def get_games_info():
    games = {
        'game1': {'name': 'Jogo 1', 'balance': 0, 'total_bets': 0},
        'game2': {'name': 'Jogo 2', 'balance': 0, 'total_bets': 0},
        'game3': {'name': 'Jogo 3', 'balance': 0, 'total_bets': 0}
    }

    # Atualiza os saldos e total de apostas para cada jogo
    user_id = session['user_id']
    user = User.query.get(user_id)
    for bet in user.bets:
        games[bet.game_id]['balance'] += user.balance
        games[bet.game_id]['total_bets'] += bet.amount

    return jsonify(games)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
