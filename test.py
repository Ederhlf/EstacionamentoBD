from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

app = QApplication([])

window = QWidget()
window.setWindowTitle("Teste de Cor de Fundo")
window.setStyleSheet("background-color: lightblue;")

layout = QVBoxLayout()
label = QLabel("Cor de Fundo Teste")
label.setStyleSheet("color: black;")

button = QPushButton("Botão Teste")
button.setStyleSheet("background-color: green; color: white;")

layout.addWidget(label)
layout.addWidget(button)

window.setLayout(layout)
window.show()

app.exec_()
