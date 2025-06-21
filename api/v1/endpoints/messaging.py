from fastapi import APIRouter
from typing import Optional

router = APIRouter(
    prefix="/mensajeria",
    tags=["messaging"],
)

@router.get("/{mensaje_id}")
async def read_message(mensaje_id: int, q: Optional[str] = None):
    if q:
        return {"user": mensaje_id, "q": q, "message": f"Obteniendo item {mensaje_id} con query '{q}'"}
    return {"item_id": mensaje_id, "message": f"Obteniendo item {mensaje_id}"}