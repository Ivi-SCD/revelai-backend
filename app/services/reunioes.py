from app.repositories.reunioes import ReuniaoRepository
from app.models.reuniao import ReuniaoModel


class ReuniaoService:
    def __init__(self):
        self._repo = ReuniaoRepository()

    async def criar_reuniao(self, reuniao: ReuniaoModel) -> dict:
        return await self._repo.create(reuniao)

    async def obter_reuniao(self, id_historico: str) -> dict:
        reuniao = await self._repo.get_by_id(id_historico)
        if not reuniao:
            raise ValueError(f"Reunião {id_historico} não encontrada")
        return reuniao

    async def listar_por_cliente(self, id_cliente: str) -> list[dict]:
        return await self._repo.list_by_cliente(id_cliente)

    async def listar_por_cliente_produto(
        self, id_cliente: str, id_produto: str
    ) -> list[dict]:
        return await self._repo.list_by_cliente_produto(id_cliente, id_produto)

    async def listar_apos_data(
        self, id_cliente: str, id_produto: str, after_date: str
    ) -> list[dict]:
        return await self._repo.list_after_date(id_cliente, id_produto, after_date)
