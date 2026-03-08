"""
Script de população do banco de dados com dados realistas.
Cria 1 cliente, 1 produto, 10 reuniões e 10 documentos.

Uso:
    poetry run python scripts/populate.py
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.db.mongo_manager import init_database, get_mongo_manager
from app.repositories.clientes import ClienteRepository
from app.repositories.produtos import ProdutoRepository
from app.repositories.reunioes import ReuniaoRepository
from app.repositories.documentos import DocumentoRepository
from app.models.clientes import ClienteModel
from app.models.produtos import ProdutoModel
from app.models.reuniao import ReuniaoModel
from app.models.documentos import DocumentoModel


REUNIOES_DATA = [
    {
        "data_reuniao": "2026-01-10",
        "informacoes_reuniao": (
            "## Reunião de Descoberta Inicial\n\n"
            "Cliente apresentou sua empresa: TechVerde Soluções, 120 funcionários, "
            "atua no setor de logística. Problema principal: relatórios manuais em Excel "
            "que consomem 3 dias/mês de uma equipe de 5 analistas. Buscam automação, "
            "dashboards em tempo real e integração com o ERP SAP. Sentimento do cliente: "
            "animado e curioso. Canal: videochamada Google Meet."
        ),
    },
    {
        "data_reuniao": "2026-01-17",
        "informacoes_reuniao": (
            "## Reunião de Levantamento de Requisitos\n\n"
            "Mapeamos os KPIs principais: tempo médio de entrega, custo por rota, "
            "taxa de devoluções, NPS interno. Cliente quer alertas automáticos quando "
            "KPIs saem do threshold. Integração necessária: SAP ECC 6.0 via API REST. "
            "Equipe de TI do cliente tem 2 devs disponíveis para apoio. "
            "Sentimento: muito engajado, fez perguntas detalhadas."
        ),
    },
    {
        "data_reuniao": "2026-01-24",
        "informacoes_reuniao": (
            "## Reunião de Demonstração do Produto\n\n"
            "Apresentamos o Analytics Pro com dados simulados do setor logístico. "
            "Cliente ficou impressionado com os dashboards de tempo real. Pediu "
            "customização no layout de relatórios e exportação em PDF automatizada. "
            "Participaram 8 pessoas: diretoria, gestores e equipe de TI. "
            "Sentimento: muito positivo, já pediram proposta comercial."
        ),
    },
    {
        "data_reuniao": "2026-02-03",
        "informacoes_reuniao": (
            "## Reunião de Proposta Comercial\n\n"
            "Apresentamos 3 planos: Starter (R$2.000/mês), Standard (R$4.500/mês), "
            "Full (R$8.000/mês). Cliente se interessou pelo Standard mas pediu desconto "
            "de 10% para contrato anual. Discutimos SLA: 99.5% uptime, suporte 8x5. "
            "Sentimento: positivo mas cauteloso com investimento. Diretor financeiro "
            "pediu ROI projetado."
        ),
    },
    {
        "data_reuniao": "2026-02-10",
        "informacoes_reuniao": (
            "## Reunião de Negociação Final\n\n"
            "Enviamos estudo de ROI projetando economia de R$15.000/mês com automação "
            "dos relatórios. Cliente aceitou plano Standard com desconto de 8% no "
            "contrato anual. Assinatura prevista para semana que vem. Definimos kick-off "
            "de implementação para 24/02. Sentimento: confiante e decidido."
        ),
    },
    {
        "data_reuniao": "2026-02-24",
        "informacoes_reuniao": (
            "## Kick-off de Implementação\n\n"
            "Reunião com equipes completas de ambos os lados. Definimos cronograma: "
            "Semana 1-2: configuração de ambiente e integração SAP. "
            "Semana 3-4: customização de dashboards e relatórios. "
            "Semana 5-6: testes e treinamento. Go-live previsto para 07/04. "
            "Responsáveis definidos. Sentimento: motivados e organizados."
        ),
    },
    {
        "data_reuniao": "2026-03-10",
        "informacoes_reuniao": (
            "## Reunião de Acompanhamento - Semana 2\n\n"
            "Integração SAP concluída com sucesso. API funcionando, dados fluindo "
            "em tempo real. Pequeno atraso na customização do dashboard de rotas: "
            "precisou de ajuste no mapeamento de campos. Equipe de TI do cliente "
            "muito colaborativa. Sentimento: confiante, progresso visível."
        ),
    },
    {
        "data_reuniao": "2026-03-17",
        "informacoes_reuniao": (
            "## Reunião de Acompanhamento - Semana 3\n\n"
            "Dashboards principais prontos: KPIs de entrega, custos, devoluções. "
            "Cliente testou e pediu ajustes em cores e filtros de data. Relatório "
            "PDF automatizado funcionando. Alertas configurados para 3 KPIs. "
            "Treinamento agendado para próxima semana com 15 usuários. "
            "Sentimento: entusiasmado com resultados parciais."
        ),
    },
    {
        "data_reuniao": "2026-03-24",
        "informacoes_reuniao": (
            "## Treinamento de Usuários\n\n"
            "Treinamento realizado com 15 usuários em 2 turmas. Conteúdo: "
            "navegação em dashboards, criação de filtros, exportação de relatórios, "
            "configuração de alertas pessoais. Feedback muito positivo. 2 usuários "
            "pediram treinamento avançado em criação de dashboards customizados. "
            "Sentimento: empolgados para usar no dia a dia."
        ),
    },
    {
        "data_reuniao": "2026-04-07",
        "informacoes_reuniao": (
            "## Reunião de Go-Live e Acompanhamento\n\n"
            "Plataforma em produção há 1 semana. Adoção de 80% dos usuários treinados. "
            "Tempo de geração de relatórios reduziu de 3 dias para 15 minutos. "
            "2 bugs menores reportados e corrigidos. Cliente quer expandir para "
            "módulo de previsão de demanda (upsell). NPS interno subiu 12 pontos. "
            "Sentimento: muito satisfeito, já recomendando para parceiros."
        ),
    },
]

DOCUMENTOS_DATA = [
    {
        "informacoes_completas": (
            "## Briefing Inicial do Cliente\n\n"
            "**Empresa:** TechVerde Soluções Ltda.\n"
            "**Setor:** Logística e Transporte\n"
            "**Funcionários:** 120\n"
            "**Faturamento anual:** R$ 45 milhões\n"
            "**Problema:** Relatórios manuais em Excel, processos lentos\n"
            "**Objetivo:** Automação de dashboards e relatórios com integração SAP\n"
            "**Decisores:** Carlos Mendes (CEO), Ana Paula (CTO), Roberto (CFO)\n"
            "**Prazo desejado:** 2 meses para go-live"
        ),
    },
    {
        "informacoes_completas": (
            "## Mapeamento de KPIs\n\n"
            "1. **Tempo médio de entrega** - Meta: < 48h (atual: 72h)\n"
            "2. **Custo por rota** - Meta: redução de 15% (atual: R$180/rota)\n"
            "3. **Taxa de devoluções** - Meta: < 3% (atual: 5.2%)\n"
            "4. **NPS interno** - Meta: > 70 (atual: 58)\n"
            "5. **Produtividade de analistas** - Meta: +40% (economia de 3 dias/mês)\n"
            "**Fonte de dados:** SAP ECC 6.0, planilhas complementares"
        ),
    },
    {
        "informacoes_completas": (
            "## Proposta Comercial - Analytics Pro Standard\n\n"
            "**Plano:** Standard\n"
            "**Valor:** R$ 4.140/mês (desconto 8% contrato anual)\n"
            "**Contrato:** 12 meses\n"
            "**Incluso:** 10 dashboards, 5 relatórios automatizados, "
            "integração SAP, alertas ilimitados, suporte 8x5\n"
            "**SLA:** 99.5% uptime\n"
            "**Treinamento:** 2 turmas de 8 usuários incluídas\n"
            "**ROI projetado:** R$ 15.000/mês de economia"
        ),
    },
    {
        "informacoes_completas": (
            "## Contrato de Prestação de Serviços\n\n"
            "Contrato assinado digitalmente em 14/02/2026.\n"
            "**Partes:** RevelAI Tech (contratada) x TechVerde Soluções (contratante)\n"
            "**Objeto:** Licenciamento e implementação do Analytics Pro Standard\n"
            "**Vigência:** 12 meses a partir de 14/02/2026\n"
            "**Multa rescisória:** 20% do valor restante\n"
            "**Responsável técnico contratante:** Ana Paula Santos (CTO)"
        ),
    },
    {
        "informacoes_completas": (
            "## Plano de Implementação\n\n"
            "**Fase 1 (Sem 1-2):** Configuração de ambiente, integração SAP\n"
            "**Fase 2 (Sem 3-4):** Customização de dashboards e relatórios\n"
            "**Fase 3 (Sem 5-6):** Testes, treinamento e go-live\n"
            "**Equipe RevelAI:** 1 PM, 2 devs, 1 analista de dados\n"
            "**Equipe cliente:** 2 devs TI, 1 analista de negócios\n"
            "**Go-live previsto:** 07/04/2026"
        ),
    },
    {
        "informacoes_completas": (
            "## Especificação Técnica - Integração SAP\n\n"
            "**Sistema:** SAP ECC 6.0\n"
            "**Protocolo:** API REST via middleware RFC\n"
            "**Dados extraídos:** Pedidos (SD), Entregas (LE), Custos (CO)\n"
            "**Frequência:** Tempo real via webhooks + batch diário às 02:00\n"
            "**Autenticação:** OAuth 2.0 client credentials\n"
            "**Volume estimado:** ~5.000 registros/dia\n"
            "**Ambiente de homologação disponível:** Sim"
        ),
    },
    {
        "informacoes_completas": (
            "## Relatório de Testes - Fase UAT\n\n"
            "**Data:** 20/03/2026 a 28/03/2026\n"
            "**Cenários testados:** 47\n"
            "**Aprovados:** 44 (93.6%)\n"
            "**Bugs encontrados:** 3 (2 baixa, 1 média prioridade)\n"
            "- Bug #1: Filtro de data não considerava fuso horário (corrigido)\n"
            "- Bug #2: Exportação PDF cortava tabela longa (corrigido)\n"
            "- Bug #3: Alerta duplicado em horário de batch (corrigido)\n"
            "**Resultado:** Aprovado para go-live"
        ),
    },
    {
        "informacoes_completas": (
            "## Material de Treinamento\n\n"
            "**Módulo 1:** Navegação e dashboards (2h)\n"
            "**Módulo 2:** Filtros, segmentação e drill-down (1.5h)\n"
            "**Módulo 3:** Relatórios e exportação automatizada (1.5h)\n"
            "**Módulo 4:** Configuração de alertas pessoais (1h)\n"
            "**Módulo 5 (avançado):** Criação de dashboards customizados (3h)\n"
            "**Formato:** Presencial + gravação disponível na plataforma\n"
            "**Turmas:** 2 turmas de 8 pessoas (24-25/03/2026)"
        ),
    },
    {
        "informacoes_completas": (
            "## Relatório de Go-Live - Semana 1\n\n"
            "**Data go-live:** 07/04/2026\n"
            "**Usuários ativos:** 12 de 15 treinados (80%)\n"
            "**Dashboards mais acessados:** Tempo de entrega (89x), Custos (67x)\n"
            "**Relatórios gerados:** 23 automatizados na primeira semana\n"
            "**Tempo médio de relatório:** 15 min (antes: 3 dias)\n"
            "**Incidentes:** 2 bugs menores (corrigidos em < 4h)\n"
            "**Uptime:** 99.8%\n"
            "**Feedback geral:** Muito positivo"
        ),
    },
    {
        "informacoes_completas": (
            "## Análise de ROI - Primeiro Mês\n\n"
            "**Economia em horas de relatório:** 120h/mês → R$ 12.000\n"
            "**Redução de erros manuais:** estimativa R$ 3.000/mês\n"
            "**Melhoria em tempo de entrega:** 72h → 56h (-22%)\n"
            "**Taxa de devoluções:** 5.2% → 4.1% (-1.1 p.p.)\n"
            "**ROI realizado:** R$ 15.000/mês vs R$ 4.140/mês investido\n"
            "**Payback:** Menos de 1 mês\n"
            "**NPS interno:** 58 → 70 (+12 pontos)\n"
            "**Oportunidade de upsell:** Módulo de previsão de demanda"
        ),
    },
]


async def main():
    print("🚀 Iniciando população do banco de dados...\n")

    # Initialize DB
    await init_database()

    # Repos
    cliente_repo = ClienteRepository()
    produto_repo = ProdutoRepository()
    reuniao_repo = ReuniaoRepository()
    doc_repo = DocumentoRepository()

    # 1. Create client
    cliente = await cliente_repo.create(ClienteModel(nome_cliente="TechVerde Soluções"))
    id_cliente = cliente["id_cliente"]
    print(f"✅ Cliente criado: {cliente['nome_cliente']} ({id_cliente})")

    # 2. Create product
    produto = await produto_repo.create(
        ProdutoModel(
            nome="Analytics Pro",
            descricao="Plataforma de análise de dados com dashboards inteligentes e IA preditiva",
            tipo="plataforma",
            fase_atual="contratacao",
        )
    )
    id_produto = produto["id_produto"]
    print(f"✅ Produto criado: {produto['nome']} ({id_produto})")

    # 3. Create 10 reuniões
    print(f"\n📅 Criando {len(REUNIOES_DATA)} reuniões...")
    for i, r in enumerate(REUNIOES_DATA, 1):
        reuniao = await reuniao_repo.create(
            ReuniaoModel(
                id_cliente=id_cliente,
                id_produto=id_produto,
                data_reuniao=r["data_reuniao"],
                informacoes_reuniao=r["informacoes_reuniao"],
            )
        )
        print(f"   {i:>2}. {r['data_reuniao']} — {reuniao['id_historico'][:8]}...")

    # 4. Create 10 documentos
    print(f"\n📄 Criando {len(DOCUMENTOS_DATA)} documentos...")
    for i, d in enumerate(DOCUMENTOS_DATA, 1):
        doc = await doc_repo.create(
            DocumentoModel(
                id_cliente=id_cliente,
                id_produto=id_produto,
                informacoes_completas=d["informacoes_completas"],
            )
        )
        title = d["informacoes_completas"].split("\n")[0].replace("## ", "")
        print(f"   {i:>2}. {title} — {doc['id_documento'][:8]}...")

    # Summary
    print("\n" + "=" * 60)
    print("🎉 POPULAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"\n  id_cliente:  {id_cliente}")
    print(f"  id_produto:  {id_produto}")
    print(f"  Reuniões:    {len(REUNIOES_DATA)}")
    print(f"  Documentos:  {len(DOCUMENTOS_DATA)}")
    print()
    print("Próximos passos (cole no terminal ou use /docs):")
    print()
    print(f"  1. Gerar análise IA:")
    print(f"     POST /api/v1/analises/")
    print(f'     {{"id_cliente": "{id_cliente}", "id_produto": "{id_produto}"}}')
    print()
    print(f"  2. Gerar implementação IA:")
    print(f"     POST /api/v1/implementacao/gerar")
    print(f'     {{"id_cliente": "{id_cliente}", "id_produto": "{id_produto}"}}')
    print()
    print(f"  3. Ver jornada completa:")
    print(f"     GET /api/v1/jornada/cliente/{id_cliente}/produto/{id_produto}")
    print()

    # Close connection
    get_mongo_manager().close_connection()


if __name__ == "__main__":
    asyncio.run(main())
