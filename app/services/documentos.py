from app.repositories.documentos import DocumentoRepository
from app.models.documentos import DocumentoModel


class DocumentoService:
    def __init__(self):
        self._repo = DocumentoRepository()

    async def criar_documento(self, documento: DocumentoModel) -> dict:
        return await self._repo.create(documento)

    async def obter_documento(self, id_documento: str) -> dict:
        doc = await self._repo.get_by_id(id_documento)
        if not doc:
            raise ValueError(f"Documento {id_documento} não encontrado")
        return doc

    async def listar_por_cliente(self, id_cliente: str) -> list[dict]:
        return await self._repo.list_by_cliente(id_cliente)

    async def listar_por_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> list[dict]:
        return await self._repo.list_by_cliente_produto(id_cliente, id_produto)
