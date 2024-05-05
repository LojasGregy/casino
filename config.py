from flask import Flask, jsonify, request, session, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import DataRequired
from sqlalchemy.orm import relationship

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cassino.db'
app.config['SECRET_KEY'] = 'chave_secreta'  # Chave secreta para sessão
bcrypt = Bcrypt(app)

# Configuração do banco de dados
db = SQLAlchemy(app)

# Modelo de dados para usuários
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    balance = db.relationship('Balance', backref='user', uselist=False)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    bets = db.relationship('Bet', backref='user', lazy=True)
    horse_bets = db.relationship('HorseBet', backref='user', lazy=True)
    formula1_bets = db.relationship('Formula1Bet', backref='user', lazy=True)

# Modelo de dados para o saldo dos usuários
class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Modelo de dados para transações financeiras dos usuários
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=False)

# Modelo de dados para as apostas em corridas de cavalos
class HorseBet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    horse_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Modelo de dados para as apostas em Fórmula 1
class Formula1Bet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driver = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Formulário para validação de entrada ao fazer login
class LoginForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])

# Formulário para validação de entrada ao registrar um novo usuário
class RegisterForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])

# Formulário para validação de entrada ao fazer uma transação financeira
class TransactionForm(FlaskForm):
    amount = FloatField('Quantidade', validators=[DataRequired()])
    description = StringField('Descrição', validators=[DataRequired()])

# Formulário para validação de entrada ao fazer uma aposta em um jogo de futebol
class BetForm(FlaskForm):
    game = StringField('Jogo', validators=[DataRequired()])
    amount = FloatField('Quantidade', validators=[DataRequired()])

# Formulário para validação de entrada ao fazer uma aposta em uma corrida de cavalos
class HorseBetForm(FlaskForm):
    horse_name = StringField('Nome do cavalo', validators=[DataRequired()])
    amount = FloatField('Quantidade', validators=[DataRequired()])

# Formulário para validação de entrada ao fazer uma aposta em Fórmula 1
class Formula1BetForm(FlaskForm):
    driver = StringField('Piloto', validators=[DataRequired()])
    amount = FloatField('Quantidade', validators=[DataRequired()])

# Rota para fazer login
@app.route('/api/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return jsonify({'message': 'Login bem-sucedido!'})
    return jsonify({'error': 'Credenciais inválidas'}), 401

# Rota para fazer logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout bem-sucedido!'})

# Rota para registrar um novo usuário
@app.route('/api/register', methods=['POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        # Cria uma entrada de saldo para o novo usuário com saldo inicial de 0.0
        new_balance = Balance(user=new_user, amount=0.0)
        db.session.add(new_balance)
        db.session.commit()
        return jsonify({'message': 'Usuário registrado com sucesso!'}), 201
    return jsonify({'error': 'Erro de validação', 'messages': form.errors}), 400

# Rota protegida para a área de administração
@app.route('/admin')
def admin():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user.is_admin:
            # Se o usuário é um administrador, renderize a página de administração
            return render_template('admin.html')
    # Se o usuário não está autenticado ou não é um administrador, redirecione para a página de login
    return redirect(url_for('login'))

# Rota para realizar uma transação financeira
@app.route('/api/transaction', methods=['POST'])
def transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        if 'user_id' in session:
            user_id = session['user_id']
            amount = form.amount.data
            description = form.description.data
            user = User.query.get(user_id)
            if user:
                # Atualiza o saldo do usuário
                user.balance.amount += amount
                # Registra a transação
                transaction = Transaction(user_id=user_id, amount=amount, description=description)
                db.session.add(transaction)
                db.session.commit()
                return jsonify({'message': 'Transação concluída com sucesso!'}), 201
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return jsonify({'error': 'Erro de validação', 'messages': form.errors}), 400

# Rota para calcular o saldo e o total de prêmios ganhos pelo usuário
@app.route('/api/user-info')
def user_info():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
        if user:
            balance = user.balance.amount
            total_prizes = sum(transaction.amount for transaction in user.transactions if transaction.amount > 0)
            return jsonify({'username': user.username, 'balance': balance, 'total_prizes': total_prizes})
        else:
            return jsonify({'error': 'Usuário não encontrado'}), 404
    else:
        return jsonify({'error': 'Usuário não autenticado'}), 401

# Rota para realizar uma aposta em um jogo de futebol
@app.route('/api/bet', methods=['POST'])
def bet():
    form = BetForm()
    if form.validate_on_submit():
        if 'user_id' in session:
            user_id = session['user_id']
            amount = form.amount.data
            game = form.game.data
            user = User.query.get(user_id)
            if user:
                if user.balance.amount >= amount:
                    # Deduz o valor da aposta do saldo do usuário
                    user.balance.amount -= amount
                    # Registra a aposta
                    bet = Bet(user_id=user_id, game=game, amount=amount)
                    db.session.add(bet)
                    db.session.commit()
                    return jsonify({'message': 'Aposta realizada com sucesso!'}), 201
                else:
                    return jsonify({'error': 'Saldo insuficiente'}), 400
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return jsonify({'error': 'Erro de validação', 'messages': form.errors}), 400

# Rota para realizar uma aposta em uma corrida de cavalos
@app.route('/api/horse-bet', methods=['POST'])
def horse_bet():
    form = HorseBetForm()
    if form.validate_on_submit():
        if 'user_id' in session:
            user_id = session['user_id']
            amount = form.amount.data
            horse_name = form.horse_name.data
            user = User.query.get(user_id)
            if user:
                if user.balance.amount >= amount:
                    # Deduz o valor da aposta do saldo do usuário
                    user.balance.amount -= amount
                    # Registra a aposta em corrida de cavalos
                    horse_bet = HorseBet(user_id=user_id, horse_name=horse_name, amount=amount)
                    db.session.add(horse_bet)
                    db.session.commit()
                    return jsonify({'message': 'Aposta em corrida de cavalos realizada com sucesso!'}), 201
                else:
                    return jsonify({'error': 'Saldo insuficiente'}), 400
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return jsonify({'error': 'Erro de validação', 'messages': form.errors}), 400

# Rota para realizar uma aposta em Fórmula 1
@app.route('/api/formula1-bet', methods=['POST'])
def formula1_bet():
    form = Formula1BetForm()
    if form.validate_on_submit():
        if 'user_id' in session:
            user_id = session['user_id']
            amount = form.amount.data
            driver = form.driver.data
            user = User.query.get(user_id)
            if user:
                if user.balance.amount >= amount:
                    # Deduz o valor da aposta do saldo do usuário
                    user.balance.amount -= amount
                    # Registra a aposta em Fórmula 1
                    formula1_bet = Formula1Bet(user_id=user_id, driver=driver, amount=amount)
                    db.session.add(formula1_bet)
                    db.session.commit()
                    return jsonify({'message': 'Aposta em Fórmula 1 realizada com sucesso!'}), 201
                else:
                    return jsonify({'error': 'Saldo insuficiente'}), 400
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return jsonify({'error': 'Erro de validação', 'messages': form.errors}), 400

# Rota para realizar uma aposta
@app.route('/api/bet/<string:bet_type>', methods=['POST'])
def bet(bet_type):
    if bet_type == 'horse':
        form = HorseBetForm()
        model = HorseBet
    elif bet_type == 'formula1':
        form = Formula1BetForm()
        model = Formula1Bet
    else:
        return jsonify({'error': 'Tipo de aposta inválido'}), 400

    if form.validate_on_submit():
        if 'user_id' in session:
            user_id = session['user_id']
            amount = form.amount.data
            choice = form.horse_name.data if bet_type == 'horse' else form.driver.data
            user = User.query.get(user_id)
            if user:
                if user.balance.amount >= amount:
                    # Deduz o valor da aposta do saldo do usuário
                    user.balance.amount -= amount
                    # Registra a aposta
                    bet = model(user_id=user_id, choice=choice, amount=amount)
                    db.session.add(bet)
                    db.session.commit()
                    return jsonify({'message': f'Aposta em {bet_type} realizada com sucesso!'}), 201
                else:
                    return jsonify({'error': 'Saldo insuficiente'}), 400
            else:
                return jsonify({'error': 'Usuário não encontrado'}), 404
        else:
            return jsonify({'error': 'Usuário não autenticado'}), 401
    return jsonify({'error': 'Erro de validação', 'messages': form.errors}), 400

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
