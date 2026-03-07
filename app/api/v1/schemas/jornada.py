from pydantic import BaseModel
from typing import Any, Optional


class JornadaRequest(BaseModel):
    id_cliente: str
    id_produto: str


class FaseStatus(BaseModel):
    status: str
    dados: Optional[dict[str, Any]] = None


class ImplantacaoFase(BaseModel):
    status: str
    progresso_tasks: dict[str, Any]
    treinamentos: list[dict[str, Any]]


class JornadaResponse(BaseModel):
    cliente: dict[str, Any]
    produto: dict[str, Any]
    fases: dict[str, Any]
