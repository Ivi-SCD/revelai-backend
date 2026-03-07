from pydantic import BaseModel
from typing import Any, Optional


class UsoRequest(BaseModel):
    id_cliente: str
    id_produto: str


class SentimentoReuniaoResponse(BaseModel):
    id_historico: str
    data_reuniao: str
    sentimento: str
    resumo: str


class UsoResponse(BaseModel):
    id_uso: str
    id_cliente: str
    id_produto: str
    sentimentos_reunioes: list[SentimentoReuniaoResponse]
    sentimento_geral: str
    score_satisfacao: int
    recomendacoes_ia: list[str]
    pontos_positivos: list[str]
    pontos_negativos: list[str]
    metricas_uso: dict[str, Any]
    data_criacao: str
    data_atualizacao: Optional[str] = None
