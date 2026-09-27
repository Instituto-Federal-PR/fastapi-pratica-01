from fastapi import FastAPI
from app.endpoints import aluno_router
from app.endpoints import curso_router
from app.endpoints import disciplina_router
from app.endpoints import matricula_router

app = FastAPI(
    title="Sistema Acadêmico - Modular",
    description="API para gerenciamento de cursos e disciplinas",
    version="1.0.0"
)

app.include_router(aluno_router)
app.include_router(curso_router)
app.include_router(disciplina_router)
app.include_router(matricula_router)

# Definindo a rota principal "/"
@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API do Sistema Acadêmico!"}