from fastapi import APIRouter, HTTPException, status, Body
from typing import List
from pydantic import BaseModel
import pandas as pd


#Creamos un objeto a partir de la clase FastAPI
router= APIRouter()

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

# Cargar los datos del CSV al iniciar la app
try:
    df = pd.read_csv('registros.csv')
    alumnos_excel = [Alumno(**row) for row in df.to_dict(orient='records')]
except Exception as e:
    alumnos_excel = []
    print(f"Error al cargar el archivo CSV: {e}")

#***Get
@router.get("/router1/")
async def listar_alumnos():
    return (alumnos_excel)
 # En el explorador colocamos la raiz de la ip: http://127.0.0.1:8000/router1/

#***Delete por promedio
@router.delete("/router2/{promedio}")
async def eliminar_alumnos_por_promedio(promedio: float):
    global alumnos_excel
    try:
        # Filtrar alumnos que no tienen el promedio dado
        nuevos_alumnos = [alumno for alumno in alumnos_excel if alumno.Promedio != promedio]
        if len(nuevos_alumnos) == len(alumnos_excel):
            raise HTTPException(status_code=404, detail="No se encontraron alumnos con ese promedio.")
        # Actualiza archivo CSV
        df_nuevo = pd.DataFrame([alumno.dict() for alumno in nuevos_alumnos])
        df_nuevo.to_csv('registros.csv', index=False)
        alumnos_excel = nuevos_alumnos
        return {"mensaje": "Alumnos eliminados correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar alumnos: {e}")

#***Get: Clasificar alumnos por carrera
@router.get("/router3/carreras")
async def clasificar_por_carrera():
    clasificados = {}
    for alumno in alumnos_excel:
        carrera = alumno.Carrera
        if carrera not in clasificados:
            clasificados[carrera] = []
        clasificados[carrera].append(alumno)
    return clasificados

#***Get: Clasificar alumnos por semestre
@router.get("/router4/semestres")
async def clasificar_por_semestre():
    clasificados = {}
    for alumno in alumnos_excel:
        semestre = alumno.Semestre
        if semestre not in clasificados:
            clasificados[semestre] = []
        clasificados[semestre].append(alumno)
    return clasificados


#***Put: Actualizar edad por matrícula
@router.put("/router5/{matricula}")
async def actualizar_edad(matricula: int, nueva_edad: int = Body(..., embed=True)):
    global alumnos_excel
    actualizado = False
    for alumno in alumnos_excel:
        if alumno.Matricula == matricula:
            alumno.Edad = nueva_edad
            actualizado = True
            break
    if not actualizado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    # Actualiza CSV
    try:
        df_nuevo = pd.DataFrame([alumno.dict() for alumno in alumnos_excel])
        df_nuevo.to_csv('registros.csv', index=False)
        return {"mensaje": "Edad actualizada correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar la edad: {e}")

#***Put: Actualizar semestre por matrícula
@router.put("/router6/semestre/{matricula}")
async def actualizar_semestre(matricula: int, nuevo_semestre: int = Body(..., embed=True)):
    global alumnos_excel
    actualizado = False
    for alumno in alumnos_excel:
        if alumno.Matricula == matricula:
            alumno.Semestre = nuevo_semestre
            actualizado = True
            break
    if not actualizado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    # Actualiza CSV
    try:
        df_nuevo = pd.DataFrame([alumno.dict() for alumno in alumnos_excel])
        df_nuevo.to_csv('registros.csv', index=False)
        return {"mensaje": "Semestre actualizado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el semestre: {e}")


#***Delete: Borrar alumnos por año de matrícula (primeros 4 dígitos)
@router.delete("/router7/borrar_por_anio/{anio}")
async def borrar_por_anio(anio: int):
    global alumnos_excel
    try:
        anio_str = str(anio)
        nuevos_alumnos = [alumno for alumno in alumnos_excel if str(alumno.Matricula)[:4] != anio_str]
        if len(nuevos_alumnos) == len(alumnos_excel):
            raise HTTPException(status_code=404, detail="No se encontraron alumnos con ese año.")
        # Actualiza CSV
        df_nuevo = pd.DataFrame([alumno.dict() for alumno in nuevos_alumnos])
        df_nuevo.to_csv('registros.csv', index=False)
        alumnos_excel = nuevos_alumnos
        return {"mensaje": "Alumnos eliminados correctamente por año."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar alumnos por año: {e}")

#***Get: Conteo de alumnos por carrera
@router.get("/router8/conteo_carreras")
async def conteo_por_carrera():
    conteo = {}
    for alumno in alumnos_excel:
        carrera = alumno.Carrera
        if carrera not in conteo:
            conteo[carrera] = 0
        conteo[carrera] += 1
    return conteo

#***Get: Ordenar alumnos por promedio descendente
@router.get("/router9/ordenar_por_promedio")
async def ordenar_por_promedio():
    alumnos_ordenados = sorted(alumnos_excel, key=lambda x: x.Promedio, reverse=True)
    return alumnos_ordenados

#***Put: Actualizar promedio por matrícula
@router.put("/router10/promedio/{matricula}")
async def actualizar_promedio(matricula: int, nuevo_promedio: float = Body(..., embed=True)):
    global alumnos_excel
    actualizado = False
    for alumno in alumnos_excel:
        if alumno.Matricula == matricula:
            alumno.Promedio = nuevo_promedio
            actualizado = True
            break
    if not actualizado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado.")
    # Actualiza CSV
    try:
        df_nuevo = pd.DataFrame([alumno.dict() for alumno in alumnos_excel])
        df_nuevo.to_csv('registros.csv', index=False)
        return {"mensaje": "Promedio actualizado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el promedio: {e}")
