import os
from typing import Dict, List, Optional
import anthropic
from anthropic.types import Message
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

class ClaudeClient:
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-7-sonnet"):
        """Initialize the Claude client."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)

    async def analyze_text(
        self,
        text: str,
        categories: List[str],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict:
        """
        Analyze text using Claude and return categorized results.
        
        Args:
            text: The text to analyze
            categories: List of categories to analyze
            system_prompt: Optional custom system prompt
            temperature: Model temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dict containing the analysis results
        """
        try:
            # Construct the prompt
            prompt = f"""Please analyze the following text and categorize it according to these categories: {', '.join(categories)}

Text to analyze:
{text}

Please provide your analysis in the following JSON format:
{{
    "categories": {{
        "category_name": "analysis_result"
    }},
    "confidence_scores": {{
        "category_name": 0.0 to 1.0
    }},
    "metadata": {{
        "analysis_timestamp": "ISO timestamp",
        "model_used": "{self.model}"
    }}
}}"""

            # Make the API call
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt or "You are a text analysis assistant that provides structured analysis in JSON format.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Parse the response
            try:
                response_text = message.content[0].text
                analysis_result = json.loads(response_text)
                return analysis_result
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse Claude response as JSON: {e}")
                raise ValueError("Invalid response format from Claude")

        except Exception as e:
            logger.error(f"Error in Claude API call: {e}")
            raise

    async def batch_analyze(
        self,
        texts: List[str],
        categories: List[str],
        batch_size: int = 10
    ) -> List[Dict]:
        """
        Analyze multiple texts in batches.
        
        Args:
            texts: List of texts to analyze
            categories: List of categories to analyze
            batch_size: Number of texts to process in parallel
            
        Returns:
            List of analysis results
        """
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[self.analyze_text(text, categories) for text in batch]
            )
            results.extend(batch_results)
        return results 