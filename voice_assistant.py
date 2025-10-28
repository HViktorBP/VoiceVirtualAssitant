import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ConversationInitiationData
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import signal
import atexit
import sys
import ctypes
import threading

load_dotenv("access.env")
if os.path.exists("access.env"):
    load_dotenv("access.env")
else:
    load_dotenv()
AGENT_ID = os.getenv("AGENT_ID")
API_KEY = os.getenv("API_KEY")
API_KEY = (
    os.getenv("API_KEY")
    or os.getenv("XI_API_KEY")
    or os.getenv("ELEVEN_API_KEY")
)
user_name = "Viktor"
if not API_KEY:
    raise RuntimeError(
        "Missing ElevenLabs API key. Set API_KEY or XI_API_KEY (in access.env or environment)."
    )
schedule = "University from 10:00 to 14:00;Danish lesson 17:00"
prompt = f"You are a helpful assistant. Your interlocutor has the following schedule: {schedule}."
first_message = f"Hello {user_name}, how can I help you today?"

conversation_override = {
  "agent": {
    "prompt": {
      "prompt": prompt,
    },
    "first_message": first_message,
  },
}

config = ConversationInitiationData(
    conversation_config_override=conversation_override,
    extra_body={},
    dynamic_variables={},
)

client = ElevenLabs(api_key=API_KEY)

conversation = Conversation(
  client,
  AGENT_ID,
  config=config,
  requires_auth=True,
  audio_interface=DefaultAudioInterface(),
)

def print_agent_response(response):
  print(f"Agent: {response}")

def print_interrupted_response(original, corrected):
  print(f"Agent interrupted, truncated response: {corrected}")

def print_user_transcript(transcript):
  print(f"User: {transcript}")


conversation = Conversation(
  client,
  AGENT_ID,
  config=config,
  requires_auth=True,
  audio_interface=DefaultAudioInterface(),
  callback_agent_response=print_agent_response,
  callback_agent_response_correction=print_interrupted_response,
  callback_user_transcript=print_user_transcript,
)


def _shutdown_and_exit(*args, **kwargs):
  try:
    if 'conversation' in globals() and conversation is not None:
      conversation.end_session()
  except Exception:
    pass
  try:
    sys.exit(0)
  except SystemExit:
    raise

try:
  signal.signal(signal.SIGINT, lambda s, f: _shutdown_and_exit())
except Exception:
  pass
try:
  signal.signal(signal.SIGTERM, lambda s, f: _shutdown_and_exit())
except Exception:
  pass
if hasattr(signal, 'SIGBREAK'):
  try:
    signal.signal(signal.SIGBREAK, lambda s, f: _shutdown_and_exit())
  except Exception:
    pass

atexit.register(_shutdown_and_exit)

if os.name == 'nt':
  try:
    HandlerRoutine = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_uint)

    def _console_ctrl_handler(ctrl_type):
      if ctrl_type in (0, 1, 2, 5, 6):
        _shutdown_and_exit()
        return True
      return False

    ctypes.windll.kernel32.SetConsoleCtrlHandler(HandlerRoutine(_console_ctrl_handler), True)
  except Exception:
    pass


conversation.start_session()

def _enter_shutdown():
  try:
    if 'conversation' in globals() and conversation is not None:
      conversation.end_session()
  except Exception:
    pass
  try:
    os._exit(0)
  except Exception:
    pass

def _wait_for_enter_and_shutdown():
  try:
    input("If you want to terminate the session, press Enter\n")
  except Exception:
    pass
  _enter_shutdown()

# Start a background thread that will exit when Enter is pressed
threading.Thread(target=_wait_for_enter_and_shutdown, daemon=True).start()