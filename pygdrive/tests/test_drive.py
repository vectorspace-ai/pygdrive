import unittest
import unittest.mock as mock
from pygdrive import Gdrive
from pygdrive.tests.test_util import *

TEST_ATTR = read_settings_file()

CREDENTIALS_FILEPATH = TEST_ATTR['test_config_file']
SCOPES = TEST_ATTR['scope']
DOWNLOAD_DIR = TEST_ATTR['download_dir']
UPLOAD_DIR = TEST_ATTR['upload_dir']


class TestDrive(unittest.TestCase):

    def test_object_create(self):
        test_object = Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)
        self.assertTrue(test_object is not None)


class TestUploading(unittest.TestCase):
    gd = Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)

    def test_object_upload(self):
        ...


class TestDownloading(unittest.TestCase):
    gd = Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)

    def test_object_download(self):
        ...


class TestFileSearching(unittest.TestCase):
    gd = Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)

    def test_search_existing_file(self):
        ...
    def test_search_random_file(self):
        ...
    def test_search_existing_folder(self):
        ...
    def test_search_random_folder(self):
        ...