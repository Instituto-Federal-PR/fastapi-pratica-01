from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session,  joinedload
from typing import List

from app.database import get_db
from app.models.curso import Curso  # Importa Curso para validar sua existência
from app.models.disciplina import Disciplina
from app.schemas import DisciplinaCreate, DisciplinaResponse

router = APIRouter(
    prefix="/disciplinas",
    tags=["Disciplinas"]
)

# --- 1. CRIAR DISCIPLINA (POST /disciplinas) ---
@router.post("", response_model=DisciplinaResponse, status_code=status.HTTP_201_CREATED)
def criar_disciplina(dados: DisciplinaCreate, db: Session = Depends(get_db)):
    # Valida se o curso informado existe?
    curso_existe = db.query(Curso).filter(Curso.id == dados.curso_id).first()
    if not curso_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Não é possível criar a disciplina. O curso com ID {dados.curso_id} não existe."
        )

    nova_disciplina = Disciplina(
        nome=dados.nome, 
        carga_horaria=dados.carga_horaria, 
        curso_id=dados.curso_id
    )
    db.add(nova_disciplina)
    db.commit()
    db.refresh(nova_disciplina)
    return nova_disciplina

# --- 2. LISTAR TODAS AS DISCIPLINAS (GET /disciplinas) ---
@router.get("", response_model=List[DisciplinaResponse])
def listar_disciplinas(db: Session = Depends(get_db)):
    # return db.query(Disciplina).all()
    return db.query(Disciplina).options(joinedload(Disciplina.curso)).all()

# --- 3. BUSCAR UMA DISCIPLINA POR ID (GET /disciplinas/{disciplina_id}) ---
@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def buscar_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return disciplina

# --- 4. ATUALIZAR UMA DISCIPLINA (PUT /disciplinas/{disciplina_id}) ---
@router.put("/{disciplina_id}", response_model=DisciplinaResponse)
def atualizar_disciplina(disciplina_id: int, dados: DisciplinaCreate, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    # Valida se o curso_id mudou para um novo curso válido
    curso_existe = db.query(Curso).filter(Curso.id == dados.curso_id).first()
    if not curso_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Curso com ID {dados.curso_id} não existe."
        )
    
    disciplina.nome = dados.nome
    disciplina.carga_horaria = dados.carga_horaria
    disciplina.curso_id = dados.curso_id
    
    db.commit()
    db.refresh(disciplina)
    return disciplina

# --- 5. DELETAR UMA DISCIPLINA (DELETE /disciplinas/{disciplina_id}) ---
@router.delete("/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    
    db.delete(disciplina)
    db.commit()
    return None