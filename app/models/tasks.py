from pydantic import BaseModel


class Tasks(BaseModel):
    id_task: str
    id_cliente: str
    id_produto: str
    descricao: str
    complexidade: int  # 0 a 5
    tempo_desenvolvimento: int  # em dias
    status: str  # "pendente", "em andamento", "concluida"
