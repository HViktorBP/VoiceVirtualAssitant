import threading
import os
from typing import Optional


def start_enter_watcher(conversation_obj: Optional[object]) -> threading.Thread:
    """Start a background daemon thread that waits for Enter and then ends the conversation and exits.

    Returns the Thread object.
    """
    def _wait():
        try:
            input("Press Enter to terminate the session\n")
        except Exception:
            pass
        try:
            if conversation_obj is not None:
                conversation_obj.end_session()
        except Exception:
            pass
        try:
            os._exit(0)
        except Exception:
            pass

    t = threading.Thread(target=_wait, daemon=True)
    t.start()
    return t
