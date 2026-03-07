from app.repositories.base import BaseRepository
from app.models.reuniao import ReuniaoModel
from typing import Optional


class ReuniaoRepository(BaseRepository):
    def __init__(self):
        super().__init__("reuniao")

    async def create(self, reuniao: ReuniaoModel) -> dict:
        data = reuniao.model_dump()
        if not data.get("id_historico"):
            data["id_historico"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_historico: str) -> Optional[dict]:
        return await self.find_by_id("id_historico", id_historico)

    async def list_by_cliente(self, id_cliente: str) -> list[dict]:
        return await self.find_many({"id_cliente": id_cliente})

    async def list_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> list[dict]:
        return await self.find_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )

    async def list_after_date(
        self, id_cliente: str, id_produto: str, after_date: str
    ) -> list[dict]:
        return await self.find_many(
            {
                "id_cliente": id_cliente,
                "id_produto": id_produto,
                "data_reuniao": {"$gte": after_date},
            }
        )
