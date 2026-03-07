"""
Serviço de Implementação — gera tasks + treinamento a partir da análise via IA.
"""

from app.repositories.tasks import TaskRepository
from app.repositories.treinamentos import TreinamentoRepository
from app.repositories.analises import AnaliseRepository
from app.repositories.produtos import ProdutoRepository
from app.agents.implementacao import gerar_implementacao
from app.models.tasks import Tasks
from app.models.treinamentos import TreinamentoModel, CursoItem


class ImplementacaoService:
    def __init__(self):
        self._task_repo = TaskRepository()
        self._treinamento_repo = TreinamentoRepository()
        self._analise_repo = AnaliseRepository()
        self._produto_repo = ProdutoRepository()

    async def gerar_tasks_e_treinamento(self, id_cliente: str, id_produto: str) -> dict:
        """
        Obtém a última análise, chama a IA para gerar tasks e treinamento,
        e persiste ambos no MongoDB.
        """
        analise = await self._analise_repo.get_latest_by_cliente_produto(
            id_cliente, id_produto
        )
        if not analise:
            raise ValueError("Nenhuma análise encontrada. Execute a análise primeiro.")

        produto = await self._produto_repo.get_by_id(id_produto)
        if not produto:
            raise ValueError(f"Produto {id_produto} não encontrado")

        ai_result = await gerar_implementacao(analise=analise, produto_info=produto)

        # Persist tasks
        created_tasks = []
        for task_data in ai_result.get("tasks", []):
            task = Tasks(
                id_task="",
                id_cliente=id_cliente,
                id_produto=id_produto,
                descricao=task_data.get("descricao", ""),
                complexidade=task_data.get("complexidade", 1),
                tempo_desenvolvimento=task_data.get("tempo_desenvolvimento", 1),
                status="pendente",
            )
            created = await self._task_repo.create(task)
            created_tasks.append(created)

        # Persist treinamento
        treinamento_data = ai_result.get("treinamento", {})
        cursos = [
            CursoItem(
                nome=c.get("nome", ""),
                descricao=c.get("descricao", ""),
                duracao_horas=c.get("duracao_horas", 1.0),
                ordem=c.get("ordem", i + 1),
            )
            for i, c in enumerate(treinamento_data.get("cursos", []))
        ]

        treinamento = TreinamentoModel(
            id_cliente=id_cliente,
            id_produto=id_produto,
            trilha=treinamento_data.get("trilha", "Trilha padrão"),
            descricao_trilha=treinamento_data.get("descricao_trilha", ""),
            cursos=cursos,
            recomendacoes_ia=treinamento_data.get("recomendacoes_ia", []),
        )
        created_treinamento = await self._treinamento_repo.create(treinamento)

        # Update product phase
        await self._produto_repo.update_fase(id_produto, "implantacao")

        return {
            "tasks": created_tasks,
            "treinamento": created_treinamento,
        }


class TaskService:
    def __init__(self):
        self._repo = TaskRepository()

    async def listar_tasks(self, id_cliente: str, id_produto: str) -> list[dict]:
        return await self._repo.list_by_cliente_produto(id_cliente, id_produto)

    async def atualizar_status(self, id_task: str, status: str) -> dict:
        result = await self._repo.update_status(id_task, status)
        if not result:
            raise ValueError(f"Task {id_task} não encontrada")
        return result

    async def obter_progresso(self, id_cliente: str, id_produto: str) -> dict:
        return await self._repo.get_progress(id_cliente, id_produto)

    async def verificar_conclusao(self, id_cliente: str, id_produto: str) -> bool:
        return await self._repo.are_all_completed(id_cliente, id_produto)


class TreinamentoService:
    def __init__(self):
        self._repo = TreinamentoRepository()

    async def listar_treinamentos(self, id_cliente: str, id_produto: str) -> list[dict]:
        return await self._repo.list_by_cliente_produto(id_cliente, id_produto)

    async def concluir_curso(self, id_treinamento: str, curso_index: int) -> dict:
        result = await self._repo.mark_curso_concluido(id_treinamento, curso_index)
        if not result:
            raise ValueError(f"Treinamento {id_treinamento} não encontrado")
        return result
