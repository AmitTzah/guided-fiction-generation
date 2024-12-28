"""Writer model responsible for generating candidate sentences."""

import google.generativeai as genai
from typing import List, Optional
import config

class Writer:
    def __init__(self):
        """Initialize the Writer model with Gemini API."""
        genai.configure(api_key=config.API_KEY)
        self.model = genai.GenerativeModel(model_name=config.MODEL_NAME)

    def _build_prompt(self, story_context: str, chapter_outline: str, 
                     current_paragraph: str, starter_phrase: Optional[str] = None) -> str:
        """Build the prompt for sentence generation."""
        return config.WRITER_BASE_PROMPT.format(
            story_context=story_context,
            chapter_outline=chapter_outline,
            current_paragraph=current_paragraph,
            starter_phrase=f"Start with: {starter_phrase}" if starter_phrase else ""
        )

    async def generate_sentences(self, story_context: str, chapter_outline: str, 
                               current_paragraph: str, starter_phrase: Optional[str] = None) -> List[str]:
        """Generate multiple candidate sentences."""
        prompt = self._build_prompt(story_context, chapter_outline, 
                                  current_paragraph, starter_phrase)
        
        candidates = []
        for _ in range(config.CANDIDATE_COUNT):
            response = await self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=config.MAX_OUTPUT_TOKENS,
                    temperature=config.TEMPERATURE,
                )
            )
            candidates.append(response.text.strip())
        
        return candidates
