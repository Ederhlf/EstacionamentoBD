import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QMessageBox, QComboBox
from PyQt5.QtCore import Qt
import mysql.connector
from datetime import datetime, timedelta
from datetime import datetime, date, time

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Estacionamento")
        self.setGeometry(100, 100, 600, 400)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.tab_add_cliente = QWidget()
        self.tab_widget.addTab(self.tab_add_cliente, "Adicionar Cliente")

        self.tab_atualizar_saida = QWidget()
        self.tab_widget.addTab(self.tab_atualizar_saida, "Registrar Saída")

        self.add_cliente_ui()
        self.atualizar_saida_ui()

    def connect_to_db(self):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='erdeline',
                database='EstacionamentoDB'
            )
            return connection
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar ao banco de dados: {err}")
            return None

    def add_cliente_ui(self):
        layout = QVBoxLayout()

        self.nome_entry = QLineEdit()
        self.nome_entry.setPlaceholderText("Nome")
        layout.addWidget(self.nome_entry)

        self.telefone_entry = QLineEdit()
        self.telefone_entry.setPlaceholderText("Telefone")
        layout.addWidget(self.telefone_entry)

        self.placa_entry = QLineEdit()
        self.placa_entry.setPlaceholderText("Placa")
        layout.addWidget(self.placa_entry)

        self.modelo_entry = QLineEdit()
        self.modelo_entry.setPlaceholderText("Modelo")
        layout.addWidget(self.modelo_entry)

        self.cor_entry = QLineEdit()
        self.cor_entry.setPlaceholderText("Cor")
        layout.addWidget(self.cor_entry)

        self.plano_combobox = QComboBox()
        self.plano_combobox.addItems(["Plano Mensal", "Plano Semanal", "Plano Diário"])
        layout.addWidget(self.plano_combobox)

        add_cliente_button = QPushButton("Adicionar Cliente")
        add_cliente_button.clicked.connect(self.add_cliente)
        layout.addWidget(add_cliente_button)

        self.tab_add_cliente.setLayout(layout)

    def atualizar_saida_ui(self):
        layout = QVBoxLayout()

        self.placa_entry_saida = QLineEdit()
        self.placa_entry_saida.setPlaceholderText("Placa do Veículo")
        layout.addWidget(self.placa_entry_saida)

        registrar_saida_button = QPushButton("Registrar Saída")
        registrar_saida_button.clicked.connect(self.atualizar_saida)
        layout.addWidget(registrar_saida_button)

        self.tab_atualizar_saida.setLayout(layout)

    def add_cliente(self):
        nome = self.nome_entry.text()
        telefone = self.telefone_entry.text()
        placa = self.placa_entry.text()
        modelo = self.modelo_entry.text()
        cor = self.cor_entry.text()
        plano = self.plano_combobox.currentText()

        if not all([nome, telefone, placa, modelo, cor, plano]):
            QMessageBox.warning(self, "Aviso", "Todos os campos devem ser preenchidos!")
            return

        connection = self.connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                add_cliente_query = """
                INSERT INTO Cliente (Nome, Telefone, Placa, Modelo, Cor)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(add_cliente_query, (nome, telefone, placa, modelo, cor))
                cliente_id = cursor.lastrowid

                plano_id_query = "SELECT ID_Plano FROM PlanoEstacionamento WHERE Nome = %s"
                cursor.execute(plano_id_query, (plano,))
                plano_id = cursor.fetchone()[0]

                add_cliente_plano_query = """
                INSERT INTO ClientePlano (ID_Cliente, ID_Plano, DataInicio, DataFim)
                VALUES (%s, %s, %s, %s)
                """
                data_inicio = datetime.now().date()
                data_fim = data_inicio + timedelta(days=30)  # Ajuste conforme a duração do plano
                cursor.execute(add_cliente_plano_query, (cliente_id, plano_id, data_inicio, data_fim))

                add_entrada_query = """
                INSERT INTO EntradaSaida (ID_Cliente, ID_Vaga, DataEntrada, HoraEntrada)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(add_entrada_query, (cliente_id, 1, data_inicio, datetime.now().time()))

                connection.commit()
                QMessageBox.information(self, "Sucesso", "Cliente adicionado com sucesso!")
            except mysql.connector.Error as err:
                connection.rollback()
                QMessageBox.critical(self, "Erro", f"Erro ao adicionar cliente: {err}")
            finally:
                cursor.close()
                connection.close()

    def atualizar_saida(self):
        placa = self.placa_entry_saida.text()
        if not placa:
            QMessageBox.warning(self, "Aviso", "A placa do veículo deve ser preenchida!")
            return

        connection = self.connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Buscar cliente pelo número da placa
                cliente_id_query = "SELECT ID_Cliente, Nome FROM Cliente WHERE Placa = %s"
                cursor.execute(cliente_id_query, (placa,))
                result = cursor.fetchone()
                if not result:
                    QMessageBox.warning(self, "Aviso", "Placa não encontrada!")
                    return
                
                cliente_id, cliente_nome = result

                # Buscar o último registro de entrada do cliente que não possui saída registrada
                ultima_entrada_query = """
                SELECT ID_EntradaSaida, DataEntrada, HoraEntrada 
                FROM EntradaSaida 
                WHERE ID_Cliente = %s
                ORDER BY DataEntrada DESC, HoraEntrada DESC 
                LIMIT 1
                """
                cursor.execute(ultima_entrada_query, (cliente_id,))
                entrada_result = cursor.fetchone()
                if not entrada_result:
                    QMessageBox.warning(self, "Aviso", "Nenhum registro de entrada encontrado para este cliente.")
                    return

                id_entrada_saida, data_entrada, hora_entrada = entrada_result

                data_saida = datetime.now().date()
                hora_saida = datetime.now().time()

                # Atualizar saída no banco de dados
                update_saida_query = """
                UPDATE EntradaSaida
                SET DataSaida = %s, HoraSaida = %s
                WHERE ID_EntradaSaida = %s
                """
                cursor.execute(update_saida_query, (data_saida, hora_saida, id_entrada_saida))

                connection.commit()

                # Calcular o custo com base no registro de entrada e saída
                custo = self.calcular_custo(cliente_id, data_entrada, hora_entrada, data_saida, hora_saida)
                QMessageBox.information(self, "Sucesso", f"Saída registrada com sucesso!\nCliente: {cliente_nome}\nValor a pagar: R${custo:.2f}")
            except mysql.connector.Error as err:
                connection.rollback()
                QMessageBox.critical(self, "Erro", f"Erro ao registrar saída: {err}")
            finally:
                cursor.close()
                connection.close()
                    
    def calcular_custo(self, cliente_id, data_entrada, hora_entrada, data_saida, hora_saida):
        connection = self.connect_to_db()
        if connection:
            cursor = connection.cursor()
            try:
                # Buscar o plano do cliente
                query = """
                SELECT pe.Nome
                FROM ClientePlano cp
                JOIN PlanoEstacionamento pe ON cp.ID_Plano = pe.ID_Plano
                WHERE cp.ID_Cliente = %s
                """
                cursor.execute(query, (cliente_id,))
                result = cursor.fetchone()
                if result:
                    plano_nome = result[0]

                        # Adicionando mensagens de depuração
                    print(f"data_entrada: {data_entrada} (tipo: {type(data_entrada)})")
                    print(f"hora_entrada: {hora_entrada} (tipo: {type(hora_entrada)})")
                    print(f"data_saida: {data_saida} (tipo: {type(data_saida)})")
                    print(f"hora_saida: {hora_saida} (tipo: {type(hora_saida)})")

                        # Garantir que data_entrada e hora_entrada são do tipo correto
                    if isinstance(data_entrada, str):
                        data_entrada = datetime.strptime(data_entrada, '%Y-%m-%d').date()
                     # Corrigir tipo de hora_entrada se necessário
                    if isinstance(hora_entrada, str):
                        hora_entrada = datetime.strptime(hora_entrada, '%H:%M:%S').time()
                    elif isinstance(hora_entrada, timedelta):
                        # Converter timedelta para time (se possível)
                        hora_entrada = (datetime.min + hora_entrada).time()

                    if isinstance(data_saida, str):
                        data_saida = datetime.strptime(data_saida, '%Y-%m-%d').date()
                    if isinstance(hora_saida, str):
                        hora_saida = datetime.strptime(hora_saida, '%H:%M:%S').time()

                    # Verificar os tipos de data e hora
                    if not isinstance(data_entrada, date):
                        raise TypeError("data_entrada deve ser do tipo datetime.date")
                    if not isinstance(hora_entrada, time):
                        raise TypeError("hora_entrada deve ser do tipo datetime.time")
                    if not isinstance(data_saida, date):
                        raise TypeError("data_saida deve ser do tipo datetime.date")
                    if not isinstance(hora_saida, time):
                        raise TypeError("hora_saida deve ser do tipo datetime.time")


                    # Calcular a diferença de tempo entre a entrada e a saída
                    data_entrada_dt = datetime.combine(data_entrada, hora_entrada)
                    data_saida_dt = datetime.combine(data_saida, hora_saida)
                    delta = data_saida_dt - data_entrada_dt
                    total_horas = delta.total_seconds() / 3600

                    # Definir o custo por hora com base no plano
                    if plano_nome == "Plano Diário":
                        custo = total_horas * 10  # Exemplo de valor por hora
                    elif plano_nome == "Plano Semanal":
                        custo = total_horas * 7  # Exemplo de valor por hora
                    elif plano_nome == "Plano Mensal":
                        custo = total_horas * 5  # Exemplo de valor por hora
                    else:
                        custo = total_horas * 10  # Valor padrão por hora

                    return custo
                else:
                    QMessageBox.warning(self, 'Aviso', 'Plano do cliente não encontrado.')
                    return 0
            finally:
                cursor.close()
                connection.close()
        return 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
