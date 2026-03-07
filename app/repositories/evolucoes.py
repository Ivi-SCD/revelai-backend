from app.repositories.base import BaseRepository
from app.models.evolucoes import EvolucaoModel
from typing import Optional
from datetime import datetime


class EvolucaoRepository(BaseRepository):
    def __init__(self):
        super().__init__("evolucaos")

    async def create(self, evolucao: EvolucaoModel) -> dict:
        data = evolucao.model_dump()
        if not data.get("id_evolucao"):
            data["id_evolucao"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_evolucao: str) -> Optional[dict]:
        return await self.find_by_id("id_evolucao", id_evolucao)

    async def get_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> Optional[dict]:
        docs = await self.find_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )
        return docs[0] if docs else None

    async def update(self, id_evolucao: str, update_data: dict) -> Optional[dict]:
        update_data["data_atualizacao"] = datetime.now().isoformat()
        return await self.update_one({"id_evolucao": id_evolucao}, update_data)
