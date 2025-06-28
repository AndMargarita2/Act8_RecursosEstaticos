#importamos el framework fastapi a nuestro entorno 
from fastapi import FastAPI, HTTPException, status, APIRouter, Header
app= FastAPI()

# Importamos el módulo de manejo de archivos estáticos
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Importamos el router de routers.py
from routers import router1
app.include_router(router1.router)

# Seguridad para contraseñas y JWT
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Importamos las dependencias necesarias para manejar JWT y contraseñas
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt


from pydantic import BaseModel

#----ACTIVIDAD 01------
from typing import List
import pandas as pd

# Definir el modelo Alumno para los datos del Excel
class Alumno(BaseModel):
    Nombre: str
    Matricula: int
    Edad: int
    Facultad: str
    Grado: str
    Carrera: str
    Genero: str
    Correo: str
    Promedio: float
    Semestre: int
    Imagen: str  # Nueva URL de imagen de perfil
    PasswordHash: str = None  # Hash de la contraseña

# Cargar los datos del CSV al iniciar la app
try:
    df = pd.read_csv('registros.csv')
    alumnos_excel = []
    for idx, row in enumerate(df.to_dict(orient='records')):
        genero = row['Genero'].strip().lower()
        if genero == 'femenino':
            imagen_url = f"https://randomuser.me/api/portraits/women/{row['Matricula'] % 100}.jpg"
        else:
            imagen_url = f"https://randomuser.me/api/portraits/men/{row['Matricula'] % 100}.jpg"
        row['Imagen'] = imagen_url
        alumnos_excel.append(Alumno(**row))
except Exception as e:
    alumnos_excel = []
    print(f"Error al cargar el archivo CSV: {e}")


#----ACTIVIDAD 02 ENDPOINTS POR QUERY------

@app.get("/alumnos", status_code=status.HTTP_200_OK)
async def listar_alumnos():
    alumnos = filter(lambda a: True, alumnos_excel)  # Devuelve todos los alumnos
    try:
        return list(alumnos)
    except:
        return {"error": "No se encontraron alumnos"}

@app.get("/alumno/matricula")
async def alumno_by_matricula(Matricula: int):
    alumnos = filter(lambda a: str(a.Matricula).strip() == str(Matricula).strip(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con esa matrícula"}

@app.get("/alumno/nombre")
async def alumno_by_nombre(Nombre: str):
    alumnos = filter(lambda a: a.Nombre.lower() == Nombre.lower(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con ese nombre"}

@app.get("/alumno/edad")
async def alumno_by_edad(Edad: int):
    alumnos = filter(lambda a: int(a.Edad) == int(Edad), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con esa edad"}

@app.get("/alumno/facultad")
async def alumno_by_facultad(Facultad: str):
    alumnos = filter(lambda a: a.Facultad.lower() == Facultad.lower(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con esa facultad"}

@app.get("/alumno/carrera")
async def alumno_by_carrera(Carrera: str):
    alumnos = filter(lambda a: a.Carrera.lower() == Carrera.lower(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con esa carrera"}

@app.get("/alumno/genero")
async def alumno_by_genero(Genero: str):
    alumnos = filter(lambda a: a.Genero.lower() == Genero.lower(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con ese género"}

@app.get("/alumno/promedio")
async def alumno_by_promedio(Promedio: float):
    alumnos = filter(lambda a: abs(float(a.Promedio) - float(Promedio)) < 0.01, alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con ese promedio"}

@app.get("/alumno/semestre")
async def alumno_by_semestre(Semestre: int):
    alumnos = filter(lambda a: int(a.Semestre) == int(Semestre), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con ese semestre"}

@app.get("/alumno/facultad_carrera")
async def alumno_by_facultad_carrera(Facultad: str, Carrera: str):
    alumnos = filter(lambda a: a.Facultad.lower() == Facultad.lower() and a.Carrera.lower() == Carrera.lower(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con esa facultad y carrera"}

@app.get("/alumno/edad_genero")
async def alumno_by_edad_genero(Edad: int, Genero: str):
    alumnos = filter(lambda a: int(a.Edad) == int(Edad) and a.Genero.lower() == Genero.lower(), alumnos_excel)
    try:
        return list(alumnos)
    except:
        return {"error": "No se ha encontrado el alumno con esa edad y género"}


#ACT5_CRUD
@app.post("/alumnos/", status_code=status.HTTP_201_CREATED)
async def crear_alumno(alumno: Alumno):
    for saved_alumno in alumnos_excel:
        if saved_alumno.Matricula == alumno.Matricula:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El alumno ya existe")
    alumnos_excel.append(alumno)
    return alumno

@app.put("/alumnos/", status_code=status.HTTP_200_OK)
async def actualizar_alumno(alumno: Alumno):
    for index, saved_alumno in enumerate(alumnos_excel):
        if saved_alumno.Matricula == alumno.Matricula:
            alumnos_excel[index] = alumno
            return alumno
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha actualizado el alumno porque no existe")

@app.delete("/alumnos/{matricula}", status_code=status.HTTP_200_OK)
async def eliminar_alumno(matricula: int):
    for index, saved_alumno in enumerate(alumnos_excel):
        if saved_alumno.Matricula == matricula:
            del alumnos_excel[index]
            return {"mensaje": f"Alumno con matrícula {matricula} eliminado correctamente"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha eliminado el alumno porque no existe")




SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Funciones de utilidad para contraseñas y JWT

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Buscar alumno por matrícula

def get_alumno_by_matricula(matricula: int):
    for alumno in alumnos_excel:
        if alumno.Matricula == matricula:
            return alumno
    return None

# Endpoint para registro de contraseña
@app.post("/register")
async def register(matricula: int, password: str):
    alumno = get_alumno_by_matricula(matricula)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    if alumno.PasswordHash:
        raise HTTPException(status_code=400, detail="El alumno ya tiene contraseña")
    alumno.PasswordHash = get_password_hash(password)
    return {"msg": "Contraseña registrada correctamente", "hash": alumno.PasswordHash}

# Endpoint para login (token JWT)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    alumno = get_alumno_by_matricula(int(form_data.username))
    if not alumno or not alumno.PasswordHash or not verify_password(form_data.password, alumno.PasswordHash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token = create_access_token(data={"sub": str(alumno.Matricula)})
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_alumno(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        matricula: str = payload.get("sub")
        if matricula is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    alumno = get_alumno_by_matricula(int(matricula))
    if alumno is None:
        raise credentials_exception
    return alumno

# Endpoint protegido que devuelve los datos del alumno autenticado
@app.get("/me")
async def read_users_me(current_alumno: Alumno = Depends(get_current_alumno)):
    return current_alumno

@app.get("/alumno/hash")
async def alumno_by_hash(Authorization: str = Header(None)):
    if not Authorization or not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token Bearer requerido")
    hash_token = Authorization.split(" ", 1)[1]
    alumno = next((a for a in alumnos_excel if a.PasswordHash == hash_token), None)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado para ese hash")
    return alumno

#levantamos el server Uvicornuvicorn main:app --reload
#con uvicorn main:app --reload

#http..... /imprimir
