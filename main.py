"""Main script to run the story generation system."""

import asyncio
from story_generator import StoryGenerator
import config

async def main():
    # Initialize the story generator
    generator = StoryGenerator()

    # Load chapter outline from file
    try:
        with open(config.CHAPTER_OUTLINE_FILE, "r", encoding="utf-8") as f:
            chapter_outline = f.read()
    except FileNotFoundError:
        print(f"Error: Chapter outline file not found at {config.CHAPTER_OUTLINE_FILE}")
        return

    # Generate the chapter
    await generator.generate_chapter(config.STORY_FILE, chapter_outline)

    print(f"\nChapter has been saved to {config.OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())