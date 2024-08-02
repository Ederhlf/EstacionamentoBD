import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Configuração da conexão com o banco de dados
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'erdeline'
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'EstacionamentoDB'

# Cria a URL de conexão
DATABASE_URL = f'mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

# Cria o engine SQLAlchemy
engine = create_engine(DATABASE_URL)

def fetch_data(query):
    """Recupera dados do banco de dados e retorna um DataFrame do pandas."""
    return pd.read_sql(query, engine)

def get_data_from_db():
    """Conecta ao banco de dados e retorna um DataFrame com os dados necessários."""
    try:
        print("Conectado ao banco de dados")
        
        # Consultas SQL para recuperar dados
        queries = {
            'entrada_saida': "SELECT * FROM EntradaSaida",
            'cliente': "SELECT * FROM Cliente",
            'vaga': "SELECT * FROM Vaga"
        }
        
        data = {key: fetch_data(query) for key, query in queries.items()}
        return data

    except Exception as e:
        print(f"Erro: {e}")
        return {}

def analyze_data(data):
    """Analisa os dados e gera gráficos."""
    entrada_saida = data['entrada_saida']
    cliente = data['cliente']
    vaga = data['vaga']
    
    # Convertendo as colunas de data e hora para datetime
    entrada_saida['DataEntrada'] = pd.to_datetime(entrada_saida['DataEntrada'])
    entrada_saida['DataSaida'] = pd.to_datetime(entrada_saida['DataSaida'])
    
    # Converta as colunas HoraEntrada e HoraSaida para o formato de hora
    entrada_saida['HoraEntrada'] = pd.to_timedelta(entrada_saida['HoraEntrada'].astype(str))
    entrada_saida['HoraSaida'] = pd.to_timedelta(entrada_saida['HoraSaida'].astype(str))
    
    # Criando datetime completos para entrada e saída
    entrada_saida['TempoEntrada'] = entrada_saida['DataEntrada'] + entrada_saida['HoraEntrada']
    entrada_saida['TempoSaida'] = entrada_saida['DataSaida'] + entrada_saida['HoraSaida']
    
    # Calculando a duração do estacionamento em minutos
    entrada_saida['TempoEstacionado'] = (entrada_saida['TempoSaida'] - entrada_saida['TempoEntrada']).dt.total_seconds() / 60
    
    # Gráfico da média de horas que um cliente passa no estacionamento
    mean_duration = entrada_saida.groupby('ID_Cliente')['TempoEstacionado'].mean()
    plt.figure(figsize=(10, 6))
    mean_duration.plot(kind='bar')
    plt.title('Média de Tempo que um Cliente Passa no Estacionamento')
    plt.xlabel('ID do Cliente')
    plt.ylabel('Média de Tempo (minutos)')
    plt.xticks(rotation=0)
    plt.show()
    
    # Gráfico da vaga mais usada
    vaga_uso = entrada_saida['ID_Vaga'].value_counts()
    vaga_uso_names = vaga.set_index('ID_Vaga').loc[vaga_uso.index]['Número']
    plt.figure(figsize=(10, 6))
    vaga_uso.plot(kind='bar')
    plt.title('Número de Ocupações por Vaga')
    plt.xlabel('Número da Vaga')
    plt.ylabel('Número de Ocupações')
    plt.xticks(ticks=range(len(vaga_uso_names)), labels=vaga_uso_names, rotation=0)
    plt.show()
    
    # Cliente que vem mais frequentemente
    frequencia_cliente = entrada_saida['ID_Cliente'].value_counts()
    cliente_names = cliente.set_index('ID_Cliente').loc[frequencia_cliente.index]['Nome']
    plt.figure(figsize=(10, 6))
    frequencia_cliente.plot(kind='bar')
    plt.title('Número de Visitas por Cliente')
    plt.xlabel('Cliente')
    plt.ylabel('Número de Visitas')
    plt.xticks(ticks=range(len(cliente_names)), labels=cliente_names, rotation=45)
    plt.show()

def main():
    data = get_data_from_db()
    if data:
        analyze_data(data)

if __name__ == "__main__":
    main()
