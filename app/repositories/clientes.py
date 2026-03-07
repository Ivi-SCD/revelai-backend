from app.repositories.base import BaseRepository
from app.models.clientes import ClienteModel
from typing import Optional


class ClienteRepository(BaseRepository):
    def __init__(self):
        super().__init__("clientes")

    async def create(self, cliente: ClienteModel) -> dict:
        data = cliente.model_dump()
        if not data.get("id_cliente"):
            data["id_cliente"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_cliente: str) -> Optional[dict]:
        return await self.find_by_id("id_cliente", id_cliente)

    async def list_all(self) -> list[dict]:
        return await self.find_many({})
