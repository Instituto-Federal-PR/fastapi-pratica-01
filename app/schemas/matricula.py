from pydantic import BaseModel
from datetime import datetime

# Dados que o cliente envia ao criar uma disciplina
class MatriculaCreate(BaseModel):
    aluno_id: int  # Chave estrangeira ligando a matricula ao aluno
    disciplina_id: int  # Chave estrangeira ligando a matricula a disciplina

# Dados que o FastAPI retorna para o cliente
class MatriculaResponse(BaseModel):
    aluno_id: int
    disciplina_id: int
    criado_em: datetime
    
    class Config:
        from_attributes = True