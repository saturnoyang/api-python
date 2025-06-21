from fastapi import APIRouter
from typing import Optional

router = APIRouter(
    prefix="/usuarios",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}")
async def read_user(user_id: int, q: Optional[str] = None):
    if q:
        return {"user": user_id, "q": q, "message": f"Obteniendo item {user_id} con query '{q}'"}
    return {"item_id": user_id, "message": f"Obteniendo item {user_id}"}