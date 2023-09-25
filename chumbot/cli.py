"""Command-line interface and main entry point for Chumbot."""
import argparse
import configparser
from os.path import expanduser

from chumbot import client_interface
from chumbot.backend.chumshell import ChumShell
from chumbot.backend.constants import MUMBLE_CONFIG

_CONFIG = configparser.ConfigParser()
_CONFIG.read(expanduser(MUMBLE_CONFIG))

_USERNAME = _CONFIG['mumble']['Username']
_HOST = _CONFIG['mumble']['Host']
_PORT = int(_CONFIG['mumble']['Port'])
_PASSWORD = _CONFIG['mumble']['Password']


def run():
    """Run the Chumbot command-line interface."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(prog='chumbot',
                                     description='Chumbot command-line interface')

    parser.add_argument('-u', '--username', help="specify Chumbot's username",
                        type=str, action='store', default=_USERNAME)
    parser.add_argument('-H', '--host', help='specify the Mumble host address',
                        type=str, action='store', default=_HOST)
    parser.add_argument('-P', '--port', help='specify the Mumble host port',
                        type=str, action='store', default=_PORT)
    parser.add_argument('-p', '--password', help='specify the Mumble host password',
                        type=str, action='store', default=_PASSWORD)
    parser.add_argument('-d', '--debug', help='enable debug message printing',
                        action='store_true')

    args = parser.parse_args()
    client_interface.initialize(args.username, args.host, args.port, args.password, args.debug)

    ChumShell().cmdloop()


if __name__ == '__main__':
    run()
