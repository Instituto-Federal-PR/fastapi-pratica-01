from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AlunoResponse(BaseModel):
    id: int
    nome: str
    turma: int 
    class Config:
        from_attributes = True

class DisciplinaResponse(BaseModel):
    id: int
    nome: str
    carga_horaria: int
    class Config:
        from_attributes = True

# Dados que o cliente envia ao criar um curso
class CursoCreate(BaseModel):
    nome: str
    duracao: int 

# Dados que o FastAPI retorna para o cliente
class CursoResponse(BaseModel):
    id: int
    nome: str
    duracao: int
    criado_em: datetime
    alterado_em: datetime
    disciplina: list[DisciplinaResponse] = []
    aluno: list[AlunoResponse] = []

    # Necessário no Pydantic v2 para ler objetos do SQLAlchemy automaticamente
    class Config:
        from_attributes = True