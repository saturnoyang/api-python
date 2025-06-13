from fastapi import FastAPI

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Define un endpoint (ruta) para la raíz de tu API
@app.get("/")
async def read_root():
    return {"message": "¡Hola, Mundo!"}

# Puedes añadir otro endpoint si quieres
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q, "message": f"Obteniendo item {item_id} con query '{q}'"}
    return {"item_id": item_id, "message": f"Obteniendo item {item_id}"}

