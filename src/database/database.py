import os
from contextlib import contextmanager
from typing import Dict, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Base, TextAnalysis

# Global database instance
_db = None

def init_db(db_path: str = "trades.db"):
    """Initialize the database connection."""
    global _db
    if _db is None:
        _db = Database(db_path)
    return _db

def get_db() -> 'Database':
    """Get the database instance."""
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db

def add_trade(trade_data: Dict):
    """Add a new trade to the database."""
    db = get_db()
    with db.get_session() as session:
        # Create a new TextAnalysis instance for the trade
        analysis = TextAnalysis.create_from_analysis(
            text=trade_data.get('message', ''),
            categories={
                'player_name': trade_data.get('player_name'),
                'server': trade_data.get('server'),
                'trade_type': trade_data.get('trade_type')
            },
            metadata={
                'price_amount': trade_data.get('price_amount'),
                'price_currency': trade_data.get('price_currency'),
                'items': trade_data.get('items', [])
            }
        )
        session.add(analysis)
        session.commit()
        return analysis

class Database:
    def __init__(self, db_path: str):
        """Initialize the database connection."""
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        Base.metadata.create_all(bind=self.engine)

    def __enter__(self):
        """Enter the context manager."""
        self.session = self.SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

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