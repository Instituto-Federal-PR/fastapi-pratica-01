from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.aluno import Aluno
from app.models.disciplina import Disciplina
from app.models.matricula import Matricula
from app.schemas import MatriculaCreate, MatriculaResponse

router = APIRouter(
    prefix="/matriculas",
    tags=["Matriculas"]
)


# --- 1. CRIAR MATRÍCULA (POST /matriculas) ---
@router.post("", response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
async def criar_matricula(
    dados: MatriculaCreate, 
    db: AsyncSession = Depends(get_db),
):
    result_aluno = await db.execute(select(Aluno).where(Aluno.id == dados.aluno_id))
    aluno_existe = result_aluno.scalar_one_or_none()
    
    if not aluno_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Não é possível efetuar a matrícula. O aluno com ID {dados.aluno_id} não existe."
        )
    
    result_disc = await db.execute(select(Disciplina).where(Disciplina.id == dados.disciplina_id))
    disciplina_existe = result_disc.scalar_one_or_none()
    
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
    await db.commit()

    # Re-consulta carregando explicitamente tanto `aluno` quanto `disciplina`
    statement = (
        select(Matricula)
        .options(
            selectinload(Matricula.aluno),
            selectinload(Matricula.disciplina)
        )
        .where(
            Matricula.aluno_id == nova_matricula.aluno_id,
            Matricula.disciplina_id == nova_matricula.disciplina_id
        )
    )
    result = await db.execute(statement)
    return result.scalar_one()


# --- 2. LISTAR TODAS AS MATRÍCULAS (GET /matriculas) ---
@router.get("", response_model=List[MatriculaResponse])
async def listar_matriculas(
    db: AsyncSession = Depends(get_db),
):
    statement = select(Matricula).options(
        selectinload(Matricula.aluno),
        selectinload(Matricula.disciplina)
    )
    result = await db.execute(statement)
    return result.scalars().all()


# --- 3. BUSCAR UMA MATRÍCULA POR IDS (GET /matriculas/{aluno_id}/{disciplina_id}) ---
@router.get("/{aluno_id}/{disciplina_id}", response_model=MatriculaResponse)
async def buscar_matricula(
    aluno_id: int, 
    disciplina_id: int, 
    db: AsyncSession = Depends(get_db),
):
    statement = (
        select(Matricula)
        .options(
            selectinload(Matricula.aluno),
            selectinload(Matricula.disciplina)
        )
        .where(
            Matricula.aluno_id == aluno_id, 
            Matricula.disciplina_id == disciplina_id
        )
    )
    result = await db.execute(statement)
    matricula = result.scalar_one_or_none()
    
    if not matricula:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula não encontrada!")
    
    return matricula

# --- 4. DELETAR UMA MATRÍCULA (DELETE /matriculas/{aluno_id}/{disciplina_id}) ---
@router.delete("/{aluno_id}/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_matricula(
    aluno_id: int, 
    disciplina_id: int, 
    db: AsyncSession = Depends(get_db),
):
    statement = select(Matricula).where(
        Matricula.aluno_id == aluno_id,
        Matricula.disciplina_id == disciplina_id
    )
    result = await db.execute(statement)
    matricula = result.scalar_one_or_none()
    
    if not matricula:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula não encontrada")
    
    await db.delete(matricula)
    await db.commit()
    return None