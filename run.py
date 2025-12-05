import asyncio
import sys
import os

# Add parent directory to path for proper imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from r2d2brain.brain import main

if __name__ == "__main__":
    asyncio.run(main())
