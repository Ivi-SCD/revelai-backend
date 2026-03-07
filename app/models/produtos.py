from pydantic import BaseModel
from typing import Optional


class ProdutoModel(BaseModel):
    id_produto: Optional[str] = None
    nome: str
    descricao: str
    tipo: str  # "servico" | "plataforma" | "consultoria"
    fase_atual: (
        str  # "contratacao" | "implantacao" | "treinamento" | "uso" | "evolucao"
    )
