from pydantic import BaseModel

from typing import Optional

class DocumentoModel(BaseModel):
    id_documento: Optional[str] = None
    id_cliente: Optional[str] = None
    id_produto: Optional[str] = None
    informacoes_completas: str