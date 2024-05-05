# Importando bibliotecas necessárias
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Carregar os dados dos jogadores
dados_jogadores = pd.read_csv('dados_jogadores.csv')

# Engenharia de recursos: criar recursos relevantes para detecção de fraudes
dados_jogadores['quantidade_de_contas'] = dados_jogadores.groupby('id_jogador')['id_jogador'].transform('count')

# Selecionar recursos relevantes e transformar em matriz
X = dados_jogadores[['quantidade_de_contas', 'total_de_apostas']].values

# Dividir os dados em conjunto de treinamento e teste
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

# Treinar o modelo de detecção de anomalias (Isolation Forest)
modelo = IsolationForest(contamination=0.01)  # 1% de anomalias esperadas
modelo.fit(X_train)

# Fazer previsões no conjunto de teste
predicoes = modelo.predict(X_test)

# Avaliar o desempenho do modelo
print(classification_report(predicoes, y_test))
