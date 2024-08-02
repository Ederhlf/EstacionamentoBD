
import mysql.connector
from mysql.connector import Error

# Função para criar conexão com o banco de dados
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Altere para o seu usuário MySQL
            password='erdeline',  # Altere para a sua senha MySQL
            database='EstacionamentoDB'
        )
        if connection.is_connected():
            print("Conectado ao banco de dados")
            return connection
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para inserir dados
def insert_data(connection):
    cursor = connection.cursor()
    insert_query = """
        INSERT INTO Cliente (Nome, Telefone, Placa, Modelo, Cor)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = ('Carlos Lima', '111222333', 'DEF9012', 'Corolla', 'Prata')
    cursor.execute(insert_query, data)
    connection.commit()
    print("Dados inseridos com sucesso")

# Função para consultar dados
def fetch_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Cliente")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Função para atualizar dados
def update_data(connection):
    cursor = connection.cursor()
    update_query = """
        UPDATE Cliente
        SET Telefone = %s
        WHERE Nome = %s
    """
    data = ('999888777', 'Carlos Lima')
    cursor.execute(update_query, data)
    connection.commit()
    print("Dados atualizados com sucesso")

# Função para excluir dados
def delete_data(connection):
    cursor = connection.cursor()
    delete_query = """
        DELETE FROM Cliente
        WHERE Nome = %s
    """
    data = ('Carlos Lima',)
    cursor.execute(delete_query, data)
    connection.commit()
    print("Dados excluídos com sucesso")

# Função principal para executar as operações
def main():
    connection = create_connection()
    if connection:
        insert_data(connection)
        # fetch_data(connection)
        # update_data(connection)
        # fetch_data(connection)
        # delete_data(connection)
        fetch_data(connection)
        connection.close()

if __name__ == "__main__":
    main()
