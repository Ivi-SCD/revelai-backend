# RevelAI Backend

![Imagem Logo Revelia](/docs/images/revelai.png)

Plataforma de acompanhamento da jornada do cliente com IA — cobrindo todo o ciclo de **contratação → implantação → treinamento → uso → evolução**.

## Tecnologias

| Tecnologia | Uso |
|------------|-----|
| **FastAPI** | Framework web assíncrono |
| **MongoDB** | Banco de dados NoSQL |
| **LangChain** | Orquestração de agentes IA |
| **Groq** | LLM provider (Llama 3.3 70B) |
| **Pydantic** | Validação de dados e schemas |
| **Poetry** | Gerenciamento de dependências |

## Arquitetura

```
app/
├── agents/            # Lógica de IA (LangChain + Groq)
│   ├── llm.py            # Factory do LLM compartilhado
│   ├── contratacao.py    # Análise de contratação
│   ├── implementacao.py  # Geração de tasks e treinamento
│   ├── uso.py            # Análise de uso pós-implementação
│   └── evolucao.py       # Mapeamento de evolução
├── api/v1/
│   ├── endpoints/     # Rotas FastAPI separadas por função
│   │   ├── clientes.py   # CRUD clientes e produtos
│   │   ├── dados.py      # Reuniões, documentos e histórico
│   │   ├── analises.py   # Geração de análises IA
│   │   ├── implementacao.py  # Tasks e treinamentos
│   │   ├── uso.py        # Análise de uso
│   │   ├── evolucao.py   # Mapeamento de evolução
│   │   └── jornada.py    # Visão consolidada
│   ├── schemas/       # Schemas de request/response
│   └── router.py      # Agregação de rotas
├── core/
│   ├── settings.py    # Configurações (env vars)
│   └── db/
│       └── mongo_manager.py  # Conexão MongoDB assíncrona
├── models/            # Modelos Pydantic de domínio
├── repositories/      # Camada de acesso a dados (MongoDB)
├── services/          # Lógica de negócio e orquestração
└── main.py            # Entry point FastAPI
```

## Setup Local

```bash
# 1. Clonar e entrar no diretório
git clone <repo-url>
cd revelai-backend

# 2. Instalar dependências
poetry install

# 3. Configurar variáveis de ambiente
cp .env.example .env
```

### Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `GROQ_API_KEY` | API key do Groq para LLM | `gsk_xxx...` |
| `MONGODB_CONNECTION_STRING` | URI de conexão MongoDB | `mongodb://localhost:27017` |
| `MONGODB_DATABASE_NAME` | Nome do banco | `revelai` |

```bash
# 4. Rodar servidor de desenvolvimento
poetry run uvicorn app.main:app --reload --port 8000
```

## Scripts Utilitários

```bash
# Limpar todos os dados do banco
poetry run python scripts/reset_database.py

# Popular banco com dados de exemplo
poetry run python scripts/populate.py

# Migrar produtos órfãos (sem id_cliente)
poetry run python scripts/migrate_products.py
```

## Fluxo da Jornada do Cliente

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ CONTRATAÇÃO │ -> │ IMPLANTAÇÃO │ -> │ TREINAMENTO │ -> │     USO     │ -> │  EVOLUÇÃO   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │                  │
      v                  v                  v                  v                  v
   Análise IA       Tasks geradas      Trilha criada     Métricas IA      Roadmap IA
```

### Endpoints por Fase

#### 1. Cadastro Inicial
```http
POST /api/v1/clientes/              # Criar cliente
POST /api/v1/clientes/produtos      # Criar produto (vinculado ao cliente)
```

#### 2. Coleta de Dados
```http
POST /api/v1/dados/reunioes         # Registrar reunião
POST /api/v1/dados/documentos       # Registrar documento
GET  /api/v1/dados/historico/cliente/{id}  # Histórico unificado
```

#### 3. Análise IA (Contratação)
```http
POST /api/v1/analises/              # Gerar análise com IA
GET  /api/v1/analises/cliente/{id}/produto/{id}
```

#### 4. Implementação
```http
POST  /api/v1/implementacao/gerar   # Gerar tasks + treinamento com IA
GET   /api/v1/implementacao/tasks/cliente/{id}/produto/{id}
PATCH /api/v1/implementacao/tasks/{id_task}  # Atualizar status
GET   /api/v1/implementacao/tasks/progresso/cliente/{id}/produto/{id}
```

#### 5. Uso e Evolução
```http
POST /api/v1/uso/gerar              # Análise de uso (após 100% tasks)
POST /api/v1/evolucao/gerar         # Roadmap de evolução
```

#### 6. Visão Consolidada
```http
GET /api/v1/jornada/cliente/{id}/produto/{id}  # Jornada completa
```

## Modelo de Dados

### Collections MongoDB

| Collection | Descrição |
|------------|-----------|
| `clientes` | Dados dos clientes |
| `produtos` | Produtos/serviços por cliente |
| `reuniao` | Registros de reuniões |
| `documentos` | Documentos e contratos |
| `analises` | Análises geradas pela IA |
| `tasks` | Tasks de implementação |
| `treinamentos` | Trilhas de treinamento |
| `uso` | Métricas de uso |
| `evolucao` | Roadmaps de evolução |

### Relacionamentos

```
Cliente (1) ──────> (N) Produto
    │                    │
    └──> Reuniões <──────┘
    └──> Documentos <────┘
    └──> Análises <──────┘
    └──> Tasks <─────────┘
    └──> Treinamentos <──┘
```

## Deploy

### Docker

```bash
docker build -t revelai-backend .
docker run -p 8000:8000 \
  -e GROQ_API_KEY=xxx \
  -e MONGODB_CONNECTION_STRING=xxx \
  revelai-backend
```

### IBM Code Engine

```bash
ibmcloud ce app create --name revelai-backend \
  --image <registry>/revelai-backend \
  --port 8000 \
  --env GROQ_API_KEY=xxx \
  --env MONGODB_CONNECTION_STRING=xxx
```

## Arquitetura Longo Prazo

![Imagem Arquitetura](/docs/images/diagrama-revelai.png)

## API Docs

Com o servidor rodando: [http://localhost:8000/docs](http://localhost:8000/docs)

## Contribuição

1. Crie uma branch: `git checkout -b feature/nova-feature`
2. Commit: `git commit -m "feat: descrição"`
3. Push: `git push origin feature/nova-feature`
4. Abra um Pull Request
