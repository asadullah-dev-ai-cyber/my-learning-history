import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_BASE_URL = "https://api.github.com"
    USER_AGENT = "DevInsight-App"
    REQUEST_TIMEOUT = 10  # seconds
    MAX_REPOS_PER_PAGE = 100
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", None)