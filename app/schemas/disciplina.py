from pydantic import BaseModel
from datetime import datetime

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
    class Config:
        from_attributes = True