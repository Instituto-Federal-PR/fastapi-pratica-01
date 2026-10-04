from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Tabela de Matrículas
class Matricula(Base):
    
    __tablename__ = "matriculas"

    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), primary_key=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id", ondelete="CASCADE"), primary_key=True)
    
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    aluno = relationship("Aluno", back_populates="matricula")
    disciplina = relationship("Disciplina", back_populates="matricula")