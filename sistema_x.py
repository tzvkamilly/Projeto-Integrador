"""
Sistema X - Criação e população do banco de dados SQLite (origem)
"""
import sqlite3
import os

DB_PATH = "banco_sistema_x.db"

def criar_banco_origem():
    # Remove banco anterior se existir (evita duplicatas ao rodar várias vezes)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            cidade TEXT,
            estado TEXT,
            data_cadastro TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            produto TEXT,
            quantidade INTEGER,
            valor_unitario REAL,
            data_pedido TEXT,
            status TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    clientes = [
        ("Ana Paula Souza",  "ana.souza@email.com",    "11987654321", "São Paulo",      "SP", "2024-01-10"),
        ("Bruno Mendes",     "bruno.mendes@email.com", "11912345678", "Campinas",        "SP", "2024-02-15"),
        ("Carla Ferreira",   "carla.f@email.com",      "11934567890", "Santos",          "SP", "2024-03-05"),
        ("Diego Oliveira",   "diego.o@email.com",      "21987001234", "Rio de Janeiro",  "RJ", "2024-03-20"),
        ("Elaine Costa",     "elaine.c@email.com",     "31976543210", "Belo Horizonte",  "MG", "2024-04-01"),
    ]

    pedidos = [
        (1, "Notebook Dell",    1, 3200.00, "2024-01-15", "entregue"),
        (1, "Mouse Sem Fio",    2,   89.90, "2024-02-10", "entregue"),
        (2, "Teclado Mecânico", 1,  350.00, "2024-02-20", "entregue"),
        (3, "Monitor 24pol",    1, 1100.00, "2024-03-10", "em_transito"),
        (4, "Headset Gamer",    1,  250.00, "2024-03-25", "pendente"),
        (5, "Webcam HD",        1,  180.00, "2024-04-05", "entregue"),
        (2, "SSD 480GB",        2,  220.00, "2024-04-10", "pendente"),
    ]

    cursor.executemany("INSERT INTO clientes (nome, email, telefone, cidade, estado, data_cadastro) VALUES (?, ?, ?, ?, ?, ?)", clientes)
    cursor.executemany("INSERT INTO pedidos (cliente_id, produto, quantidade, valor_unitario, data_pedido, status) VALUES (?, ?, ?, ?, ?, ?)", pedidos)

    conn.commit()
    conn.close()
    print(f"[Sistema X] Banco criado com sucesso: {DB_PATH}")
    return DB_PATH

if __name__ == "__main__":
    criar_banco_origem()
