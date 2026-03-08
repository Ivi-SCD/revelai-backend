"""
Agente de Evolução.

Analisa o histórico completo (uso, sentimento, reuniões) e mapeia a evolução
do cliente: marcos de maturidade, tendências, oportunidades de expansão.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.agents.llm import get_llm


EVOLUCAO_SYSTEM_PROMPT = """Você é um estrategista de Customer Success especialista em evolução e expansão de contas.

Com base em TODOS os dados fornecidos, mapeie a evolução do cliente.

Regras:
- Responda APENAS com JSON válido.
- maturidade deve ser: "inicial", "intermediario", "avancado", "referencia".
- tendência deve ser: "crescente", "estavel", "decrescente".
- score_evolucao de 0 a 100.
- Identifique marcos concretos de evolução.
- Impacto de cada marco: "baixo", "medio", "alto".
- Categoria: "performance", "adocao", "satisfacao", "expansao".

Formato JSON:
{{
    "marcos": [
        {{
            "titulo": "título do marco",
            "descricao": "descrição",
            "data_identificacao": "YYYY-MM-DD",
            "impacto": "baixo|medio|alto",
            "categoria": "performance|adocao|satisfacao|expansao"
        }}
    ],
    "maturidade_atual": "inicial|intermediario|avancado|referencia",
    "score_evolucao": 0,
    "tendencia": "crescente|estavel|decrescente",
    "oportunidades_expansao": ["oportunidade 1"],
    "recomendacoes_ia": ["recomendação 1"],
    "metricas_evolucao": {{
        "tempo_como_cliente_dias": 0,
        "num_marcos_atingidos": 0,
        "crescimento_adocao_percentual": 0
    }}
}}
"""

EVOLUCAO_USER_PROMPT = """Analise a evolução completa deste cliente:

## Análise de Uso Atual
{uso_data}

## Histórico de Reuniões Completo
{reunioes}

## Análise Inicial (contratação)
{analise_inicial}

## Informações do Cliente
{cliente_info}

## Informações do Produto
{produto_info}

Gere a análise de evolução JSON:"""


async def analisar_evolucao(
    uso_data: dict,
    reunioes: list[dict],
    analise_inicial: dict,
    cliente_info: dict,
    produto_info: dict,
) -> dict:
    """
    Analisa a evolução completa do cliente e retorna marcos, tendências e recomendações.
    """
    llm = get_llm(temperature=0.3)
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", EVOLUCAO_SYSTEM_PROMPT),
            ("human", EVOLUCAO_USER_PROMPT),
        ]
    )

    chain = prompt | llm | parser

    result = await chain.ainvoke(
        {
            "uso_data": str(uso_data) if uso_data else "Nenhum dado de uso disponível.",
            "reunioes": (
                "\n\n".join(
                    f"### Reunião {r.get('id_historico', 'N/A')} - {r.get('data_reuniao', 'N/A')}\n{r.get('informacoes_reuniao', '')}"
                    for r in reunioes
                )
                if reunioes
                else "Nenhuma reunião disponível."
            ),
            "analise_inicial": (
                str(analise_inicial) if analise_inicial else "Nenhuma análise inicial."
            ),
            "cliente_info": str(cliente_info),
            "produto_info": str(produto_info),
        }
    )

    return result
