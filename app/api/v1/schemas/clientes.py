from pydantic import BaseModel
from typing import Optional


class ClienteCreateRequest(BaseModel):
    nome_cliente: str


class ClienteResponse(BaseModel):
    id_cliente: str
    nome_cliente: str


class ProdutoCreateRequest(BaseModel):
    nome: str
    descricao: str
    tipo: str  # "servico" | "plataforma" | "consultoria"


class ProdutoResponse(BaseModel):
    id_produto: str
    nome: str
    descricao: str
    tipo: str
    fase_atual: str
