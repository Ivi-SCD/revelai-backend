from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class MarcoEvolucao(BaseModel):
    titulo: str
    descricao: str
    data_identificacao: str
    impacto: str  # "baixo" | "medio" | "alto"
    categoria: str  # "performance" | "adocao" | "satisfacao" | "expansao"


class EvolucaoModel(BaseModel):
    id_evolucao: Optional[str] = None
    id_cliente: str
    id_produto: str
    marcos: list[MarcoEvolucao]
    maturidade_atual: str  # "inicial" | "intermediario" | "avancado" | "referencia"
    maturidade_anterior: Optional[str] = None
    score_evolucao: int  # 0-100
    tendencia: str  # "crescente" | "estavel" | "decrescente"
    oportunidades_expansao: list[str]
    recomendacoes_ia: list[str]
    metricas_evolucao: dict[str, Any]
    data_criacao: str = datetime.now().isoformat()
    data_atualizacao: Optional[str] = None
