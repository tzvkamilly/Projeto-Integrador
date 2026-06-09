"""
IA Helper - Usa a API da Anthropic para sugerir transformações nos dados
"""
import json
import urllib.request

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

def analisar_dados_com_ia(dados_brutos: list[dict]) -> dict:
    """
    Envia uma amostra dos dados para a IA e pede sugestões de transformação.
    Retorna um dicionário com sugestões e o mapeamento de campos.
    """
    amostra = dados_brutos[:3] if len(dados_brutos) >= 3 else dados_brutos
    prompt = f"""Você é um especialista em integração de sistemas e ETL (Extract, Transform, Load).

Recebi os seguintes dados do Sistema X (SQLite) e preciso migrá-los para o Sistema Y (novo banco relacional).

Dados de amostra:
{json.dumps(amostra, ensure_ascii=False, indent=2)}

Por favor, retorne um JSON com:
1. "sugestoes": lista de até 3 melhorias ou transformações recomendadas para os dados
2. "mapeamento": objeto com os campos originais como chave e os nomes recomendados para o Sistema Y como valor
3. "observacoes": texto curto sobre qualidade dos dados

Responda SOMENTE com o JSON, sem markdown, sem explicações extras."""

    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 800,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            texto = body["content"][0]["text"].strip()
            return json.loads(texto)
    except Exception as e:
        # Fallback caso a API não esteja disponível (demonstração offline)
        print(f"[IA] API indisponível ({e}). Usando análise local de fallback.")
        return {
            "sugestoes": [
                "Padronizar formato de telefone para (XX) XXXXX-XXXX",
                "Converter status de pedidos para inglês: entregue→delivered, pendente→pending, em_transito→in_transit",
                "Adicionar campo 'created_at' com timestamp da migração"
            ],
            "mapeamento": {
                "nome": "full_name",
                "email": "email_address",
                "telefone": "phone_number",
                "cidade": "city",
                "estado": "state_code",
                "data_cadastro": "registration_date"
            },
            "observacoes": "Dados com boa consistência. Telefones sem máscara uniforme."
        }

