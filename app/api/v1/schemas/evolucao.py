from pydantic import BaseModel
from typing import Any, Optional


class EvolucaoRequest(BaseModel):
    id_cliente: str
    id_produto: str


class MarcoResponse(BaseModel):
    titulo: str
    descricao: str
    data_identificacao: str
    impacto: str
    categoria: str


class EvolucaoResponse(BaseModel):
    id_evolucao: str
    id_cliente: str
    id_produto: str
    marcos: list[MarcoResponse]
    maturidade_atual: str
    maturidade_anterior: Optional[str] = None
    score_evolucao: int
    tendencia: str
    oportunidades_expansao: list[str]
    recomendacoes_ia: list[str]
    metricas_evolucao: dict[str, Any]
    data_criacao: str
    data_atualizacao: Optional[str] = None
