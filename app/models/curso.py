from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Tabela de Cursos
class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    duracao = Column(Integer, nullable=False)  
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    alterado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento: Permite acessar as disciplinas de um curso
    # Ex: meu_curso.disciplinas
    disciplina = relationship("Disciplina", back_populates="curso", cascade="all, delete-orphan")
    aluno = relationship("Aluno", back_populates="curso", cascade="all, delete-orphan")