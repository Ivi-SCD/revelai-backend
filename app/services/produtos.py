from app.repositories.produtos import ProdutoRepository
from app.models.produtos import ProdutoModel


class ProdutoService:
    def __init__(self):
        self._repo = ProdutoRepository()

    async def criar_produto(self, produto: ProdutoModel) -> dict:
        return await self._repo.create(produto)

    async def obter_produto(self, id_produto: str) -> dict:
        produto = await self._repo.get_by_id(id_produto)
        if not produto:
            raise ValueError(f"Produto {id_produto} não encontrado")
        return produto

    async def listar_produtos(self) -> list[dict]:
        return await self._repo.list_all()

    async def atualizar_fase(self, id_produto: str, fase: str) -> dict:
        result = await self._repo.update_fase(id_produto, fase)
        if not result:
            raise ValueError(f"Produto {id_produto} não encontrado")
        return result
