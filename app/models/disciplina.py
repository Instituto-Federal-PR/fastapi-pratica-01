from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# Tabela de Disciplinas
class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    
    # Chave Estrangeira: Aponta para o ID da tabela cursos
    curso_id = Column(Integer, ForeignKey("cursos.id", ondelete="CASCADE"), nullable=False)
    
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    alterado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamento Reverso: Permite saber a qual curso a disciplina pertence.
    # Ex: minha_disciplina.curso
    curso = relationship("Curso", back_populates="disciplina")
    matricula = relationship("Matricula", back_populates="disciplina")