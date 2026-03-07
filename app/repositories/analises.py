from app.repositories.base import BaseRepository
from app.models.analises import AnaliseModel
from typing import Optional


class AnaliseRepository(BaseRepository):
    def __init__(self):
        super().__init__("analises")

    async def create(self, analise: AnaliseModel) -> dict:
        data = analise.model_dump()
        if not data.get("id_analise"):
            data["id_analise"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_analise: str) -> Optional[dict]:
        return await self.find_by_id("id_analise", id_analise)

    async def get_latest_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> Optional[dict]:
        cursor = (
            self.collection.find({"id_cliente": id_cliente, "id_produto": id_produto})
            .sort("data_analise", -1)
            .limit(1)
        )
        async for doc in cursor:
            doc.pop("_id", None)
            return doc
        return None

    async def list_by_cliente(self, id_cliente: str) -> list[dict]:
        return await self.find_many({"id_cliente": id_cliente})
