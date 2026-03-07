from app.repositories.base import BaseRepository
from app.models.produtos import ProdutoModel
from typing import Optional


class ProdutoRepository(BaseRepository):
    def __init__(self):
        super().__init__("produtos")

    async def create(self, produto: ProdutoModel) -> dict:
        data = produto.model_dump()
        if not data.get("id_produto"):
            data["id_produto"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_produto: str) -> Optional[dict]:
        return await self.find_by_id("id_produto", id_produto)

    async def list_all(self) -> list[dict]:
        return await self.find_many({})

    async def update_fase(self, id_produto: str, fase: str) -> Optional[dict]:
        return await self.update_one({"id_produto": id_produto}, {"fase_atual": fase})
