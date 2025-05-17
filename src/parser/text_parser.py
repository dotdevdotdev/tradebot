import asyncio
import logging
from typing import Dict, List, Optional, Union
import yaml
from pathlib import Path

from .claude_client import ClaudeClient
from ..database.database import Database

logger = logging.getLogger(__name__)

class TextParser:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the text parser with configuration."""
        self.config = self._load_config(config_path)
        self.claude_client = ClaudeClient(
            model=self.config["anthropic"]["model"]
        )
        self.db = Database(self.config["database"]["path"])
        self.categories = self.config["parser"]["default_categories"]

    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        
        try:
            with open(config_path, "r") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            raise

    def set_categories(self, categories: List[str]):
        """Set custom categories for analysis."""
        self.categories = categories

    async def process_text(
        self,
        text: str,
        custom_instructions: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Process a single text and store results in the database.
        
        Args:
            text: The text to analyze
            custom_instructions: Optional custom instructions for Claude
            metadata: Optional metadata to store with the analysis
            
        Returns:
            Dict containing the analysis results
        """
        try:
            # Analyze text with Claude
            analysis_result = await self.claude_client.analyze_text(
                text=text,
                categories=self.categories,
                system_prompt=custom_instructions or self.config["anthropic"]["system_prompt"],
                temperature=self.config["anthropic"]["temperature"],
                max_tokens=self.config["anthropic"]["max_tokens"]
            )

            # Store results in database
            stored_analysis = self.db.store_analysis(
                text=text,
                categories=analysis_result["categories"],
                metadata={
                    **(metadata or {}),
                    "confidence_scores": analysis_result["confidence_scores"],
                    "analysis_metadata": analysis_result["metadata"]
                }
            )

            return stored_analysis.to_dict()

        except Exception as e:
            logger.error(f"Error processing text: {e}")
            raise

    async def process_batch(
        self,
        texts: List[str],
        custom_instructions: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Process multiple texts in parallel.
        
        Args:
            texts: List of texts to analyze
            custom_instructions: Optional custom instructions for Claude
            metadata: Optional metadata to store with each analysis
            
        Returns:
            List of analysis results
        """
        try:
            # Process texts in batches
            results = await self.claude_client.batch_analyze(
                texts=texts,
                categories=self.categories,
                batch_size=self.config["parser"]["batch_size"]
            )

            # Store results in database
            stored_analyses = []
            for text, analysis in zip(texts, results):
                stored = self.db.store_analysis(
                    text=text,
                    categories=analysis["categories"],
                    metadata={
                        **(metadata or {}),
                        "confidence_scores": analysis["confidence_scores"],
                        "analysis_metadata": analysis["metadata"]
                    }
                )
                stored_analyses.append(stored.to_dict())

            return stored_analyses

        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            raise

    def get_analysis(self, analysis_id: int) -> Optional[Dict]:
        """Retrieve a stored analysis by ID."""
        analysis = self.db.get_analysis(analysis_id)
        return analysis.to_dict() if analysis else None

    def search_analyses(self, query: str) -> List[Dict]:
        """Search stored analyses by content."""
        analyses = self.db.search_analyses(query)
        return [analysis.to_dict() for analysis in analyses]

    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """Get the most recent analyses."""
        analyses = self.db.get_recent_analyses(limit)
        return [analysis.to_dict() for analysis in analyses] 