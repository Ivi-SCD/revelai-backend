"""
Agente de Implementação.

Analisa a análise do cliente e gera tasks de implementação e trilhas de treinamento.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.core.settings import get_settings


TASKS_SYSTEM_PROMPT = """Você é um gerente de projetos especialista em implementação de soluções tecnológicas.

Com base na análise do cliente, gere uma lista de tasks de implementação e uma trilha de treinamento.

Regras:
- Responda APENAS com JSON válido.
- Cada task deve ter complexidade de 0 a 5.
- tempo_desenvolvimento em dias.
- status inicial sempre "pendente".
- A trilha deve conter cursos ordenados logicamente.
- Seja prático e específico.

Formato JSON:
{{
    "tasks": [
        {{
            "descricao": "descrição da task",
            "complexidade": 0,
            "tempo_desenvolvimento": 0,
            "status": "pendente"
        }}
    ],
    "treinamento": {{
        "trilha": "nome da trilha",
        "descricao_trilha": "descrição da trilha de aprendizado",
        "cursos": [
            {{
                "nome": "nome do curso",
                "descricao": "descrição",
                "duracao_horas": 0.0,
                "ordem": 1
            }}
        ],
        "recomendacoes_ia": ["recomendação 1", "recomendação 2"]
    }}
}}
"""

TASKS_USER_PROMPT = """Com base na análise abaixo, gere as tasks de implementação e trilha de treinamento:

## Análise do Cliente
{analise}

## Informações do Produto
{produto_info}

Gere o JSON com tasks e treinamento:"""


def _get_llm() -> ChatGroq:
    settings = get_settings()
    return ChatGroq(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        api_key=settings.GROQ_API_KEY,
        temperature=0.4,
        max_tokens=4096,
    )


async def gerar_implementacao(analise: dict, produto_info: dict) -> dict:
    """
    Gera tasks de implementação e trilha de treinamento a partir da análise.
    """
    llm = _get_llm()
    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TASKS_SYSTEM_PROMPT),
            ("human", TASKS_USER_PROMPT),
        ]
    )

    chain = prompt | llm | parser

    result = await chain.ainvoke(
        {
            "analise": str(analise),
            "produto_info": str(produto_info),
        }
    )

    return result
