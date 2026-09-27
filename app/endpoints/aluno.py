from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.curso import Curso  # Importa Curso para validar sua existência
from app.models.aluno import Aluno
from app.schemas import AlunoCreate, AlunoResponse

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)

# --- 1. CRIAR ALUNO (POST /alunos) ---
@router.post("", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(dados: AlunoCreate, db: Session = Depends(get_db)):
    # Valida se o curso informado existe?
    curso_existe = db.query(Curso).filter(Curso.id == dados.curso_id).first()
    if not curso_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Não é possível cadastrar o aluno. O curso com ID {dados.curso_id} não existe."
        )

    novo_aluno = Aluno(
        nome=dados.nome, 
        turma=dados.turma, 
        curso_id=dados.curso_id
    )
    db.add(novo_aluno)
    db.commit()
    db.refresh(novo_aluno)
    return novo_aluno

# --- 2. LISTAR TODOS OS ALUNOS (GET /alunos) ---
@router.get("", response_model=List[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).all()

# --- 3. BUSCAR UM ALUNO POR ID (GET /alunos/{aluno_id}) ---
@router.get("/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno

# --- 4. ATUALIZAR UM ALUNO (PUT /aluno/{aluno_id}) ---
@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, dados: AlunoCreate, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    # Valida se o curso_id mudou para um novo curso válido
    curso_existe = db.query(Curso).filter(Curso.id == dados.curso_id).first()
    if not curso_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Curso com ID {dados.curso_id} não existe."
        )
    
    aluno.nome = dados.nome
    aluno.carga_horaria = dados.carga_horaria
    aluno.curso_id = dados.curso_id
    
    db.commit()
    db.refresh(aluno)
    return aluno

# --- 5. DELETAR UM ALUNO (DELETE /alunos/{aluno_id}) ---
@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    db.delete(aluno)
    db.commit()
    return None