from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CursoItem(BaseModel):
    nome: str
    descricao: str
    duracao_horas: float
    ordem: int
    concluido: bool = False
    data_conclusao: Optional[str] = None


class TreinamentoModel(BaseModel):
    id_treinamento: Optional[str] = None
    id_cliente: str
    id_produto: str
    trilha: str  # nome da trilha de aprendizado
    descricao_trilha: str
    cursos: list[CursoItem]
    progresso_percentual: float = 0.0  # 0-100
    status: str = "pendente"  # "pendente" | "em_andamento" | "concluido"
    recomendacoes_ia: list[str] = []
    data_criacao: str = datetime.now().isoformat()
    data_atualizacao: Optional[str] = None
