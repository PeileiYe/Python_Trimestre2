from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from auth import router as auth_router
from deps import get_current_user

from db import get_db
from models import Incidente

app = FastAPI(
    title="Prueba Trimestre 2",
    description="FastAPI + Swagger + MySQL",
    version="1.0.0"
)

class IncidenteCreate(BaseModel):
    titulo: str = Field(..., max_length=150)
    descripcion: str
    prioridad: str = Field(..., max_length=20)
    estado: str = Field(..., max_length=20)
    
class IncidenteResponse(IncidenteCreate):
    id: int
    class Config:
        from_attributes = True

@app.get("/")
def root():
    return {"ok": True, "mensaje": "API con MySQL lista. Ve a /docs"}


@app.get("/incidentes", response_model=list[IncidenteResponse])
def listar_incidente(db: Session = Depends(get_db)):
    return db.query(Incidente).all()


# para login
app.include_router(auth_router)

# endpoints protegidos: necesita autenticacion

@app.get("/nombre")
def nombre(usuario: str = Depends(get_current_user)):
    return{"usuario": usuario}

@app.post("/incidentes", response_model=IncidenteResponse, status_code=201)
def crear_incidente(incidente: IncidenteCreate, 
                    db: Session = Depends(get_db),
                    usuario: str = Depends(get_current_user)):
    nuevo = Incidente(titulo=incidente.titulo, descripcion=incidente.descripcion, 
                      prioridad=incidente.prioridad, estado=incidente.estado)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/incidentes/{incidente_id}", response_model=IncidenteResponse)
def actualizar_incidente(
    incidente_id: int,
    incidente: IncidenteCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    existente = db.query(Incidente).filter(Incidente.id == incidente_id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    existente.titulo = incidente.titulo
    existente.descripcion = incidente.descripcion
    existente.prioridad = incidente.prioridad
    existente.estado = incidente.estado

    db.commit()
    db.refresh(existente)
    return existente

@app.delete("/incidentes/{incidente_id}", status_code=204)
def eliminar_incidente(
    incidente_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    existente = db.query(Incidente).filter(Incidente.id == incidente_id).first()
    if not existente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")

    db.delete(existente)
    db.commit()
    return