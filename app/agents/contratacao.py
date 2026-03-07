"""
Esse agente deve captar informações da empresa (continuamente)
vulgo cliente, deve:
- elaborar * contrato, 
- * encaminhar ao cliente solicitando
- * assinatura, receber,verificar , assinaturas
- * Importante métricas de reuniões, quantas reuniões teve, etc.
- Histórico de contratação

Informações Importantes:
- Historico:
    {
        "id_historico": ID,
        "id_cliente": ID,
        "id_produto": ID,
        "informacoes_completas": str (markdown llm ready)               (ESSA PARTE IA SE INTEGRARIA AS FERRAMENTAS PRA MONTAR ESSAS INFOS)
        "data_reuniao": datetime
        "canal"
    }

- Documentos:
    {
        "id_documento": ID,
        "id_cliente": ID,
        "id_produto": ID,
        "canal": str
        "informacoes_completas": str (markdown llm ready) 

    }

Funcionalidades:
- Analisar Cliente [ENDPOINT]
{
        "metas_cliente": dict(str, Any)
        "problema_cliente": str
        "grau_maturidade_empresa"
        "sentimento"
        "proximos_passos"
        "canal"
        "evolucao_sentimento": ["neutral", "positive", "positive", "positive"],
        "taxa_comparecimento": 1.0,      # cliente não faltou nenhuma
        "velocidade_pipeline_dias": 18,  # dias desde primeiro contato
        "engajamento_score": 87          # calculado pela IA
        "plano_recomendado": str,           # starter | standard | full | custom
        "justificativa_plano": str,         # por que esse plano
        "riscos_identificados": [str],      # o que pode dar errado
        "criterios_sucesso": [str],         # como vamos medir se deu certo
        "estimativa_roi": float,            # R$ de retorno esperado
        "timeline_recomendada": int,        # meses até valor percebido
}
"""