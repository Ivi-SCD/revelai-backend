"""
Serviço de Jornada — visão consolidada do progresso do cliente através de todas as fases.
"""

from app.services.analises import AnaliseService
from app.services.implementacao import TaskService, TreinamentoService
from app.services.uso import UsoService
from app.services.evolucao import EvolucaoService
from app.repositories.clientes import ClienteRepository
from app.repositories.produtos import ProdutoRepository


class JornadaService:
    def __init__(self):
        self._cliente_repo = ClienteRepository()
        self._produto_repo = ProdutoRepository()
        self._analise_svc = AnaliseService()
        self._task_svc = TaskService()
        self._treinamento_svc = TreinamentoService()
        self._uso_svc = UsoService()
        self._evolucao_svc = EvolucaoService()

    async def obter_jornada_completa(self, id_cliente: str, id_produto: str) -> dict:
        """
        Retorna a visão completa da jornada do cliente com um produto.
        """
        cliente = await self._cliente_repo.get_by_id(id_cliente)
        produto = await self._produto_repo.get_by_id(id_produto)

        if not cliente or not produto:
            raise ValueError("Cliente ou Produto não encontrado")

        jornada = {
            "cliente": cliente,
            "produto": produto,
            "fases": {},
        }

        # Fase: Contratação (análise)
        try:
            analise = await self._analise_svc.obter_ultima_analise(
                id_cliente, id_produto
            )
            jornada["fases"]["contratacao"] = {
                "status": "concluida",
                "dados": analise,
            }
        except ValueError:
            jornada["fases"]["contratacao"] = {"status": "pendente", "dados": None}

        # Fase: Implantação (tasks + treinamento)
        progresso = await self._task_svc.obter_progresso(id_cliente, id_produto)
        treinamentos = await self._treinamento_svc.listar_treinamentos(
            id_cliente, id_produto
        )
        jornada["fases"]["implantacao"] = {
            "status": (
                "concluida"
                if progresso["percentual"] == 100
                else ("em_andamento" if progresso["total"] > 0 else "pendente")
            ),
            "progresso_tasks": progresso,
            "treinamentos": treinamentos,
        }

        # Fase: Uso
        try:
            uso = await self._uso_svc.obter_uso(id_cliente, id_produto)
            jornada["fases"]["uso"] = {"status": "ativa", "dados": uso}
        except ValueError:
            jornada["fases"]["uso"] = {"status": "pendente", "dados": None}

        # Fase: Evolução
        try:
            evolucao = await self._evolucao_svc.obter_evolucao(id_cliente, id_produto)
            jornada["fases"]["evolucao"] = {"status": "ativa", "dados": evolucao}
        except ValueError:
            jornada["fases"]["evolucao"] = {"status": "pendente", "dados": None}

        return jornada
