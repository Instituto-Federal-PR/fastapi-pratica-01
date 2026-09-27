from pydantic import BaseModel
from datetime import datetime

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

    class Config:
        from_attributes = True