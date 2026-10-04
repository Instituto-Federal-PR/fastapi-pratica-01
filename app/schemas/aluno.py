from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DisciplinaSchema(BaseModel):
    id: int
    nome: str
    class Config:
        from_attributes = True
    
class MatriculaResponse(BaseModel):
    aluno_id: int
    disciplina_id: int
    disciplina: Optional[DisciplinaSchema] = None
    class Config:
        from_attributes = True

class CursoResponse(BaseModel):
    id: int
    nome: str
    duracao: int 

    class Config:
        from_attributes = True

# Dados que o cliente envia ao criar um aluno
class AlunoCreate(BaseModel):
    nome: str
    turma: int
    curso_id: int  # Chave estrangeira ligando o aluno ao curso

# Dados que o FastAPI retorna para o cliente
class AlunoResponse(BaseModel):
    id: int
    nome: str
    turma: int
    curso_id: int
    criado_em: datetime
    alterado_em: datetime
    curso: CursoResponse
    matricula: list[MatriculaResponse] = []
    class Config:
        from_attributes = True