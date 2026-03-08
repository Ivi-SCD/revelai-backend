# RevelAI Backend

Plataforma de acompanhamento da jornada do cliente com IA — cobrindo todo o ciclo de **contratação → implantação → treinamento → uso → evolução**.

## Arquitetura

```
app/
├── agents/            # Lógica de IA (LangChain + Groq)
│   ├── contratacao.py    # Análise de contratação
│   ├── implementacao.py  # Geração de tasks e treinamento
│   ├── uso.py            # Análise de uso pós-implementação
│   └── evolucao.py       # Mapeamento de evolução
├── api/v1/
│   ├── endpoints/     # Rotas FastAPI separadas por função
│   │   ├── clientes.py
│   │   ├── dados.py      # Reuniões e Documentos
│   │   ├── analises.py
│   │   ├── implementacao.py
│   │   ├── uso.py
│   │   ├── evolucao.py
│   │   └── jornada.py    # Visão consolidada
│   ├── schemas/       # Schemas de request/response
│   └── router.py      # Agregação de rotas
├── core/
│   ├── settings.py    # Configurações (env vars)
│   └── db/
│       └── mongo_manager.py
├── models/            # Modelos Pydantic de domínio
├── repositories/      # Camada de acesso a dados (MongoDB)
├── services/          # Lógica de negócio e orquestração
└── main.py            # Entry point FastAPI
```

## Setup

```bash
# 1. Instalar dependências
poetry install

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas credenciais

# 3. Rodar
poetry run uvicorn app.main:app --reload
```

## Fluxo da Jornada

1. **Cadastrar cliente e produto** — `POST /api/v1/clientes/` e `POST /api/v1/clientes/produtos`
2. **Registrar reuniões e documentos** — `POST /api/v1/dados/reunioes` e `POST /api/v1/dados/documentos`
3. **Gerar análise (IA)** — `POST /api/v1/analises/` → agente analisa docs+reuniões
4. **Gerar implementação (IA)** — `POST /api/v1/implementacao/gerar` → cria tasks + trilha de treinamento
5. **Acompanhar tasks** — `GET /api/v1/implementacao/tasks/progresso/cliente/{id}/produto/{id}`
6. **Atualizar tasks** — `PATCH /api/v1/implementacao/tasks/{id_task}`
7. **Quando todas tasks 100%** → `POST /api/v1/uso/gerar` → análise de uso (IA)
8. **Gerar evolução (IA)** — `POST /api/v1/evolucao/gerar`
9. **Jornada completa** — `GET /api/v1/jornada/cliente/{id}/produto/{id}`

## API Docs

Com o servidor rodando: [http://localhost:8000/docs](http://localhost:8000/docs)
