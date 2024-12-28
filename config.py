"""Configuration settings for the story generation system."""

# Gemini API settings
API_KEY = "YOUR_API_KEY"  # Replace with actual API key
MODEL_NAME = "gemini-exp-1206"

# Generation settings
CANDIDATE_COUNT = 3  # Number of candidate sentences to generate
MAX_OUTPUT_TOKENS = 100  # Maximum length of generated sentences
TEMPERATURE = 0.7  # Controls randomness in generation

# File paths
STORY_FILE = "story.txt"  # File containing the existing story
OUTPUT_FILE = "next_chapter.txt"  # File to save the generated chapter

# System prompts
WRITER_BASE_PROMPT = """
You are a creative writer tasked with continuing a story. Generate the next sentence that:
- Maintains consistent point-of-view
- Avoids common AI writing pitfalls and clichés
- Flows naturally from the previous content
- Advances the story meaningfully

Story context: {story_context}
Chapter outline: {chapter_outline}
Current paragraph: {current_paragraph}
{starter_phrase}

Generate the next sentence:"""

EVALUATOR_BASE_PROMPT = """
You are a literary critic evaluating sentences for a story. Analyze these candidate sentences:

Story context: {story_context}
Current paragraph: {current_paragraph}
Candidate sentences:
{candidate_sentences}

Evaluate each sentence based on:
1. Human-like quality and naturalness
2. Avoidance of AI writing patterns
3. Pacing and flow
4. POV consistency
5. Contribution to the story

Rank the sentences and explain your reasoning. If none are suitable, provide a guiding phrase for the next attempt."""
