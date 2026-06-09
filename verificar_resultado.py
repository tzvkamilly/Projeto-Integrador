"""
Verificação - Consulta o banco do Sistema Y e exibe os dados migrados
"""
import sqlite3

def verificar(db_path="banco_sistema_y.db"):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DO SISTEMA Y (pós-migração)")
    print("=" * 60)

    print("\n📋 CLIENTES MIGRADOS:")
    print("-" * 60)
    for r in cur.execute("SELECT * FROM customers").fetchall():
        print(f"  [{r['id']}] {r['full_name']} | {r['email_address']} | {r['phone_number']} | {r['city']}/{r['state_code']}")

    print("\n🛒 PEDIDOS MIGRADOS:")
    print("-" * 60)
    for r in cur.execute("SELECT * FROM orders").fetchall():
        print(f"  [{r['id']}] Cliente {r['customer_id']} | {r['product_name']} | Qtd: {r['quantity']} | Total: R${r['total_price']:.2f} | Status: {r['status']}")

    total = cur.execute("SELECT SUM(total_price) FROM orders").fetchone()[0]
    print(f"\n💰 Valor total dos pedidos migrados: R$ {total:.2f}")

    conn.close()
    print("\n✅ Verificação concluída.\n")

if __name__ == "__main__":
    verificar()
