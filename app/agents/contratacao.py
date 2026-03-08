"""
Agente de Análise de Contratação.

Analisa documentos e histórico de reuniões de um cliente/produto e produz
uma análise completa cobrindo: metas, problemas, maturidade, sentimento,
plano recomendado, riscos, critérios de sucesso, etc.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.agents.llm import get_llm

ANALISE_SYSTEM_PROMPT = """Você é um consultor especialista em Customer Success e análise de jornada do cliente.

Sua tarefa é analisar TODOS os documentos e reuniões fornecidos de um cliente e produzir uma análise completa em JSON.

Regras:
- Responda APENAS com JSON válido, sem texto adicional.
- Analise sentimentos, evolução, maturidade e engajamento com base nos dados reais.
- Seja específico e prático nas recomendações.
- O plano_recomendado deve ser um de: "starter", "standard", "full", "custom".
- O grau_maturidade_empresa deve ser: "baixo", "medio", "alto".
- sentimento deve ser: "positive", "neutral", "negative".
- engajamento_score é de 0 a 100.

Formato de saída JSON:
{{{{
    "metas_cliente": {{"meta1": "descrição", "meta2": "descrição"}},
    "problema_cliente": "descrição do principal problema identificado",
    "grau_maturidade_empresa": "baixo|medio|alto",
    "sentimento": "positive|neutral|negative",
    "proximos_passos": "descrição dos próximos passos recomendados",
    "canal": "canal predominante de contato",
    "evolucao_sentimento": {{"id_historico_1": "sentimento", "id_historico_2": "sentimento"}},
    "velocidade_pipeline_dias": 0,
    "engajamento_score": 0,
    "plano_recomendado": "starter|standard|full|custom",
    "justificativa_plano": "por que esse plano",
    "riscos_identificados": ["risco1", "risco2"],
    "criterios_sucesso": ["critério1", "critério2"]
}}}}
"""

ANALISE_USER_PROMPT = """Analise os seguintes dados do cliente e produza a análise completa:

## Dados do Cliente
{cliente_info}

## Documentos
{documentos}

## Histórico de Reuniões
{reunioes}

Produza a análise JSON completa:"""


async def analisar_cliente(
    cliente_info: dict,
    documentos: list[dict],
    reunioes: list[dict],
) -> dict:
    """
    Analisa documentos e reuniões de um cliente e retorna análise estruturada.
    """
    llm = get_llm(temperature=0.3)
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", ANALISE_SYSTEM_PROMPT),
            ("human", ANALISE_USER_PROMPT),
        ]
    )

    chain = prompt | llm | parser

    result = await chain.ainvoke(
        {
            "cliente_info": str(cliente_info),
            "documentos": (
                "\n\n".join(
                    f"### Documento {d.get('id_documento', 'N/A')}\n{d.get('informacoes_completas', '')}"
                    for d in documentos
                )
                if documentos
                else "Nenhum documento disponível."
            ),
            "reunioes": (
                "\n\n".join(
                    f"### Reunião {r.get('id_historico', 'N/A')} - {r.get('data_reuniao', 'N/A')}\n{r.get('informacoes_reuniao', '')}"
                    for r in reunioes
                )
                if reunioes
                else "Nenhuma reunião registrada."
            ),
        }
    )

    return result
