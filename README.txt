==============================================================
  PROJETO INTEGRADOR - Integração de Sistemas com IA
  Centro Universitário Padre Anchieta - 2026
==============================================================

DESCRIÇÃO
---------
Aplicação ETL (Extract, Transform, Load) que integra dois sistemas
distintos utilizando Inteligência Artificial para análise e sugestão
de transformações nos dados.

  Sistema X (ORIGEM): banco SQLite - banco_sistema_x.db
  Sistema Y (DESTINO): banco SQLite novo + script SQL exportado

A IA é utilizada para:
  - Analisar os dados de origem
  - Sugerir transformações e mapeamento de campos
  - Recomendar melhorias na qualidade dos dados

ARQUIVOS DO PROJETO
-------------------
  main.py               → Ponto de entrada, executa o pipeline completo
  sistema_x.py          → Cria e popula o banco de origem (Sistema X)
  ia_helper.py          → Integração com a API da IA (Anthropic/Claude)
  integracao.py         → Pipeline ETL principal com transformações
  verificar_resultado.py→ Consulta e exibe os dados do Sistema Y

REQUISITOS
----------
  - Python 3.8 ou superior (testado no 3.12)
  - Sem dependências externas (usa apenas bibliotecas padrão do Python)

COMO EXECUTAR
-------------
1. Abra o terminal na pasta do projeto

2. Execute o pipeline completo com:
      python main.py

3. Ao final, serão gerados:
      banco_sistema_x.db  → banco de origem (Sistema X)
      banco_sistema_y.db  → banco de destino migrado (Sistema Y)
      banco_sistema_y.sql → script SQL com todos os dados migrados
      log_migracao.txt    → log completo com timestamps de cada etapa

O QUE A APLICAÇÃO FAZ (PASSO A PASSO)
--------------------------------------
  1. Cria o banco do Sistema X com tabelas: clientes e pedidos
  2. Popula com dados de exemplo (5 clientes, 7 pedidos)
  3. Consulta a IA com uma amostra dos dados
  4. A IA retorna: sugestões de transformação, mapeamento de campos
     e observações sobre qualidade dos dados
  5. Aplica as transformações:
       - Formata telefones para padrão (XX) XXXXX-XXXX
       - Traduz status: entregue→delivered, pendente→pending, etc.
       - Renomeia campos: nome→full_name, email→email_address, etc.
       - Calcula total_price (quantidade × valor_unitario)
       - Adiciona timestamp created_at em cada registro
  6. Insere os dados transformados no banco do Sistema Y
  7. Exporta script SQL completo (banco_sistema_y.sql)
  8. Exibe relatório de verificação com todos os registros

RESULTADO ESPERADO
------------------
  [Sistema X] Banco criado com sucesso: banco_sistema_x.db
  [TIMESTAMP] INÍCIO DA MIGRAÇÃO - Sistema X → Sistema Y
  [TIMESTAMP] Extração: 5 clientes e 7 pedidos lidos do Sistema X.
  [TIMESTAMP] Consultando IA para análise dos dados...
  [TIMESTAMP] Análise da IA recebida:
  [TIMESTAMP]   → Padronizar formato de telefone para (XX) XXXXX-XXXX
  [TIMESTAMP]   → Converter status de pedidos para inglês
  [TIMESTAMP]   → Adicionar campo 'created_at' com timestamp da migração
  [TIMESTAMP] Aplicando transformações nos dados...
  [TIMESTAMP] Carga concluída: 5 clientes e 7 pedidos inseridos no Sistema Y.
  [TIMESTAMP] MIGRAÇÃO CONCLUÍDA COM SUCESSO

COMPROVAÇÃO DE FUNCIONAMENTO
-----------------------------
  Print 1: terminal mostrando a execução do python main.py
  Print 2: seção "VERIFICAÇÃO DO SISTEMA Y" com clientes e pedidos
  Print 3: conteúdo do arquivo log_migracao.txt
  Print 4: (opcional) conteúdo do banco_sistema_y.sql aberto no editor

==============================================================
