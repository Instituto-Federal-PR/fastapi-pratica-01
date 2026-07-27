from fastapi import FastAPI

# Criando uma instância do FastAPI
app = FastAPI(title="Meu Primeiro App FastAPI")

# Definindo a rota principal "/"
@app.get("/")
def read_root():
    return {"mensagem": "Olá, Mundo! Framework FastAPI + Docker!"}