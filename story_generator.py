"""Main class for managing the story generation process."""

import asyncio
from typing import List, Optional
from writer import Writer
from evaluator import Evaluator

class StoryGenerator:
    def __init__(self):
        """Initialize the story generator with its components."""
        self.writer = Writer()
        self.evaluator = Evaluator()
        self.current_chapter = []
        self.current_paragraph: List[str] = []

    def load_story(self, filepath: str) -> str:
        """Load the existing story from a file."""
        with open(filepath, 'r',encoding="utf-8") as f:
            return f.read()

    def save_progress(self, filepath: str):
        """Save the current progress to a file."""
        full_text = '\n\n'.join(self.current_chapter)
        with open(filepath, 'w') as f:
            f.write(full_text)

    async def generate_paragraph(self, story_context: str, chapter_outline: str) -> str:
        """Generate a single paragraph."""
        self.current_paragraph = []
        starter_phrase = None

        while True:
            # Generate candidate sentences
            candidates = await self.writer.generate_sentences(
                story_context,
                chapter_outline,
                ' '.join(self.current_paragraph),
                starter_phrase
            )

            # Evaluate candidates
            selected_sentence, new_starter = await self.evaluator.evaluate_sentences(
                story_context,
                ' '.join(self.current_paragraph),
                candidates
            )

            if selected_sentence:
                self.current_paragraph.append(selected_sentence)
                
                # Check if we should break the paragraph
                should_break = await self.evaluator.should_break_paragraph(
                    ' '.join(self.current_paragraph),
                    selected_sentence
                )
                
                if should_break:
                    break
                    
                starter_phrase = None
            else:
                starter_phrase = new_starter

        return ' '.join(self.current_paragraph)

    async def generate_chapter(self, story_filepath: str, chapter_outline: str):
        """Generate a complete chapter with user interaction."""
        story_context = self.load_story(story_filepath)
        
        while True:
            # Generate a paragraph
            new_paragraph = await self.generate_paragraph(story_context, chapter_outline)
            
            # Show the paragraph to the user
            print("\nGenerated paragraph:")
            print(new_paragraph)
            print("\nOptions:")
            print("1. Continue to next paragraph")
            print("2. Regenerate this paragraph")
            print("3. Save and quit")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == '1':
                self.current_chapter.append(new_paragraph)
                story_context = story_context + '\n\n' + new_paragraph
            elif choice == '2':
                continue
            elif choice == '3':
                self.current_chapter.append(new_paragraph)
                self.save_progress(config.OUTPUT_FILE)
                break
            else:
                print("Invalid choice. Please try again.")
