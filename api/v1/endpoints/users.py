from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import random
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

# Configuración para JWT (idealmente debería cargarse desde variables de entorno)
# ¡IMPORTANTE!: Cambia esta clave secreta en un entorno de producción.
SECRET_KEY = "your-super-secret-and-secure-key"  # TODO: Change this in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5 # Período de validez del código en el token

router = APIRouter(
    prefix="/usuarios",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

class EmailRequest(BaseModel):
    email: EmailStr

# Nuevo modelo para la continuación del registro de usuario
class UserRegistrationRequest(BaseModel):
    jwt_token: str = Field(..., description="JWT token recibido de /generate-code-token que contiene el correo y el código de verificación.")
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del usuario.")
    last_name: str = Field(..., min_length=1, max_length=100, description="Apellido del usuario.")
    gender: str = Field(..., description="Género del usuario (ej. 'Masculino', 'Femenino', 'Otro').", min_length=1, max_length=50)
    phone_number: str = Field(..., description="Número de teléfono del usuario.", min_length=5, max_length=20) # Validación básica de longitud

@router.get("/{user_id}")
async def read_user(user_id: int, q: Optional[str] = None):
    if q:
        return {"user": user_id, "q": q, "message": f"Obteniendo item {user_id} con query '{q}'"}
    return {"item_id": user_id, "message": f"Obteniendo item {user_id}"}

@router.post("/generate-code-token")
async def generate_code_token(request: EmailRequest):
    # Generar un código numérico aleatorio de 6 dígitos
    code = str(random.randint(100000, 999999))

    # Imprimir el código en la terminal para depuración
    print(f"Código de verificación generado para {request.email}: {code}")

    # Crear el payload del JWT y codificarlo
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": request.email, "code": code, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": encoded_jwt, "token_type": "bearer", "message": "Token con código generado exitosamente."}

@router.post("/continue-user-registration")
async def continue_user_registration(request: UserRegistrationRequest):
    try:
        # Decodificar el JWT
        payload = jwt.decode(request.jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        code: str = payload.get("code") # El código de 6 dígitos del JWT

        if email is None or code is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token inválido o incompleto. Faltan datos esenciales (email o código)."
            )

        # Aquí podrías añadir lógica adicional para verificar el código si fuera necesario.
        # Por ejemplo, si el código se envió por email y el usuario lo ingresa manualmente
        # en otro campo, lo compararías con el 'code' extraído del JWT.
        # Para este ejemplo, asumimos que la presencia de un JWT válido y no expirado es suficiente.

        # Imprimir los datos recibidos para depuración
        print(f"--- Registro de usuario continuado ---")
        print(f"Email del token: {email}")
        print(f"Código de verificación del token: {code}")
        print(f"Nombre: {request.name}")
        print(f"Apellido: {request.last_name}")
        print(f"Sexo: {request.gender}")
        print(f"Número de teléfono: {request.phone_number}")
        print(f"------------------------------------")

        # Aquí iría la lógica para guardar el usuario en la base de datos.
        # Por ejemplo:
        # user_data = {
        #     "email": email,
        #     "name": request.name,
        #     "last_name": request.last_name,
        #     "gender": request.gender,
        #     "phone_number": request.phone_number,
        #     "registration_date": datetime.now(timezone.utc) # Usar datetime.now(timezone.utc) para fechas con zona horaria
        # }
        # db.users.insert_one(user_data) # Suponiendo que tienes una conexión a la base de datos

        return {
            "message": "Registro de usuario completado exitosamente.",
            "user_email": email,
            "user_name": request.name,
            "user_last_name": request.last_name
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token JWT inválido o expirado. Por favor, genere un nuevo código."
        )
    except Exception as e:
        # Captura cualquier otra excepción inesperada para depuración
        print(f"Error inesperado en continue_user_registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor al procesar el registro: {str(e)}"
        )

# Modelo para el login de Rumbita
class RumbitaLoginRequest(BaseModel):
    email: EmailStr
    clave: str
    ubicacion: Optional[str] = None

@router.post("/rumbita-login")
async def rumbita_login(request: RumbitaLoginRequest):
    # Aquí iría la lógica de autenticación:
    # 1. Verificar el email y la clave en la base de datos.
    # 2. Si son correctos, generar un token de sesión (JWT).
    # 3. Registrar la ubicación si es necesario.

    # Por ahora, solo devolvemos los datos recibidos para confirmar que el endpoint funciona.
    print(f"Intento de login para el email: {request.email}")
    print(f"Ubicación reportada: {request.ubicacion}")

    return {
        "message": "Login endpoint a ser implementado.",
        "email": request.email,
        "ubicacion": request.ubicacion
    }
