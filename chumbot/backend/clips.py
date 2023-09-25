"""Map sound clip names to sound clip files."""
from os import listdir
from os.path import expanduser, splitext


class Clips(dict):
    """Stores and maps sound clip files by their extensionless names."""

    def __init__(self, clip_directory, extension):
        """Create a new sound clip dictionary."""
        super().__init__()

        self._clip_directory = clip_directory
        self._extension = extension
        self._load_clips()

    def __iter__(self):
        """Return a sound clip iterator."""
        return iter(self.keys())

    def reload(self):
        """Reload the sound clips, loading any new ones if they exist."""
        self.clear()
        self._load_clips()

    def _load_clips(self):
        """Load the sound clips from the clip directory."""
        for filename in listdir(expanduser(self._clip_directory)):
            name, ext = splitext(filename)
            if ext == self._extension:
                self[name] = filename
