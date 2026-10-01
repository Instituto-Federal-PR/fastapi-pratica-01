from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.database import get_db
from app.models.curso import Curso
from app.schemas import CursoCreate, CursoResponse

router = APIRouter(
    prefix="/cursos",
    tags=["Cursos"]
)

@router.post("", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def criar_curso(curso_dados: CursoCreate, db: Session = Depends(get_db)):
    novo_curso = Curso(nome=curso_dados.nome, duracao=curso_dados.duracao)
    db.add(novo_curso)
    db.commit()
    db.refresh(novo_curso)
    return novo_curso

@router.get("", response_model=List[CursoResponse])
def listar_cursos(db: Session = Depends(get_db)):
    # return db.query(Curso).all()
    return db.query(Curso).options(joinedload(Curso.aluno)).all()

@router.get("/{curso_id}", response_model=CursoResponse)
def buscar_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return curso

@router.put("/{curso_id}", response_model=CursoResponse)
def atualizar_curso(curso_id: int, curso_dados: CursoCreate, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    curso.nome = curso_dados.nome
    curso.duracao = curso_dados.duracao
    db.commit()
    db.refresh(curso)
    return curso

@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_curso(curso_id: int, db: Session = Depends(get_db)):
    curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    db.delete(curso)
    db.commit()
    return None