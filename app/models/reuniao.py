from pydantic import BaseModel, Field

from typing import Optional


class ReuniaoModel(BaseModel):
    id_historico: Optional[str] = None
    id_cliente: Optional[str] = None
    id_produto: Optional[str] = None
    data_reuniao: str
    informacoes_reuniao: str


# Alias for backward compatibility
HistoricoModel = ReuniaoModel
