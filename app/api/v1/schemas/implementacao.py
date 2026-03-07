from pydantic import BaseModel
from typing import Any, Optional


class ImplementacaoRequest(BaseModel):
    id_cliente: str
    id_produto: str


class TaskResponse(BaseModel):
    id_task: str
    id_cliente: str
    id_produto: str
    descricao: str
    complexidade: int
    tempo_desenvolvimento: int
    status: str


class TaskUpdateRequest(BaseModel):
    status: str  # "pendente" | "em andamento" | "concluida"


class ProgressoResponse(BaseModel):
    total: int
    concluidas: int
    percentual: float


class CursoResponse(BaseModel):
    nome: str
    descricao: str
    duracao_horas: float
    ordem: int
    concluido: bool
    data_conclusao: Optional[str] = None


class TreinamentoResponse(BaseModel):
    id_treinamento: str
    id_cliente: str
    id_produto: str
    trilha: str
    descricao_trilha: str
    cursos: list[CursoResponse]
    progresso_percentual: float
    status: str
    recomendacoes_ia: list[str]
    data_criacao: str
    data_atualizacao: Optional[str] = None


class CursoConcluirRequest(BaseModel):
    curso_index: int


class ImplementacaoResponse(BaseModel):
    tasks: list[TaskResponse]
    treinamento: TreinamentoResponse
