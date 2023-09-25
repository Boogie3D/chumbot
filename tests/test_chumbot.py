"""Test the Chumbot package with Unittest."""
import unittest

from chumbot import __version__


class TestChumbot(unittest.TestCase):
    """Test the Chumbot package."""

    def test_version(self):
        """Test the package version."""
        self.assertTrue(__version__)
