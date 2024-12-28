"""Main script to run the story generation system."""

import asyncio
from story_generator import StoryGenerator
import config

async def main():
    # Initialize the story generator
    generator = StoryGenerator()
    
    # Get chapter outline from user
    print("Please enter the outline for the next chapter:")
    chapter_outline = input("> ")
    
    # Generate the chapter
    await generator.generate_chapter(config.STORY_FILE, chapter_outline)
    
    print(f"\nChapter has been saved to {config.OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
