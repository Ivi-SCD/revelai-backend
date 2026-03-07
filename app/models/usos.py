from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class SentimentoReuniao(BaseModel):
    id_historico: str
    data_reuniao: str
    sentimento: str  # "positive" | "neutral" | "negative"
    resumo: str


class UsoModel(BaseModel):
    id_uso: Optional[str] = None
    id_cliente: str
    id_produto: str
    sentimentos_reunioes: list[SentimentoReuniao]
    sentimento_geral: str  # "positive" | "neutral" | "negative"
    score_satisfacao: int  # 0-100
    recomendacoes_ia: list[str]
    pontos_positivos: list[str]
    pontos_negativos: list[str]
    metricas_uso: dict[str, Any]  # metricas flexiveis
    data_criacao: str = datetime.now().isoformat()
    data_atualizacao: Optional[str] = None
