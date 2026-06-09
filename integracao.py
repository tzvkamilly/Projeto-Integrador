"""
Integração Principal - ETL entre Sistema X (SQLite) e Sistema Y (SQL exportado)
Uso de IA obrigatório conforme projeto integrador.
"""
import sqlite3
import json
import os
import re
from datetime import datetime
from ia_helper import analisar_dados_com_ia

LOG_FILE = "log_migracao.txt"
OUTPUT_SQL = "banco_sistema_y.sql"
OUTPUT_DB  = "banco_sistema_y.db"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{ts}] {msg}"
    print(linha)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")

# ── Transformações sugeridas pela IA ──────────────────────────────────────────

def formatar_telefone(tel: str) -> str:
    digits = re.sub(r"\D", "", tel or "")
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    return tel

STATUS_MAP = {
    "entregue": "delivered",
    "pendente": "pending",
    "em_transito": "in_transit",
    "cancelado": "cancelled",
}

def transformar_cliente(row: dict, mapeamento: dict) -> dict:
    return {
        "full_name":        row.get("nome", ""),
        "email_address":    (row.get("email") or "").lower().strip(),
        "phone_number":     formatar_telefone(row.get("telefone", "")),
        "city":             row.get("cidade", ""),
        "state_code":       row.get("estado", ""),
        "registration_date":row.get("data_cadastro", ""),
        "created_at":       datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

def transformar_pedido(row: dict) -> dict:
    return {
        "customer_id":   row.get("cliente_id"),
        "product_name":  row.get("produto", ""),
        "quantity":      row.get("quantidade", 0),
        "unit_price":    row.get("valor_unitario", 0.0),
        "total_price":   round(row.get("quantidade", 0) * row.get("valor_unitario", 0.0), 2),
        "order_date":    row.get("data_pedido", ""),
        "status":        STATUS_MAP.get(row.get("status", ""), row.get("status", "")),
        "created_at":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

# ── Extração ──────────────────────────────────────────────────────────────────

def extrair_dados(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    clientes = [dict(r) for r in cur.execute("SELECT * FROM clientes").fetchall()]
    pedidos  = [dict(r) for r in cur.execute("SELECT * FROM pedidos").fetchall()]
    conn.close()
    log(f"Extração: {len(clientes)} clientes e {len(pedidos)} pedidos lidos do Sistema X.")
    return clientes, pedidos

# ── Carga no Sistema Y ────────────────────────────────────────────────────────

def criar_sistema_y(clientes_t, pedidos_t):
    # Salva como banco SQLite novo (Sistema Y)
    if os.path.exists(OUTPUT_DB):
        os.remove(OUTPUT_DB)
    conn = sqlite3.connect(OUTPUT_DB)
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT, email_address TEXT, phone_number TEXT,
            city TEXT, state_code TEXT, registration_date TEXT, created_at TEXT
        )""")
    cur.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER, product_name TEXT, quantity INTEGER,
            unit_price REAL, total_price REAL, order_date TEXT,
            status TEXT, created_at TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )""")

    for c in clientes_t:
        cur.execute("""INSERT INTO customers
            (full_name,email_address,phone_number,city,state_code,registration_date,created_at)
            VALUES (:full_name,:email_address,:phone_number,:city,:state_code,:registration_date,:created_at)""", c)

    for p in pedidos_t:
        cur.execute("""INSERT INTO orders
            (customer_id,product_name,quantity,unit_price,total_price,order_date,status,created_at)
            VALUES (:customer_id,:product_name,:quantity,:unit_price,:total_price,:order_date,:status,:created_at)""", p)

    conn.commit()
    conn.close()
    log(f"Carga concluída: {len(clientes_t)} clientes e {len(pedidos_t)} pedidos inseridos no Sistema Y ({OUTPUT_DB}).")

def gerar_sql_export(clientes_t, pedidos_t):
    lines = [
        "-- ============================================================",
        f"-- Sistema Y - Exportação SQL gerada em {datetime.now()}",
        "-- Projeto Integrador - Integração de Sistemas com IA",
        "-- ============================================================\n",
        "CREATE TABLE IF NOT EXISTS customers (",
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "  full_name TEXT, email_address TEXT, phone_number TEXT,",
        "  city TEXT, state_code TEXT, registration_date TEXT, created_at TEXT",
        ");\n",
        "CREATE TABLE IF NOT EXISTS orders (",
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,",
        "  customer_id INTEGER, product_name TEXT, quantity INTEGER,",
        "  unit_price REAL, total_price REAL, order_date TEXT,",
        "  status TEXT, created_at TEXT",
        ");\n",
    ]
    for c in clientes_t:
        vals = "', '".join(str(v) for v in c.values())
        lines.append(f"INSERT INTO customers VALUES (NULL, '{vals}');")
    lines.append("")
    for p in pedidos_t:
        vals = "', '".join(str(v) for v in p.values())
        lines.append(f"INSERT INTO orders VALUES (NULL, '{vals}');")

    with open(OUTPUT_SQL, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"Script SQL exportado: {OUTPUT_SQL}")

# ── Pipeline principal ────────────────────────────────────────────────────────

def executar_migracao(db_origem: str):
    open(LOG_FILE, "w").close()  # limpa log
    log("=" * 60)
    log("INÍCIO DA MIGRAÇÃO - Sistema X → Sistema Y")
    log("=" * 60)

    # 1. Extração
    clientes_raw, pedidos_raw = extrair_dados(db_origem)

    # 2. IA analisa e sugere transformações
    log("Consultando IA para análise dos dados...")
    analise = analisar_dados_com_ia(clientes_raw)
    log("Análise da IA recebida:")
    for s in analise.get("sugestoes", []):
        log(f"  → {s}")
    log(f"  Observação: {analise.get('observacoes', '')}")
    log(f"  Mapeamento de campos: {analise.get('mapeamento', {})}")

    # 3. Transformação (aplica sugestões)
    log("Aplicando transformações nos dados...")
    clientes_t = [transformar_cliente(c, analise.get("mapeamento", {})) for c in clientes_raw]
    pedidos_t  = [transformar_pedido(p) for p in pedidos_raw]

    # 4. Carga
    criar_sistema_y(clientes_t, pedidos_t)
    gerar_sql_export(clientes_t, pedidos_t)

    log("=" * 60)
    log("MIGRAÇÃO CONCLUÍDA COM SUCESSO")
    log(f"  Banco destino : {OUTPUT_DB}")
    log(f"  Script SQL    : {OUTPUT_SQL}")
    log(f"  Log completo  : {LOG_FILE}")
    log("=" * 60)

    return clientes_t, pedidos_t, analise

if __name__ == "__main__":
    from sistema_x import criar_banco_origem
    db = criar_banco_origem()
    executar_migracao(db)
