import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env", override=True)

API_KEY = os.environ["ANTHROPIC_API_KEY"]
BASE_URL = os.environ["ANTHROPIC_BASE_URL"]
MODEL = "glm-4.7"