from fastapi import APIRouter
from typing import Optional

router = APIRouter(
    prefix="/eventos",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{event_id}")
async def read_event(event_id: int, q: Optional[str] = None):
    if q:
        return {"user": event_id, "q": q, "message": f"Obteniendo item {event_id} con query '{q}'"}
    return {"item_id": event_id, "message": f"Obteniendo item {event_id}"}