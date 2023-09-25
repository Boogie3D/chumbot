# Chumbot
The Conveying Harmonies Unto Mumble Bot, or Chumbot, is a Mumble soundboard and notification bot
written in Python 3. Chumbot relies on the [PYMUMBLE](https://pypi.org/project/pymumble/) API,
and requires `libopus` and `ffmpeg` to be available on the host machine.

Chumbot is currently not supported on Windows.

## Installation
### For users
The Chumbot client can be installed via [pip](https://pypi.org/project/chumbot/):

`pip install chumbot`

### For developers
Chumbot can be installed for development by first installing [Poetry](https://python-poetry.org/docs/) and running
the following command within the project directory:

`poetry install`

## Usage
The Chumbot interactive shell is run from the command line. Audio clips should be stored in mp3 format.
```
usage: chumbot [-h] [-u USERNAME] [-H HOST] [-P PORT] [-p PASSWORD] [-d]

Chumbot command-line interface

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        specify Chumbot's username
  -H HOST, --host HOST  specify the Mumble host address
  -P PORT, --port PORT  specify the Mumble host port
  -p PASSWORD, --password PASSWORD
                        specify the Mumble host password
  -d, --debug           enable debug message printing
```

Once connected, Chumbot's default behavior is to move to the channel with the most users. Chumbot can be moved manually
by turning off auto-move and using the `move` command from the interactive shell. (See the
[ChumShell](https://github.com/Boogie3D/chumbot/blob/main/chumbot/backend/chumshell.py) for a list of all commands.)

Mumble users can interact with Chumbot by simply typing the names of audio clips (no extension) into the Mumble text chat.
Multiple clips can be queued sequentially by typing them comma (`,`)-separated (white-space does not matter). Up to 10 clips can
be queued at once, by default. Typing a `*` character will play a random sound. If only one random sound is played, the name
of that sound clip will be displayed in Mumble text chat.

Mumble users can type `list` into Mumble chat to make Chumbot print the list of all clips into Mumble chat, broken up into segments of up to 50 clips per message, by default, due
to character limits. Users can type `?string` to display a list of all sound clips containing `string` in text chat.

## Configuration
Chumbot configuration is stored in `~/.config/chumbot.ini`. Chumbot must be configured to know where
audio files are stored.

Chumbot can be configured to play a specific clip when a link or image is posted
or when a user joins or leaves a channel. It can even be configured to play a personalized 'join' or 'disconnect'
sound for each user.

An example `chumbot.ini`:

```
[mumble]
Username = chumbot
Host = example.murmur.nfoservers.com
Port = 2112
Password = 1234

[clips]
ClipDir = ~/chumbot-clips
LinkPostedClipName = link_clip
UserJoinedClipName = default_join_clip
UserLeftClipName = default_leave_clip

[join]
user1 = join_clip1
user2 = join_clip2
user3 = join_clip3

[disconnect]
user1 = disconnect_clip1
user2 = disconnect_clip2
user3 = disconnect_clip3
```

## Contributing
Contributions are taken and any pull requests will be reviewed by me (eventually).

Please attempt to adhere to the coding practices in `.pylintrc`. Ensure no pylint
warnings are generated before creating a PR.
