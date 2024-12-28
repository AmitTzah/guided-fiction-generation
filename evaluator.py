"""Evaluator model responsible for assessing generated sentences."""

import google.generativeai as genai
from typing import List, Tuple, Optional
import config

class Evaluator:
    def __init__(self):
        """Initialize the Evaluator model with Gemini API."""
        genai.configure(api_key=config.API_KEY)
        self.model = genai.GenerativeModel(model_name=config.MODEL_NAME)

    def _build_evaluation_prompt(self, story_context: str, current_paragraph: str, 
                               candidate_sentences: List[str]) -> str:
        """Build the prompt for sentence evaluation."""
        return config.EVALUATOR_BASE_PROMPT.format(
            story_context=story_context,
            current_paragraph=current_paragraph,
            candidate_sentences="\n".join(f"{i+1}. {sent}" 
                                        for i, sent in enumerate(candidate_sentences))
        )

    async def evaluate_sentences(self, story_context: str, current_paragraph: str, 
                               candidate_sentences: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """Evaluate candidate sentences and return the best one or a guiding phrase."""
        prompt = self._build_evaluation_prompt(story_context, current_paragraph, 
                                             candidate_sentences)
        
        response = await self.model.generate_content(prompt)
        evaluation = response.text

        # Parse the evaluation to extract the best sentence or get a guiding phrase
        # This is a simplified implementation - you might want to make it more robust
        if "none are suitable" in evaluation.lower():
            # Extract guiding phrase - this would need to be more sophisticated
            # in a production environment
            return None, "Start with something like: [extracted phrase]"
        else:
            # Extract the highest-ranked sentence
            for sent in candidate_sentences:
                if sent in evaluation and "best choice" in evaluation.lower():
                    return sent, None

        return None, "Consider describing the character's immediate reaction"

    async def should_break_paragraph(self, current_paragraph: str, 
                                   selected_sentence: str) -> bool:
        """Decide if a new paragraph should be started."""
        prompt = f"""
        Analyze this paragraph and determine if it should be broken after the last sentence.
        Consider: topic changes, dialogue shifts, and natural narrative breaks.

        Paragraph: {current_paragraph}
        Last sentence: {selected_sentence}

        Should this start a new paragraph? Answer YES or NO and explain why.
        """
        
        response = await self.model.generate_content(prompt)
        return "YES" in response.text.upper()
