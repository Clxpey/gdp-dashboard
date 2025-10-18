from pathlib import Path
import os

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
INDEX_DIR = DATA_DIR / "index"
GMAIL_DIR = DATA_DIR / "gmail"
TMP_DIR = DATA_DIR / "tmp"

# Create directories if missing
for p in [DATA_DIR, DOCS_DIR, INDEX_DIR, GMAIL_DIR, TMP_DIR]:
    p.mkdir(parents=True, exist_ok=True)

# Embedding / Model config
DEFAULT_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "384"))  # all-MiniLM-L6-v2 dimension

# OpenAI config (optional)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Security
ENABLE_LOGIN = os.getenv("ENABLE_LOGIN", "false").lower() == "true"
APP_USERNAME = os.getenv("APP_USERNAME", "manager")
APP_PASSWORD = os.getenv("APP_PASSWORD", "manager")

# Encryption
ENABLE_ENCRYPTION_DEFAULT = os.getenv("ENABLE_ENCRYPTION_DEFAULT", "false").lower() == "true"

# Gmail
GOOGLE_CREDENTIALS_DIR = Path(os.getenv("GOOGLE_CREDENTIALS_DIR", str(BASE_DIR / "credentials")))
GOOGLE_CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
GOOGLE_CLIENT_SECRET_FILE = GOOGLE_CREDENTIALS_DIR / "client_secret.json"
GOOGLE_TOKEN_FILE = GOOGLE_CREDENTIALS_DIR / "token.json"
GMAIL_USER_ID = "me"

# Misc
MAX_TEXT_PREVIEW_CHARS = 3000
MAX_EMBED_TEXT_CHARS = 4000
