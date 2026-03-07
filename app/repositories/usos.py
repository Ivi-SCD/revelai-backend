from app.repositories.base import BaseRepository
from app.models.usos import UsoModel
from typing import Optional
from datetime import datetime


class UsoRepository(BaseRepository):
    def __init__(self):
        super().__init__("usos")

    async def create(self, uso: UsoModel) -> dict:
        data = uso.model_dump()
        if not data.get("id_uso"):
            data["id_uso"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_uso: str) -> Optional[dict]:
        return await self.find_by_id("id_uso", id_uso)

    async def get_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> Optional[dict]:
        docs = await self.find_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )
        return docs[0] if docs else None

    async def update(self, id_uso: str, update_data: dict) -> Optional[dict]:
        update_data["data_atualizacao"] = datetime.now().isoformat()
        return await self.update_one({"id_uso": id_uso}, update_data)
