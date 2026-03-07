from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime


class AnaliseModel(BaseModel):
    id_analise: Optional[str] = None
    id_cliente: str
    id_produto: str
    metas_cliente: dict[str, Any]
    problema_cliente: str
    grau_maturidade_empresa: str  # "baixo" | "medio" | "alto"
    sentimento: str  # "positive" | "neutral" | "negative"
    proximos_passos: str
    canal: str
    evolucao_sentimento: dict[str, str]  # {id_historico: sentimento}
    velocidade_pipeline_dias: int
    engajamento_score: int  # 0-100
    plano_recomendado: str  # "starter" | "standard" | "full" | "custom"
    justificativa_plano: str
    riscos_identificados: list[str]
    criterios_sucesso: list[str]
    data_analise: str = datetime.now().isoformat()
