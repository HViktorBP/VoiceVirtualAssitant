from typing import Optional, Callable, Dict
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ConversationInitiationData
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface


class ConversationManager:
    """Simple wrapper that creates and manages a single Conversation instance.

    Callbacks should be a dict mapping the SDK callback names to callables, e.g.
      {
        'callback_agent_response': callable,
        'callback_agent_response_correction': callable,
        'callback_user_transcript': callable,
      }
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        conversation_override: Optional[dict] = None,
        callbacks: Optional[Dict[str, Callable]] = None,
    ) -> None:
        self.api_key = api_key
        self.agent_id = agent_id
        self.conversation_override = conversation_override or {}
        self.callbacks = callbacks or {}

        self.client: Optional[ElevenLabs] = None
        self.conversation: Optional[Conversation] = None

    def start(self) -> Conversation:
        """Create the ElevenLabs client and start a conversation session."""
        self.client = ElevenLabs(api_key=self.api_key)

        config = ConversationInitiationData(
            conversation_config_override=self.conversation_override,
            extra_body={},
            dynamic_variables={},
        )

        self.conversation = Conversation(
            self.client,
            self.agent_id,
            config=config,
            requires_auth=True,
            audio_interface=DefaultAudioInterface(),
            **self.callbacks,
        )

        self.conversation.start_session()
        return self.conversation

    def end(self) -> None:
        """End the conversation if it exists."""
        try:
            if self.conversation is not None:
                self.conversation.end_session()
        except Exception:
            pass
