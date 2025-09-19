from fastapi import FastAPI
import psycopg2.pool
from api.v1.endpoints import users, events, messaging

# Parámetros de conexión a la base de datos
db_params = {
    "host": "192.168.1.23",
    "port": 5432, 
    "database": "odoo_dev",
    "user": "odoo",
    "password": "myodoo"
}
# 1. Inicializar el pool de conexiones
#   - minconn: número mínimo de conexiones a mantener
#   - maxconn: número máximo de conexiones que el pool puede tener
pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **db_params
)
def get_data_from_db(query):
    """
    Función que toma una conexión del pool, ejecuta una consulta y la devuelve.
    """
    conn = None
    try:
        # 2. Tomar una conexión del pool
        conn = pool.getconn()
        cur = conn.cursor()

        # 3. Ejecutar la consulta
        cur.execute(query)
        result = cur.fetchall()
        
        # 4. Confirmar la transacción si es necesario
        # conn.commit()
        
        return result

    except (Exception, psycopg2.Error) as error:
        print(f"Error al obtener una conexión o ejecutar la consulta: {error}")
        return None
    
    finally:
        # 5. Asegurarse de devolver la conexión al pool
        if conn:
            pool.putconn(conn)
            print("Conexión devuelta al pool.")

# --- Uso del pool en la aplicación ---

print("Obteniendo 5 usuarios del modelo res_users...")

# Definir la consulta que queremos ejecutar
sql_query = """
    SELECT id, login, signature
    FROM res_users
    LIMIT 5;
"""

# Usar la función que gestiona el pool para obtener los datos
db_users = get_data_from_db(sql_query)

if db_users:
    for user in db_users:
        print(user)
else: # type: ignore
        print(user)

print("\nSimulando otra llamada a la base de datos...")
other_query = "SELECT COUNT(*) FROM res_users;"
user_count = get_data_from_db(other_query)
if user_count:
    print(f"Número total de usuarios: {user_count[0][0]}")
    
# Al finalizar la aplicación, cerrar todas las conexiones del pool
pool.closeall()
print("\nPool de conexiones cerrado.")

# Crea una instancia de la aplicación FastAPI
app = FastAPI()
app.state.db_pool = pool

# Define un endpoint (ruta) para la raíz de tu API
@app.get("/")
async def read_root(): # type: ignore
    return {"message": "¡Hola, Mundo!"}


# Incluye los routers de cada módulo
app.include_router(users.router)
app.include_router(events.router)
app.include_router(messaging.router)


# Evento de cierre para limpiar el pool
@app.on_event("shutdown")
def shutdown_event():
    pool.closeall()
    print("Pool de conexiones cerrado.")