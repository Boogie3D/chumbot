"""Defines constants for types of Mumble events."""

# Convert a WAV file to PCM
CONVERT_COMMAND = ['ffmpeg', '-i', '-', '-acodec', 'pcm_s16le',
                   '-ar', '48000', '-ac', '1', '-f', 's32le', '-']

# Name of Mumble config file
MUMBLE_CONFIG = '~/.config/chumbot.ini'

# Extension of sound clip files
SOUND_FILE_EXTENSION = '.mp3'

# Maximum clips that can be played in a row
MAXIMUM_CLIP_LIST_SIZE = 10

# The size of each partition of the clips list
CLIPS_PARTITION_SIZE = 50
