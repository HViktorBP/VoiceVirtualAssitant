import os
from dotenv import load_dotenv
from typing import Dict, Optional


def load_env(path: str = ".env") -> str:
    """Load environment from the given path if it exists, otherwise fall back to default.

    Returns the path that was loaded (for diagnostics).
    """
    if os.path.exists(path):
        load_dotenv(path)
        return path
    load_dotenv()
    return ".env (or environment)"


def get_api_key() -> Optional[str]:
    return os.getenv("API_KEY") or os.getenv("XI_API_KEY") or os.getenv("ELEVEN_API_KEY")


def get_agent_id() -> Optional[str]:
    return os.getenv("AGENT_ID")


def require_env() -> Dict[str, str]:
    """Ensure required environment variables exist and return them.

    Raises RuntimeError with a helpful message if missing.
    """
    loaded = load_env()
    api_key = get_api_key()
    agent_id = get_agent_id()
    missing = []
    if not api_key:
        missing.append("API_KEY (or XI_API_KEY / ELEVEN_API_KEY)")
    if not agent_id:
        missing.append("AGENT_ID")
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}.\nLoaded from: {loaded}"
        )
    return {"API_KEY": api_key, "AGENT_ID": agent_id}
