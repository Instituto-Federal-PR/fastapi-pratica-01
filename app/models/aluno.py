from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Tabela de Cursos
class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    turma = Column(Integer, nullable=False)
    
    # Chave Estrangeira: Aponta para o ID da tabela cursos
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False)
    
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    alterado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento Reverso: Permite saber a qual curso o aluno pertence.
    # Ex: meu_aluno.curso
    curso = relationship("Curso", back_populates="aluno")
    matricula = relationship("Matricula", back_populates="aluno")