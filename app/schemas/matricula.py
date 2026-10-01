from pydantic import BaseModel
from datetime import datetime

class AlunoResponse(BaseModel):
    id: int
    nome: str
    turma: int
    curso_id: int
    class Config:
        from_attributes = True
class DisciplinaResponse(BaseModel):
    id: int
    nome: str
    carga_horaria: int
    curso_id: int
    class Config:
        from_attributes = True

# Dados que o cliente envia ao criar uma disciplina
class MatriculaCreate(BaseModel):
    aluno_id: int  # Chave estrangeira ligando a matricula ao aluno
    disciplina_id: int  # Chave estrangeira ligando a matricula a disciplina

# Dados que o FastAPI retorna para o cliente
class MatriculaResponse(BaseModel):
    aluno_id: int
    disciplina_id: int
    criado_em: datetime
    aluno: AlunoResponse
    disciplina: DisciplinaResponse
    class Config:
        from_attributes = True