from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.aluno import Aluno  # Importa Curso para validar sua existência
from app.models.disciplina import Disciplina
from app.models.matricula import Matricula
from app.schemas import MatriculaCreate, MatriculaResponse

router = APIRouter(
    prefix="/matriculas",
    tags=["Matriculas"]
)

# --- 1. CRIAR DISCIPLINA (POST /disciplinas) ---
@router.post("", response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
def criar_matricula(dados: MatriculaCreate, db: Session = Depends(get_db)):
    # Valida se o aluno informado existe?
    aluno_existe = db.query(Aluno).filter(Aluno.id == dados.aluno_id).first()
    if not aluno_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Não é possível efetuar a matrícula. O aluno com ID {dados.aluno_id} não existe."
        )
    
    # Valida se a disciplinas informada existe?
    disciplina_existe = db.query(Disciplina).filter(Disciplina.id == dados.disciplina_id).first()
    if not disciplina_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Não é possível efetuar a matrícula. A disciplina com ID {dados.disciplina_id} não existe."
        )

    nova_matricula = Matricula(
        aluno_id=dados.aluno_id,
        disciplina_id=dados.disciplina_id
    )
    db.add(nova_matricula)
    db.commit()
    db.refresh(nova_matricula)
    return nova_matricula

# --- 2. LISTAR TODAS AS MATRÍCULAS (GET /matriculas) ---
@router.get("", response_model=List[MatriculaResponse])
def listar_matriculas(db: Session = Depends(get_db)):
    #return db.query(Matricula).all()
    return db.query(Matricula).options(joinedload(Matricula.aluno)).all()

# --- 3. BUSCAR UMA MATRÍCULA POR IDS (GET /matriculas/{aluno_id}/{disciplina_id}) ---
@router.get("/{aluno_id}/{disciplina_id}", response_model=MatriculaResponse)
def buscar_matricula(aluno_id: int, disciplina_id: int, db: Session = Depends(get_db)):
    matricula = db.query(Matricula).filter(
        Matricula.aluno_id == aluno_id, 
        Matricula.disciplina_id == disciplina_id
    ).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada!")
    
    return matricula

# --- 4. DELETAR UMA MATRÍCULA (DELETE /matricula/{aluno_id}/{disciplina_id}) ---
@router.delete("/{aluno_id}/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_disciplina(aluno_id: int, disciplina_id: int, db: Session = Depends(get_db)):
    matricula = db.query(Disciplina).filter(
        Matricula.aluno_id == aluno_id,
        Matricula.disciplina_id == disciplina_id
    ).first()
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    
    db.delete(matricula)
    db.commit()
    return None