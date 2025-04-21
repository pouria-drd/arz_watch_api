from pathlib import Path
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SCRAPERS_OUTPUT_DIR = BASE_DIR / "output" / "scrapers"
SCRAPERS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
