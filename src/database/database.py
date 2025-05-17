import os
from contextlib import contextmanager
from typing import Dict, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Base, TextAnalysis

class Database:
    def __init__(self, db_path: str):
        """Initialize the database connection."""
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        Base.metadata.create_all(bind=self.engine)

    @contextmanager
    def get_session(self) -> Session:
        """Get a database session."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def store_analysis(self, text: str, categories: Dict, metadata: Optional[Dict] = None) -> TextAnalysis:
        """Store a new text analysis in the database."""
        with self.get_session() as session:
            analysis = TextAnalysis.create_from_analysis(text, categories, metadata)
            session.add(analysis)
            session.commit()
            session.refresh(analysis)
            return analysis

    def get_analysis(self, analysis_id: int) -> Optional[TextAnalysis]:
        """Retrieve a text analysis by ID."""
        with self.get_session() as session:
            return session.query(TextAnalysis).filter(TextAnalysis.id == analysis_id).first()

    def get_recent_analyses(self, limit: int = 10) -> List[TextAnalysis]:
        """Get the most recent text analyses."""
        with self.get_session() as session:
            return session.query(TextAnalysis).order_by(TextAnalysis.created_at.desc()).limit(limit).all()

    def search_analyses(self, query: str) -> List[TextAnalysis]:
        """Search text analyses by content."""
        with self.get_session() as session:
            return session.query(TextAnalysis).filter(
                TextAnalysis.text_content.ilike(f"%{query}%")
            ).all()

    def backup_database(self, backup_path: str):
        """Create a backup of the database."""
        import shutil
        try:
            shutil.copy2(self.engine.url.database, backup_path)
        except Exception as e:
            raise SQLAlchemyError(f"Failed to backup database: {str(e)}") 