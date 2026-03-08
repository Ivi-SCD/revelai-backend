from app.repositories.base import BaseRepository
from app.models.treinamentos import TreinamentoModel
from typing import Optional
from datetime import datetime


class TreinamentoRepository(BaseRepository):
    def __init__(self):
        super().__init__("treinamentos")

    async def create(self, treinamento: TreinamentoModel) -> dict:
        data = treinamento.model_dump()
        if not data.get("id_treinamento"):
            data["id_treinamento"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_treinamento: str) -> Optional[dict]:
        return await self.find_by_id("id_treinamento", id_treinamento)

    async def list_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> list[dict]:
        return await self.find_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )

    async def delete_by_cliente_produto(self, id_cliente: str, id_produto: str) -> int:
        """Delete all treinamentos for a given client/product. Returns count deleted."""
        result = await self.collection.delete_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )
        return result.deleted_count

    async def update_progresso(
        self, id_treinamento: str, progresso: float, status: str
    ) -> Optional[dict]:
        return await self.update_one(
            {"id_treinamento": id_treinamento},
            {
                "progresso_percentual": progresso,
                "status": status,
                "data_atualizacao": datetime.now().isoformat(),
            },
        )

    async def mark_curso_concluido(
        self, id_treinamento: str, curso_index: int
    ) -> Optional[dict]:
        treinamento = await self.get_by_id(id_treinamento)
        if not treinamento:
            return None
        cursos = treinamento["cursos"]
        if 0 <= curso_index < len(cursos):
            cursos[curso_index]["concluido"] = True
            cursos[curso_index]["data_conclusao"] = datetime.now().isoformat()
        concluidos = sum(1 for c in cursos if c["concluido"])
        progresso = round((concluidos / len(cursos)) * 100, 2) if cursos else 0
        status = "concluido" if progresso == 100 else "em_andamento"
        return await self.update_one(
            {"id_treinamento": id_treinamento},
            {
                "cursos": cursos,
                "progresso_percentual": progresso,
                "status": status,
                "data_atualizacao": datetime.now().isoformat(),
            },
        )
