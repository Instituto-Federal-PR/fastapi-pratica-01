from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class AlunoSchema(BaseModel):
    id: int
    nome: str
    turma: int
    class Config:
        from_attributes = True

class MatriculaResponse(BaseModel):
    aluno_id: int
    disciplina_id: int
    aluno: Optional[AlunoSchema] = None
    class Config:
        from_attributes = True
class CursoResponse(BaseModel):
    id: int
    nome: str
    duracao: int
    # Necessário no Pydantic v2 para ler objetos do SQLAlchemy automaticamente
    class Config:
        from_attributes = True

# Dados que o cliente envia ao criar uma disciplina
class DisciplinaCreate(BaseModel):
    nome: str
    carga_horaria: int
    curso_id: int  # Chave estrangeira ligando a disciplina ao curso

# Dados que o FastAPI retorna para o cliente
class DisciplinaResponse(BaseModel):
    id: int
    nome: str
    carga_horaria: int
    curso_id: int
    criado_em: datetime
    alterado_em: datetime
    curso: CursoResponse
    matricula: list[MatriculaResponse] = []
    class Config:
        from_attributes = True