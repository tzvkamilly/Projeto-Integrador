-- ============================================================
-- Sistema Y - Exportação SQL gerada em 2026-06-02 10:01:35.680389
-- Projeto Integrador - Integração de Sistemas com IA
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  full_name TEXT, email_address TEXT, phone_number TEXT,
  city TEXT, state_code TEXT, registration_date TEXT, created_at TEXT
);

CREATE TABLE IF NOT EXISTS orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER, product_name TEXT, quantity INTEGER,
  unit_price REAL, total_price REAL, order_date TEXT,
  status TEXT, created_at TEXT
);

INSERT INTO customers VALUES (NULL, 'Ana Paula Souza', 'ana.souza@email.com', '(11) 98765-4321', 'São Paulo', 'SP', '2024-01-10', '2026-06-02 10:01:35');
INSERT INTO customers VALUES (NULL, 'Bruno Mendes', 'bruno.mendes@email.com', '(11) 91234-5678', 'Campinas', 'SP', '2024-02-15', '2026-06-02 10:01:35');
INSERT INTO customers VALUES (NULL, 'Carla Ferreira', 'carla.f@email.com', '(11) 93456-7890', 'Santos', 'SP', '2024-03-05', '2026-06-02 10:01:35');
INSERT INTO customers VALUES (NULL, 'Diego Oliveira', 'diego.o@email.com', '(21) 98700-1234', 'Rio de Janeiro', 'RJ', '2024-03-20', '2026-06-02 10:01:35');
INSERT INTO customers VALUES (NULL, 'Elaine Costa', 'elaine.c@email.com', '(31) 97654-3210', 'Belo Horizonte', 'MG', '2024-04-01', '2026-06-02 10:01:35');

INSERT INTO orders VALUES (NULL, '1', 'Notebook Dell', '1', '3200.0', '3200.0', '2024-01-15', 'delivered', '2026-06-02 10:01:35');
INSERT INTO orders VALUES (NULL, '1', 'Mouse Sem Fio', '2', '89.9', '179.8', '2024-02-10', 'delivered', '2026-06-02 10:01:35');
INSERT INTO orders VALUES (NULL, '2', 'Teclado Mecânico', '1', '350.0', '350.0', '2024-02-20', 'delivered', '2026-06-02 10:01:35');
INSERT INTO orders VALUES (NULL, '3', 'Monitor 24pol', '1', '1100.0', '1100.0', '2024-03-10', 'in_transit', '2026-06-02 10:01:35');
INSERT INTO orders VALUES (NULL, '4', 'Headset Gamer', '1', '250.0', '250.0', '2024-03-25', 'pending', '2026-06-02 10:01:35');
INSERT INTO orders VALUES (NULL, '5', 'Webcam HD', '1', '180.0', '180.0', '2024-04-05', 'delivered', '2026-06-02 10:01:35');
INSERT INTO orders VALUES (NULL, '2', 'SSD 480GB', '2', '220.0', '440.0', '2024-04-10', 'pending', '2026-06-02 10:01:35');