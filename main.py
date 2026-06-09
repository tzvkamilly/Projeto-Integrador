"""
PROJETO INTEGRADOR - Integração de Sistemas com IA
Centro Universitário Padre Anchieta - 2026

Executa o pipeline completo:
  1. Cria banco de origem (Sistema X / SQLite)
  2. Chama IA para analisar e sugerir transformações
  3. Executa ETL (Extract, Transform, Load)
  4. Gera banco destino (Sistema Y) e script SQL
  5. Verifica e exibe resultado
"""

from sistema_x import criar_banco_origem
from integracao import executar_migracao
from verificar_resultado import verificar

if __name__ == "__main__":
    print("\n🚀 Iniciando Projeto Integrador - ETL com IA\n")
    db_origem = criar_banco_origem()
    executar_migracao(db_origem)
    verificar()
