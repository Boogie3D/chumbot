"""Interface for managing the Chumbot Mumble client."""
from chumbot.backend.client import Client

_CLIENT = None


def initialize(username, host, port, password, debug=False):
    """Initialize the Chumbot client."""
    global _CLIENT
    _CLIENT = Client(username, host, port, password, debug)


def connect():
    """Connect the Chumbot to the server."""
    if _CLIENT:
        _CLIENT.connect()


def disconnect():
    """Disconnect the Chumbot client from the server."""
    if _CLIENT:
        _CLIENT.disconnect()


def reconnect():
    """Reconnect the Chumbot client."""
    if _CLIENT:
        _CLIENT.reconnect()


def print_users():
    """Print a display of the users and the channels they occupy."""
    if _CLIENT:
        return _CLIENT.print_users()

    return None


def move_to_channel(channel):
    """Move the Chumbot client to another Mumble channel.

    :param channel: the Mumble channel to which to move
    :type channel: str
    """
    if _CLIENT:
        _CLIENT.move_to_channel(channel)


def mute_self():
    """Mute the Chumbot client."""
    if _CLIENT:
        _CLIENT.mute_self()


def unmute_self():
    """Unmute the Chumbot client."""
    if _CLIENT:
        _CLIENT.unmute_self()


def play_clips(sound_clips):
    """Play sound clips given a comma-separated list of their names.

    :param sound_clips: the (extensionless) names of the sound clips, separated by commas
    :type sound_clips: str
    """
    if _CLIENT:
        _CLIENT.play_clips(sound_clips)


def play_random():
    """Play a random sound clip in Mumble and list its name."""
    if _CLIENT:
        _CLIENT.play_random()


def list_clips():
    """List all clips loaded into Chumbot."""
    if _CLIENT:
        _CLIENT.list_clips()


def search_clips(clip_name):
    """Search for a clip loaded into Chumbot, listing all partial matches.

    :param clip_name: the name of the clip to search for
    :type clip_name: str
    """
    if _CLIENT:
        _CLIENT.search_clips(clip_name)


def reload_clips():
    """Reload the stored sound clips."""
    if _CLIENT:
        _CLIENT.reload_clips()


def automove(action):
    """Enable or disable Chumbot auto-move.

    :param action: 'on' or 1 to turn on, 'off' or 0 to turn off
    :type action: str
    """
    if _CLIENT:
        action = action.lower()
        if action in ('on', '1'):
            _CLIENT.enable_automove()
        elif action in ('off', '0'):
            _CLIENT.disable_automove()
