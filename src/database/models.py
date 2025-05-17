from datetime import datetime
from typing import Dict, List, Optional
from sqlalchemy import Column, DateTime, Integer, JSON, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class TextAnalysis(Base):
    __tablename__ = "text_analyses"

    id = Column(Integer, primary_key=True)
    text_content = Column(String, nullable=False)
    categories = Column(JSON, nullable=False)  # Stores the categorization results
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, nullable=True)  # Additional metadata about the analysis

    def __repr__(self):
        return f"<TextAnalysis(id={self.id}, created_at={self.created_at})>"

    @classmethod
    def create_from_analysis(cls, text: str, categories: Dict, metadata: Optional[Dict] = None):
        """Create a new TextAnalysis instance from analysis results."""
        return cls(
            text_content=text,
            categories=categories,
            metadata=metadata or {}
        )

    def to_dict(self) -> Dict:
        """Convert the instance to a dictionary."""
        return {
            "id": self.id,
            "text_content": self.text_content,
            "categories": self.categories,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "metadata": self.metadata
        } 