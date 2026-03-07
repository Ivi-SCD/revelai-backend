from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.reunioes import (
    ReuniaoCreateRequest,
    ReuniaoResponse,
    DocumentoCreateRequest,
    DocumentoResponse,
)
from app.models.reuniao import ReuniaoModel
from app.models.documentos import DocumentoModel
from app.services.reunioes import ReuniaoService
from app.services.documentos import DocumentoService

router = APIRouter(prefix="/dados", tags=["Reuniões & Documentos"])

_reuniao_svc = ReuniaoService()
_documento_svc = DocumentoService()


# ── Reuniões ──────────────────────────────────────────────


@router.post("/reunioes", response_model=ReuniaoResponse)
async def criar_reuniao(req: ReuniaoCreateRequest):
    model = ReuniaoModel(
        id_cliente=req.id_cliente,
        id_produto=req.id_produto,
        data_reuniao=req.data_reuniao,
        informacoes_reuniao=req.informacoes_reuniao,
    )
    return await _reuniao_svc.criar_reuniao(model)


@router.get("/reunioes/cliente/{id_cliente}", response_model=list[ReuniaoResponse])
async def listar_reunioes_cliente(id_cliente: str):
    return await _reuniao_svc.listar_por_cliente(id_cliente)


@router.get(
    "/reunioes/cliente/{id_cliente}/produto/{id_produto}",
    response_model=list[ReuniaoResponse],
)
async def listar_reunioes_cliente_produto(id_cliente: str, id_produto: str):
    return await _reuniao_svc.listar_por_cliente_produto(id_cliente, id_produto)


@router.get("/reunioes/{id_historico}", response_model=ReuniaoResponse)
async def obter_reuniao(id_historico: str):
    try:
        return await _reuniao_svc.obter_reuniao(id_historico)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Documentos ────────────────────────────────────────────


@router.post("/documentos", response_model=DocumentoResponse)
async def criar_documento(req: DocumentoCreateRequest):
    model = DocumentoModel(
        id_cliente=req.id_cliente,
        id_produto=req.id_produto,
        informacoes_completas=req.informacoes_completas,
    )
    return await _documento_svc.criar_documento(model)


@router.get(
    "/documentos/cliente/{id_cliente}",
    response_model=list[DocumentoResponse],
)
async def listar_documentos_cliente(id_cliente: str):
    return await _documento_svc.listar_por_cliente(id_cliente)


@router.get(
    "/documentos/cliente/{id_cliente}/produto/{id_produto}",
    response_model=list[DocumentoResponse],
)
async def listar_documentos_cliente_produto(id_cliente: str, id_produto: str):
    return await _documento_svc.listar_por_cliente_produto(id_cliente, id_produto)
