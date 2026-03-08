"""
Agente de Uso.

Analisa reuniões pós-conclusão de tasks e gera análise de uso do produto.
Categoriza sentimentos, gera recomendações e métricas de satisfação.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.agents.llm import get_llm


USO_SYSTEM_PROMPT = """Você é um analista de Customer Success especialista em análise de uso de produtos.

Com base nas reuniões pós-implementação, analise como o cliente está usando o produto.

Regras:
- Responda APENAS com JSON válido.
- Classifique o sentimento de CADA reunião como "positive", "neutral" ou "negative".
- score_satisfacao é de 0 a 100.
- Seja prático nas recomendações.

Formato JSON:
{{
    "sentimentos_reunioes": [
        {{
            "id_historico": "id",
            "data_reuniao": "data",
            "sentimento": "positive|neutral|negative",
            "resumo": "resumo da reunião"
        }}
    ],
    "sentimento_geral": "positive|neutral|negative",
    "score_satisfacao": 0,
    "recomendacoes_ia": ["recomendação 1"],
    "pontos_positivos": ["ponto 1"],
    "pontos_negativos": ["ponto 1"],
    "metricas_uso": {{
        "frequencia_uso": "diario|semanal|mensal",
        "funcionalidades_mais_usadas": ["func1"],
        "nivel_adocao": "baixo|medio|alto"
    }}
}}
"""

USO_USER_PROMPT = """Analise as seguintes reuniões pós-implementação do cliente:

## Reuniões
{reunioes}

## Contexto do Produto
{produto_info}

## Contexto do Cliente
{cliente_info}

Gere a análise de uso JSON:"""


async def analisar_uso(
    reunioes: list[dict],
    produto_info: dict,
    cliente_info: dict,
) -> dict:
    """
    Analisa reuniões pós-implementação e gera análise de uso.
    """
    llm = get_llm(temperature=0.3)
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", USO_SYSTEM_PROMPT),
            ("human", USO_USER_PROMPT),
        ]
    )

    chain = prompt | llm | parser

    result = await chain.ainvoke(
        {
            "reunioes": (
                "\n\n".join(
                    f"### Reunião {r.get('id_historico', 'N/A')} - {r.get('data_reuniao', 'N/A')}\n{r.get('informacoes_reuniao', '')}"
                    for r in reunioes
                )
                if reunioes
                else "Nenhuma reunião disponível."
            ),
            "produto_info": str(produto_info),
            "cliente_info": str(cliente_info),
        }
    )

    return result
