from fastapi import APIRouter, HTTPException

from app.api.v1.schemas.jornada import JornadaResponse
from app.services.jornada import JornadaService

router = APIRouter(prefix="/jornada", tags=["Jornada Completa"])

_svc = JornadaService()


@router.get(
    "/cliente/{id_cliente}/produto/{id_produto}",
    response_model=JornadaResponse,
)
async def obter_jornada(id_cliente: str, id_produto: str):
    """
    Retorna a visão completa da jornada do cliente com o produto:
    contratação → implantação → uso → evolução.
    """
    try:
        return await _svc.obter_jornada_completa(id_cliente, id_produto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
