from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.clientes import (
    ClienteCreateRequest,
    ClienteResponse,
    ProdutoCreateRequest,
    ProdutoResponse,
)
from app.models.clientes import ClienteModel
from app.models.produtos import ProdutoModel
from app.services.clientes import ClienteService
from app.services.produtos import ProdutoService

router = APIRouter(prefix="/clientes", tags=["Clientes & Produtos"])

_cliente_svc = ClienteService()
_produto_svc = ProdutoService()


# ── Clientes ──────────────────────────────────────────────


@router.post("/", response_model=ClienteResponse)
async def criar_cliente(req: ClienteCreateRequest):
    model = ClienteModel(nome_cliente=req.nome_cliente)
    return await _cliente_svc.criar_cliente(model)


@router.get("/", response_model=list[ClienteResponse])
async def listar_clientes():
    return await _cliente_svc.listar_clientes()


# ── Produtos ──────────────────────────────────────────────
# NOTE: Produto routes MUST come before /{id_cliente} to avoid
# FastAPI matching "produtos" as an id_cliente parameter.


@router.post("/produtos", response_model=ProdutoResponse)
async def criar_produto(req: ProdutoCreateRequest):
    model = ProdutoModel(
        id_cliente=req.id_cliente,
        nome=req.nome,
        descricao=req.descricao,
        tipo=req.tipo,
        fase_atual="contratacao",
    )
    return await _produto_svc.criar_produto(model)


@router.get("/produtos", response_model=list[ProdutoResponse])
async def listar_produtos():
    return await _produto_svc.listar_produtos()


@router.get("/produtos/{id_produto}", response_model=ProdutoResponse)
async def obter_produto(id_produto: str):
    try:
        return await _produto_svc.obter_produto(id_produto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Cliente by ID (must be LAST — catches any path segment) ──


@router.get("/{id_cliente}", response_model=ClienteResponse)
async def obter_cliente(id_cliente: str):
    try:
        return await _cliente_svc.obter_cliente(id_cliente)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
