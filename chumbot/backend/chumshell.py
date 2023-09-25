"""Defines an interactive shell for Chumbot."""

# Disable unused argument warning
# pylint:disable=W0613

from cmd import Cmd

from chumbot import client_interface


class ChumShell(Cmd):
    """Implementation of interactive shell for Chumbot."""

    intro = "Type 'help' to display commands."
    prompt = 'chumbot> '

    def do_connect(self, arg):
        """Connect the Chumbot to the server."""
        client_interface.connect()

    def do_disconnect(self, arg):
        """Disconnect the Chumbot client from the server."""
        client_interface.disconnect()

    def do_reconnect(self, arg):
        """Reconnect the Chumbot client."""
        client_interface.reconnect()

    def do_users(self, arg):
        """Print a display of the users and the channels they occupy."""
        client_interface.print_users()

    def do_move(self, arg):
        """Move the Chumbot client to another Mumble channel."""
        client_interface.move_to_channel(arg)

    def do_mute(self, arg):
        """Mute the Chumbot client."""
        client_interface.mute_self()

    def do_unmute(self, arg):
        """Unmute the Chumbot client."""
        client_interface.unmute_self()

    def do_play(self, arg):
        """Play sound clips in Mumble given a comma-separated list of their extensionless names."""
        client_interface.play_clips(arg)

    def do_random(self, arg):
        """Play a random sound clip in Mumble and list its name."""
        client_interface.play_random()

    def do_list(self, arg):
        """List all clips loaded into Chumbot."""
        client_interface.list_clips()

    def do_search(self, arg):
        """Search for a clip loaded into Chumbot."""
        client_interface.search_clips(arg)

    def do_reload(self, arg):
        """Reload the stored sound clips."""
        client_interface.reload_clips()

    def do_automove(self, arg):
        """Enable or disable auto-move into most populous Mumble channel."""
        client_interface.automove(arg)

    def do_quit(self, arg):
        """Exit the Chumbot command-line interface."""
        client_interface.disconnect()
        return True

    do_exit = do_quit
    do_EOF = do_quit
