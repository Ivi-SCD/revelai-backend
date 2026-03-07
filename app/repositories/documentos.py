from app.repositories.base import BaseRepository
from app.models.documentos import DocumentoModel
from typing import Optional


class DocumentoRepository(BaseRepository):
    def __init__(self):
        super().__init__("documentos")

    async def create(self, documento: DocumentoModel) -> dict:
        data = documento.model_dump()
        if not data.get("id_documento"):
            data["id_documento"] = self._generate_id()
        return await self.insert_one(data)

    async def get_by_id(self, id_documento: str) -> Optional[dict]:
        return await self.find_by_id("id_documento", id_documento)

    async def list_by_cliente(self, id_cliente: str) -> list[dict]:
        return await self.find_many({"id_cliente": id_cliente})

    async def list_by_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> list[dict]:
        return await self.find_many(
            {"id_cliente": id_cliente, "id_produto": id_produto}
        )
