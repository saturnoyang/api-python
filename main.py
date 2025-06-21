from fastapi import FastAPI
from api.v1.endpoints import users, events, messaging

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Define un endpoint (ruta) para la raíz de tu API
@app.get("/")
async def read_root(): # type: ignore
    return {"message": "¡Hola, Mundo!"}


# Incluye los routers de cada módulo
app.include_router(users.router)
app.include_router(events.router)
app.include_router(messaging.router)
