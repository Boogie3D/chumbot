"""Test the Chumbot Client interface with Unittest."""
from time import sleep
import unittest

import pymumble_py3 as pymumble

import chumbot.client_interface as client_interface
from chumbot.backend.clips import Clips

# pylama:ignore=W0212


class TestClientInterface(unittest.TestCase):
    """Test the Client class."""

    @classmethod
    def setUpClass(cls):
        """Initialize the Mumble client."""
        client_interface.initialize()

    def test_initialize(self):
        """Test client initialization."""
        self.assertEqual(client_interface._USERNAME, client_interface._CLIENT._username)
        self.assertEqual(client_interface._HOST, client_interface._CLIENT._host)
        self.assertEqual(client_interface._PORT, client_interface._CLIENT._port)
        self.assertEqual(client_interface._PASSWORD, client_interface._CLIENT._password)

        self.assertFalse(client_interface._CLIENT._running)
        self.assertFalse(client_interface._CLIENT._connected)
        self.assertFalse(client_interface._CLIENT._muted)
        self.assertEqual(0, client_interface._CLIENT._last_message_time)
        self.assertIsInstance(client_interface._CLIENT._clips, Clips)
        self.assertIsInstance(client_interface._CLIENT._mumble, pymumble.Mumble)

    def test_connect(self):
        """Test connecting the client to the server."""
        client_interface.connect()
        sleep(2)
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)

    def test_disconnect(self):
        """Test disconnecting the client from the server."""
        client_interface.connect()
        sleep(1)
        client_interface.disconnect()
        sleep(1)
        self.assertFalse(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)

    def test_reconnect(self):
        """Test reconnecting the client to the server."""
        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)

        sleep(1)
        client_interface.reconnect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)
        sleep(1)

    def test_get_channels(self):
        """Test getting of all the Mumble channels."""
        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)
        sleep(1)

        channels = client_interface.get_channels()

        for channel in channels:
            self.assertIsInstance(channel, pymumble.channels.Channel)

    def test_get_channel_population(self):
        """Test getting of a channel population."""
        target_channel = 'Root'

        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)
        sleep(1)

        population = client_interface.get_channel_population(target_channel)

        self.assertIsInstance(population, int)
        self.assertGreaterEqual(population, 0)

    def test_move_to_channel(self):
        """Test moving the client to another channel."""
        target_channel = 'BIG CHUG'

        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)

        client_interface.move_to_channel(target_channel)
        sleep(1)
        self.assertEqual(target_channel, client_interface._CLIENT._mumble.my_channel()['name'])

    def test_mute_self(self):
        """Test muting the client."""
        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)
        self.assertFalse(client_interface._CLIENT._muted)
        sleep(1)

        client_interface.mute_self()
        self.assertTrue(client_interface._CLIENT._muted)
        sleep(2)

    def test_unmute_self(self):
        """Test unmuting the client."""
        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)
        self.assertFalse(client_interface._CLIENT._muted)
        sleep(1)

        client_interface.mute_self()
        self.assertTrue(client_interface._CLIENT._muted)
        sleep(2)

        client_interface.unmute_self()
        self.assertFalse(client_interface._CLIENT._muted)
        sleep(2)

    def test_play_audio(self):
        """Test playing audio through the client."""
        client_interface.connect()
        self.assertTrue(client_interface._CLIENT._connected)
        self.assertTrue(client_interface._CLIENT._running)
        client_interface.play_clip('_link')
        client_interface.play_clip('relax')
