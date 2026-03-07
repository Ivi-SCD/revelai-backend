from app.repositories.clientes import ClienteRepository
from app.models.clientes import ClienteModel


class ClienteService:
    def __init__(self):
        self._repo = ClienteRepository()

    async def criar_cliente(self, cliente: ClienteModel) -> dict:
        return await self._repo.create(cliente)

    async def obter_cliente(self, id_cliente: str) -> dict:
        cliente = await self._repo.get_by_id(id_cliente)
        if not cliente:
            raise ValueError(f"Cliente {id_cliente} não encontrado")
        return cliente

    async def listar_clientes(self) -> list[dict]:
        return await self._repo.list_all()
