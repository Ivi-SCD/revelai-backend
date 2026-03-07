from pydantic import BaseModel
from typing import Optional


class ReuniaoCreateRequest(BaseModel):
    id_cliente: str
    id_produto: str
    data_reuniao: str
    informacoes_reuniao: str


class ReuniaoResponse(BaseModel):
    id_historico: str
    id_cliente: str
    id_produto: str
    data_reuniao: str
    informacoes_reuniao: str


class DocumentoCreateRequest(BaseModel):
    id_cliente: str
    id_produto: str
    informacoes_completas: str


class DocumentoResponse(BaseModel):
    id_documento: str
    id_cliente: str
    id_produto: str
    informacoes_completas: str
