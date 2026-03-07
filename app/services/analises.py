"""
Serviço de Análise — orquestra agent de contratação + persistência.
"""

from datetime import datetime
from app.repositories.analises import AnaliseRepository
from app.repositories.clientes import ClienteRepository
from app.repositories.documentos import DocumentoRepository
from app.repositories.reunioes import ReuniaoRepository
from app.agents.contratacao import analisar_cliente
from app.models.analises import AnaliseModel


class AnaliseService:
    def __init__(self):
        self._analise_repo = AnaliseRepository()
        self._cliente_repo = ClienteRepository()
        self._doc_repo = DocumentoRepository()
        self._reuniao_repo = ReuniaoRepository()

    async def gerar_analise(self, id_cliente: str, id_produto: str) -> dict:
        """
        Coleta documentos e reuniões, invoca o agente de IA e persiste a análise.
        """
        cliente = await self._cliente_repo.get_by_id(id_cliente)
        if not cliente:
            raise ValueError(f"Cliente {id_cliente} não encontrado")

        documentos = await self._doc_repo.list_by_cliente_produto(
            id_cliente, id_produto
        )
        reunioes = await self._reuniao_repo.list_by_cliente_produto(
            id_cliente, id_produto
        )

        ai_result = await analisar_cliente(
            cliente_info=cliente,
            documentos=documentos,
            reunioes=reunioes,
        )

        analise = AnaliseModel(
            id_cliente=id_cliente,
            id_produto=id_produto,
            metas_cliente=ai_result.get("metas_cliente", {}),
            problema_cliente=ai_result.get("problema_cliente", ""),
            grau_maturidade_empresa=ai_result.get("grau_maturidade_empresa", "baixo"),
            sentimento=ai_result.get("sentimento", "neutral"),
            proximos_passos=ai_result.get("proximos_passos", ""),
            canal=ai_result.get("canal", ""),
            evolucao_sentimento=ai_result.get("evolucao_sentimento", {}),
            velocidade_pipeline_dias=ai_result.get("velocidade_pipeline_dias", 0),
            engajamento_score=ai_result.get("engajamento_score", 0),
            plano_recomendado=ai_result.get("plano_recomendado", "starter"),
            justificativa_plano=ai_result.get("justificativa_plano", ""),
            riscos_identificados=ai_result.get("riscos_identificados", []),
            criterios_sucesso=ai_result.get("criterios_sucesso", []),
            data_analise=datetime.now().isoformat(),
        )

        return await self._analise_repo.create(analise)

    async def obter_analise(self, id_analise: str) -> dict:
        analise = await self._analise_repo.get_by_id(id_analise)
        if not analise:
            raise ValueError(f"Análise {id_analise} não encontrada")
        return analise

    async def obter_ultima_analise(self, id_cliente: str, id_produto: str) -> dict:
        analise = await self._analise_repo.get_latest_by_cliente_produto(
            id_cliente, id_produto
        )
        if not analise:
            raise ValueError("Nenhuma análise encontrada para este cliente/produto")
        return analise

    async def listar_por_cliente(self, id_cliente: str) -> list[dict]:
        return await self._analise_repo.list_by_cliente(id_cliente)
