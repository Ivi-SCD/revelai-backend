from pydantic import BaseModel

from typing import Optional

class ClienteModel(BaseModel):
    id_cliente: Optional[str] = None
    nome_cliente: str