from typing import Dict
import env_loader
from conversation_manager import ConversationManager
import shutdown


def print_agent_response(response: str) -> None:
    print(f"Agent: {response}")


def print_interrupted_response(original: str, corrected: str) -> None:
    print(f"Agent interrupted, truncated response: {corrected}")


def print_user_transcript(transcript: str) -> None:
    print(f"User: {transcript}")


def main() -> None:
    env = env_loader.require_env()
    api_key = env["API_KEY"]
    agent_id = env["AGENT_ID"]

    user_name = "Viktor"
    schedule = "University from 10:00 to 14:00;Danish lesson 17:00"
    prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
    first_message = f"Hello {user_name}, how can I help you today?"

    conversation_override = {
        "agent": {
            "prompt": {"prompt": prompt},
            "first_message": first_message,
        }
    }

    callbacks: Dict[str, object] = {
        "callback_agent_response": print_agent_response,
        "callback_agent_response_correction": print_interrupted_response,
        "callback_user_transcript": print_user_transcript,
    }

    manager = ConversationManager(api_key=api_key, agent_id=agent_id, conversation_override=conversation_override, callbacks=callbacks)
    conversation = manager.start()

    shutdown.start_enter_watcher(conversation)

    try:
        conversation.wait_for_session_end()
    except Exception:
        manager.end()


if __name__ == "__main__":
    main()
