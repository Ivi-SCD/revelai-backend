"""
Agente de Implementação.

Analisa a análise do cliente e gera tasks de implementação e trilhas de treinamento.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.agents.llm import get_llm


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

TASKS_USER_PROMPT = """Com base na análise abaixo, gere as tasks de implementação e trilha de treinamento.

IMPORTANTE: Use EXATAMENTE o nome do produto fornecido. NÃO invente nomes de produtos.

## Análise do Cliente
{analise}

## Informações do Produto (USE ESTE NOME EXATO)
Nome do Produto: {nome_produto}
Descrição: {descricao_produto}
Tipo: {tipo_produto}

Gere o JSON com tasks e treinamento específicos para o produto "{nome_produto}":"""


async def gerar_implementacao(analise: dict, produto_info: dict) -> dict:
    """
    Gera tasks de implementação e trilha de treinamento a partir da análise.
    """
    llm = get_llm(temperature=0.4)
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
            "nome_produto": produto_info.get("nome", "Produto"),
            "descricao_produto": produto_info.get("descricao", ""),
            "tipo_produto": produto_info.get("tipo", "plataforma"),
        }
    )

    return result
