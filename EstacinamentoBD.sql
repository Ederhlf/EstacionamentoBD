-- Criação do banco de dados
-- CREATE DATABASE EstacionamentoDB;

-- Tabela Cliente
CREATE TABLE Cliente (
    ID_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100) NOT NULL,
    Telefone VARCHAR(15),
    Placa VARCHAR(10) UNIQUE NOT NULL,
    Modelo VARCHAR(50),
    Cor VARCHAR(30)
);

-- Tabela Vaga
CREATE TABLE Vaga (
    ID_Vaga INT AUTO_INCREMENT PRIMARY KEY,
    Número INT NOT NULL UNIQUE,
    Obs VARCHAR(100)
);

-- Tabela EntradaSaida
CREATE TABLE EntradaSaida (
    ID_EntradaSaida INT AUTO_INCREMENT PRIMARY KEY,
    ID_Cliente INT,
    ID_Vaga INT,
    DataEntrada DATE,
    HoraEntrada TIME,
    DataSaida DATE,
    HoraSaida TIME,
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
    FOREIGN KEY (ID_Vaga) REFERENCES Vaga(ID_Vaga)
);

-- Tabela PlanoEstacionamento
CREATE TABLE PlanoEstacionamento (
    ID_Plano INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(50) NOT NULL,
    Descrição TEXT,
    Valor DECIMAL(10, 2),
    Duração INT -- duração em dias
);

-- Tabela ClientePlano
CREATE TABLE ClientePlano (
    ID_Cliente INT,
    ID_Plano INT,
    DataInicio DATE,
    DataFim DATE,
    PRIMARY KEY (ID_Cliente),
    FOREIGN KEY (ID_Cliente) REFERENCES Cliente(ID_Cliente),
    FOREIGN KEY (ID_Plano) REFERENCES PlanoEstacionamento(ID_Plano)
);

-- Inserção de dados de exemplo

-- Adicionando alguns clientes
INSERT INTO Cliente (Nome, Telefone, Placa, Modelo, Cor)
VALUES
('João Silva', '123456789', 'ABC1234', 'Fusca', 'Azul'),
('Maria Oliveira', '987654321', 'XYZ5678', 'Civic', 'Preto'),
('Maria Paula', '998767644', 'PTD5644', 'Gol', 'Preto'),
('Fernando Henrique', '998504490', 'DVZ5604', 'Saveiro', 'Branco');

-- Adicionando algumas vagas
INSERT INTO Vaga (Número, Obs)
VALUES
(1, 'Perto da entrada'),
(2, 'Ao lado da saída'),
(4, 'final da quadra'),
(5, 'Bloco 2'),
(6, 'Térreo'),
(8, ''),
(7, '');

-- Adicionando alguns planos
INSERT INTO PlanoEstacionamento (Nome, Descrição, Valor, Duração)
VALUES
('Plano Mensal', 'Acesso ilimitado por 30 dias', 150.00, 30),
('Plano Semanal', 'Acesso ilimitado por 7 dias', 50.00, 7),
('Plano diário', 'Acesso por hora', 8.00, 1);

-- Adicionando plano aos clientes
INSERT INTO ClientePlano (ID_Cliente, ID_Plano, DataInicio, DataFim)
VALUES
(1, 1, '2024-08-01', '2024-08-31'),
(2, 2, '2024-08-01', '2024-08-07'),
(3, 3, '2024-08-01', '2024-08-01'),
(4, 3, '2024-08-01', '2024-08-01');

-- Registrando entradas e saídas
INSERT INTO EntradaSaida (ID_Cliente, ID_Vaga, DataEntrada, HoraEntrada, DataSaida, HoraSaida)
VALUES
(1, 1, '2024-08-01', '08:00:00', '2024-08-15', '17:00:00'),
(2, 2, '2024-08-01', '09:00:00', '2024-08-06', '18:00:00'),
(3, 7, '2024-08-01', '09:00:00', '2024-08-01', '15:00:00'),
(4, 3, '2024-08-01', '09:00:00', '2024-08-01', '17:00:00');
