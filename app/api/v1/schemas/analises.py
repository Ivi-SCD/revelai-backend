from pydantic import BaseModel
from typing import Any


class AnaliseRequest(BaseModel):
    id_cliente: str
    id_produto: str


class AnaliseResponse(BaseModel):
    id_analise: str
    id_cliente: str
    id_produto: str
    metas_cliente: dict[str, Any]
    problema_cliente: str
    grau_maturidade_empresa: str
    sentimento: str
    proximos_passos: str
    canal: str
    evolucao_sentimento: dict[str, str]
    velocidade_pipeline_dias: int
    engajamento_score: int
    plano_recomendado: str
    justificativa_plano: str
    riscos_identificados: list[str]
    criterios_sucesso: list[str]
    data_analise: str
