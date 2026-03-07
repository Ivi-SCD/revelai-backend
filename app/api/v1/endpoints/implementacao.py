from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.implementacao import (
    ImplementacaoRequest,
    TaskResponse,
    TaskUpdateRequest,
    ProgressoResponse,
    TreinamentoResponse,
    CursoConcluirRequest,
)
from app.services.implementacao import (
    ImplementacaoService,
    TaskService,
    TreinamentoService,
)

router = APIRouter(prefix="/implementacao", tags=["Implementação, Tasks & Treinamento"])

_impl_svc = ImplementacaoService()
_task_svc = TaskService()
_treinamento_svc = TreinamentoService()


@router.post("/gerar")
async def gerar_implementacao(req: ImplementacaoRequest):
    """
    Gera tasks de implementação e trilha de treinamento via IA
    a partir da última análise do cliente/produto.
    """
    try:
        return await _impl_svc.gerar_tasks_e_treinamento(req.id_cliente, req.id_produto)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Tasks ─────────────────────────────────────────────────


@router.get(
    "/tasks/cliente/{id_cliente}/produto/{id_produto}",
    response_model=list[TaskResponse],
)
async def listar_tasks(id_cliente: str, id_produto: str):
    return await _task_svc.listar_tasks(id_cliente, id_produto)


@router.patch("/tasks/{id_task}", response_model=TaskResponse)
async def atualizar_task(id_task: str, req: TaskUpdateRequest):
    try:
        return await _task_svc.atualizar_status(id_task, req.status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/tasks/progresso/cliente/{id_cliente}/produto/{id_produto}",
    response_model=ProgressoResponse,
)
async def obter_progresso(id_cliente: str, id_produto: str):
    return await _task_svc.obter_progresso(id_cliente, id_produto)


@router.get(
    "/tasks/concluidas/cliente/{id_cliente}/produto/{id_produto}",
)
async def verificar_conclusao(id_cliente: str, id_produto: str):
    all_done = await _task_svc.verificar_conclusao(id_cliente, id_produto)
    return {"todas_concluidas": all_done}


# ── Treinamento ───────────────────────────────────────────


@router.get(
    "/treinamentos/cliente/{id_cliente}/produto/{id_produto}",
    response_model=list[TreinamentoResponse],
)
async def listar_treinamentos(id_cliente: str, id_produto: str):
    return await _treinamento_svc.listar_treinamentos(id_cliente, id_produto)


@router.patch(
    "/treinamentos/{id_treinamento}/concluir-curso",
    response_model=TreinamentoResponse,
)
async def concluir_curso(id_treinamento: str, req: CursoConcluirRequest):
    try:
        return await _treinamento_svc.concluir_curso(id_treinamento, req.curso_index)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
