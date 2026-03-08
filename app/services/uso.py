"""
Serviço de Uso — quando todas as tasks estão concluídas, gera análise de uso.
"""

from datetime import datetime
from app.repositories.usos import UsoRepository
from app.repositories.reunioes import ReuniaoRepository
from app.repositories.tasks import TaskRepository
from app.repositories.clientes import ClienteRepository
from app.repositories.produtos import ProdutoRepository
from app.agents.uso import analisar_uso
from app.models.usos import UsoModel, SentimentoReuniao


class UsoService:
    def __init__(self):
        self._uso_repo = UsoRepository()
        self._reuniao_repo = ReuniaoRepository()
        self._task_repo = TaskRepository()
        self._cliente_repo = ClienteRepository()
        self._produto_repo = ProdutoRepository()

    async def gerar_analise_uso(self, id_cliente: str, id_produto: str) -> dict:
        """
        Verifica se todas as tasks estão concluídas. Se sim, coleta as reuniões
        posteriores à conclusão e gera a análise de uso via IA.
        Replaces existing uso analysis if one exists.
        """
        all_done = await self._task_repo.are_all_completed(id_cliente, id_produto)
        if not all_done:
            raise ValueError(
                "Nem todas as tasks estão concluídas. Conclua todas antes de gerar a análise de uso."
            )

        cliente = await self._cliente_repo.get_by_id(id_cliente)
        if not cliente:
            raise ValueError(f"Cliente {id_cliente} não encontrado")

        produto = await self._produto_repo.get_by_id(id_produto)
        if not produto:
            raise ValueError(f"Produto {id_produto} não encontrado")

        reunioes = await self._reuniao_repo.list_by_cliente_produto(
            id_cliente, id_produto
        )

        ai_result = await analisar_uso(
            reunioes=reunioes,
            produto_info=produto,
            cliente_info=cliente,
        )

        sentimentos = [
            SentimentoReuniao(
                id_historico=s.get("id_historico", ""),
                data_reuniao=s.get("data_reuniao", ""),
                sentimento=s.get("sentimento", "neutral"),
                resumo=s.get("resumo", ""),
            )
            for s in ai_result.get("sentimentos_reunioes", [])
        ]

        uso = UsoModel(
            id_cliente=id_cliente,
            id_produto=id_produto,
            sentimentos_reunioes=sentimentos,
            sentimento_geral=ai_result.get("sentimento_geral", "neutral"),
            score_satisfacao=ai_result.get("score_satisfacao", 0),
            recomendacoes_ia=ai_result.get("recomendacoes_ia", []),
            pontos_positivos=ai_result.get("pontos_positivos", []),
            pontos_negativos=ai_result.get("pontos_negativos", []),
            metricas_uso=ai_result.get("metricas_uso", {}),
            data_criacao=datetime.now().isoformat(),
        )

        # Update product phase
        await self._produto_repo.update_fase(id_produto, "uso")

        # Replace existing uso if one exists, otherwise create new
        existing = await self._uso_repo.get_by_cliente_produto(id_cliente, id_produto)
        if existing:
            return await self._uso_repo.update(existing["id_uso"], uso.model_dump())
        return await self._uso_repo.create(uso)

    async def obter_uso(self, id_cliente: str, id_produto: str) -> dict:
        uso = await self._uso_repo.get_by_cliente_produto(id_cliente, id_produto)
        if not uso:
            raise ValueError("Nenhuma análise de uso encontrada")
        return uso
