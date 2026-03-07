"""
Serviço de Evolução — mapeia evolução do cliente via IA.
"""

from datetime import datetime
from app.repositories.evolucoes import EvolucaoRepository
from app.repositories.usos import UsoRepository
from app.repositories.reunioes import ReuniaoRepository
from app.repositories.analises import AnaliseRepository
from app.repositories.clientes import ClienteRepository
from app.repositories.produtos import ProdutoRepository
from app.agents.evolucao import analisar_evolucao
from app.models.evolucoes import EvolucaoModel, MarcoEvolucao


class EvolucaoService:
    def __init__(self):
        self._evolucao_repo = EvolucaoRepository()
        self._uso_repo = UsoRepository()
        self._reuniao_repo = ReuniaoRepository()
        self._analise_repo = AnaliseRepository()
        self._cliente_repo = ClienteRepository()
        self._produto_repo = ProdutoRepository()

    async def gerar_evolucao(self, id_cliente: str, id_produto: str) -> dict:
        """
        Coleta uso, reuniões, análise inicial e gera mapeamento de evolução via IA.
        """
        cliente = await self._cliente_repo.get_by_id(id_cliente)
        if not cliente:
            raise ValueError(f"Cliente {id_cliente} não encontrado")

        produto = await self._produto_repo.get_by_id(id_produto)
        if not produto:
            raise ValueError(f"Produto {id_produto} não encontrado")

        uso = await self._uso_repo.get_by_cliente_produto(id_cliente, id_produto)
        reunioes = await self._reuniao_repo.list_by_cliente_produto(
            id_cliente, id_produto
        )
        analise_inicial = await self._analise_repo.get_latest_by_cliente_produto(
            id_cliente, id_produto
        )

        ai_result = await analisar_evolucao(
            uso_data=uso,
            reunioes=reunioes,
            analise_inicial=analise_inicial,
            cliente_info=cliente,
            produto_info=produto,
        )

        marcos = [
            MarcoEvolucao(
                titulo=m.get("titulo", ""),
                descricao=m.get("descricao", ""),
                data_identificacao=m.get(
                    "data_identificacao", datetime.now().strftime("%Y-%m-%d")
                ),
                impacto=m.get("impacto", "medio"),
                categoria=m.get("categoria", "adocao"),
            )
            for m in ai_result.get("marcos", [])
        ]

        # Check for previous evolução to track maturidade change
        existing = await self._evolucao_repo.get_by_cliente_produto(
            id_cliente, id_produto
        )
        maturidade_anterior = existing.get("maturidade_atual") if existing else None

        evolucao = EvolucaoModel(
            id_cliente=id_cliente,
            id_produto=id_produto,
            marcos=marcos,
            maturidade_atual=ai_result.get("maturidade_atual", "inicial"),
            maturidade_anterior=maturidade_anterior,
            score_evolucao=ai_result.get("score_evolucao", 0),
            tendencia=ai_result.get("tendencia", "estavel"),
            oportunidades_expansao=ai_result.get("oportunidades_expansao", []),
            recomendacoes_ia=ai_result.get("recomendacoes_ia", []),
            metricas_evolucao=ai_result.get("metricas_evolucao", {}),
            data_criacao=datetime.now().isoformat(),
        )

        # Update product phase
        await self._produto_repo.update_fase(id_produto, "evolucao")

        if existing:
            return await self._evolucao_repo.update(
                existing["id_evolucao"], evolucao.model_dump()
            )
        return await self._evolucao_repo.create(evolucao)

    async def obter_evolucao(self, id_cliente: str, id_produto: str) -> dict:
        evolucao = await self._evolucao_repo.get_by_cliente_produto(
            id_cliente, id_produto
        )
        if not evolucao:
            raise ValueError("Nenhuma evolução encontrada")
        return evolucao
