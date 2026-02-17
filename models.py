from sqlalchemy import Column, Integer, String, Text
from db import Base

class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=False)
    prioridad = Column(String(20), nullable=False)
    estado = Column(String(20), nullable=False)