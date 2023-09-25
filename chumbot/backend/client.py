"""Defines a data structure for a Mumble client."""
import configparser
from os.path import expanduser, join
from random import choice
import subprocess as sp
from threading import Thread

import pymumble_py3 as pymumble

from chumbot.backend.clips import Clips
from chumbot.backend import constants

_CONFIG = configparser.ConfigParser()
_CONFIG.read(expanduser(constants.MUMBLE_CONFIG))

_CLIP_DIRECTORY = _CONFIG['clips']['ClipDir']
_LINK_POSTED_CLIP = _CONFIG['clips']['LinkPostedClipName']
_USER_JOINED_CLIP_DEFAULT = _CONFIG['clips']['UserJoinedClipName']
_USER_LEFT_CLIP_DEFAULT = _CONFIG['clips']['UserLeftClipName']

_USER_JOINED_CLIPS_CUSTOM = {}
if _CONFIG.has_section('join'):
    _USER_JOINED_CLIPS_CUSTOM = dict(_CONFIG['join'].items())

_USER_LEFT_CLIPS_CUSTOM = {}
if _CONFIG.has_section('disconnect'):
    _USER_LEFT_CLIPS_CUSTOM = dict(_CONFIG['disconnect'].items())

class Client:
    """A class for managing a Mumble client."""

    def __init__(self, username, host, port, password, debug):
        """Create a new Mumble client for a given server host.

        The default values of the parameters are read from mumble.cfg.

        :param username: the client username
        :type username: str
        :param host: the hostname of the Mumble server
        :type host: str
        :param port: the Mumble server port number
        :type port: int
        :param password: the Mumble host password
        :type password: str
        :param debug: enable or disable debug mode
        :type debug: bool
        """
        self._username = username
        self._host = host
        self._port = port
        self._password = password
        self._debug = debug

        self._running = False
        self._connected = False
        self._muted = False
        self._last_message_time = 0

        self._clips = Clips(_CLIP_DIRECTORY, constants.SOUND_FILE_EXTENSION)

        self._mumble = None
        self._channel_poll = None
        self._automove = True

        self._initialize_client()

    def connect(self):
        """Connect to the Mumble host specified at initialization."""
        if not self._connected:
            if not self._running:
                self._mumble.start()
                self._running = True
            else:
                self._initialize_client()
                self._mumble.start()
            self._mumble.is_ready()
            self._connected = True
            if self._automove:
                self._channel_poll.start()

    def disconnect(self):
        """Disconnect from the Mumble host if connected.

        Kills the Mumble thread. Must be remade to reconnect.
        """
        if self._connected:
            self._mumble.connected = pymumble.constants.PYMUMBLE_CONN_STATE_NOT_CONNECTED
            self._mumble.control_socket.close()
            self._mumble.join()
            self._connected = False
            if self._channel_poll.is_alive():
                self._channel_poll.join()

    def reconnect(self):
        """Disconnect and reconnect to the Mumble host."""
        if self._connected:
            self.disconnect()
            self.connect()

    def print_users(self):
        """Print a display of the Mumble users and the channels they occupy."""
        if self._connected:
            for channel in self._mumble.channels.values():
                users = channel.get_users()
                if users:
                    print(channel['name'] + ':')
                    for user in users:
                        print('  ', user['name'])

    def move_to_channel(self, channel):
        """Move to another Mumble channel.

        :param channel: the Mumble channel to which to move
        :type channel: string
        """
        if self._connected:
            try:
                target_channel = self._mumble.channels.find_by_name(channel)
                if target_channel != self._mumble.my_channel():
                    target_channel.move_in()
            except pymumble.errors.UnknownChannelError:
                print('No such channel: ' + channel)

    def mute_self(self):
        """Mute the Mumble client in the server."""
        if self._connected and not self._muted:
            self._mumble.users.myself.mute()
            self._muted = True

    def unmute_self(self):
        """Unmute the Mumble client in the server."""
        if self._connected and self._muted:
            self._mumble.users.myself.unmute()
            self._muted = False

    def play_clips(self, sound_clips):
        """Play sound clips in the Mumble server.

        Sound files must match the audio file format specified in chumbot.cfg and must be
        located in the clip directory specified in chumbot.cfg.
        Multiple clips can be played in a row if names separated by commas.

        :param sound_clips: the extensionless names of the sound clips, separated by commas
        :type sound_clips: str
        """
        if self._connected:
            clip_list = sound_clips.split(',')[:constants.MAXIMUM_CLIP_LIST_SIZE]
            for sound_clip in clip_list:
                sound_clip = sound_clip.lower().strip().replace(' ', '_')
                if sound_clip == '*':
                    sound_clip = choice(list(self._clips.keys()))
                if sound_clip in self._clips:
                    audio_file = self._clips[sound_clip]
                    pcm = _convert_audio_to_pcm(audio_file)
                    self._mumble.sound_output.add_sound(pcm)

    def play_random(self):
        """Play a random sound clip in the Mumble server and list its name."""
        if self._connected:
            sound_clip = choice(list(self._clips.keys()))
            self._mumble.my_channel().send_text_message(sound_clip)
            audio_file = self._clips[sound_clip]
            pcm = _convert_audio_to_pcm(audio_file)
            self._mumble.sound_output.add_sound(pcm)

    def list_clips(self):
        """Send a message to the current channel listing all sound clips."""
        if self._connected:
            clips = sorted(clip for clip in self._clips if not clip.startswith('_'))
            for part_clips in _partition(clips, constants.CLIPS_PARTITION_SIZE):
                self._mumble.my_channel().send_text_message("<br/>" + "<br/>".join(part_clips))

    def search_clips(self, clip_name):
        """Search for clips and send a message to the current channel listing all partial matches.

        :param clip_name: the name of the clip to search for
        :type clip_name: string
        """
        clip_name = clip_name.lower().strip().replace(' ', '_')
        if self._connected:
            results = sorted(clip for clip in self._clips if not clip.startswith('_')
                             and clip.find(clip_name) != -1)
            for part_clips in _partition(results, constants.CLIPS_PARTITION_SIZE):
                self._mumble.my_channel().send_text_message("<br/>" + "<br/>".join(part_clips))

    def reload_clips(self):
        """Reload the stored sound clips."""
        self._clips.reload()

    def enable_automove(self):
        """Enable automove to most populated channel."""
        self._automove = True
        if self._connected and not self._channel_poll.is_alive():
            self._channel_poll.start()

    def disable_automove(self):
        """Disable automove to most populated channel."""
        self._automove = False

    def _initialize_client(self):
        """Initialize the mumble client.

        Creates a new Mumble client thread and adds the text message callback.
        Also creates a thread for channel population polling.
        """
        self._mumble = pymumble.Mumble(self._host, self._username, self._port, self._password,
                                       debug=self._debug)
        # Add 'text received' callback
        self._mumble.callbacks.add_callback(pymumble.constants.PYMUMBLE_CLBK_TEXTMESSAGERECEIVED,
                                            self._read_message)

        self._channel_poll = Thread(target=self._channel_population_poll)

    def _read_message(self, message_obj):
        """Read a message sent by a user.

        :param message: the message sent by the user
        :type message: pymumble.mumble_pb2.TextMessage
        """
        message = message_obj.message
        if message.startswith('<a href=') or message.startswith('<img src='):
            self.play_clips(_LINK_POSTED_CLIP)
        elif message.lower().strip() == 'list':
            self.list_clips()
        elif message == '*':
            self.play_random()
        elif message.startswith('?'):
            self.search_clips(message[1:])
        else:
            self.play_clips(message)

    def _channel_population_poll(self):
        """Poll Mumble channel population.
        
        Automove to most populous channel when automove enabled.
        Play sound clip when a user joins or leaves a channel.
        """
        def get_channel_users():
            return {user['name'].lower()
                    for user in self._mumble.my_channel().get_users()}

        if self._connected:
            old_channel_users = get_channel_users()

        while self._connected:
            try:
                if self._automove:
                    most_populous_channel = max(self._mumble.channels.values(),
                                                key=lambda c: len(c.get_users()))

                    if most_populous_channel != self._mumble.my_channel():
                        most_populous_channel.move_in()
                        old_channel_users = get_channel_users()

                # play join clip if user joins channel
                cur_channel_users = get_channel_users()
                if len(cur_channel_users) > len(old_channel_users):
                    channel_diff = list(cur_channel_users - old_channel_users)
                    joined_user = channel_diff[0]
                    user_joined_clip = _USER_JOINED_CLIPS_CUSTOM.get(joined_user, _USER_JOINED_CLIP_DEFAULT)
                    self.play_clips(user_joined_clip)
                    old_channel_users = cur_channel_users
                # play leave clip if user leaves channel
                elif len(cur_channel_users) < len(old_channel_users):
                    channel_diff = list(old_channel_users - cur_channel_users)
                    left_user = channel_diff[0]
                    user_left_clip = _USER_LEFT_CLIPS_CUSTOM.get(left_user, _USER_LEFT_CLIP_DEFAULT)
                    self.play_clips(user_left_clip)
                    old_channel_users = cur_channel_users
            except RuntimeError:
                # ignore errors when user (dis)connects
                pass


def _partition(lst, size):
    """Yield successive n-sized chunks from a list."""
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


def _convert_audio_to_pcm(audio_filename):
    """Convert an audio file's contents to .PCM format.

    :param audio_filename: the name of the audio file to convert
    :type audio_filename: string
    """
    with open(expanduser(join(_CLIP_DIRECTORY, audio_filename)), 'rb') as audio_file:
        with sp.Popen(constants.CONVERT_COMMAND, stdout=sp.PIPE,
                      stderr=sp.DEVNULL, stdin=audio_file) as process:
            pcm = process.stdout.read()

    return pcm
