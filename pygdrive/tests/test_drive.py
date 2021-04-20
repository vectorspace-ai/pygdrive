import unittest
import pygdrive

import unittest.mock as mock

CREDENTIALS_FILEPATH = {}
SCOPES = []
DOWNLOAD_DIR = ''
UPLOAD_DIR = ''


class TestBasic(unittest.TestCase):
    """
    Base class
    """
    @mock.patch.object(pygdrive.gdrive, 'build', autospec=True)
    @mock.patch.object(pygdrive.gdrive.service_account.Credentials, 'from_service_account_file', autospec=True)
    def setUp(self, mock_credential_object, mock_build_object):
        self.test_object = pygdrive.gdrive.Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)

    def tearDown(self):
        self.test_object = None


class TestDrive(TestBasic):
    def test_object_create(self):
        self.assertTrue(self.test_object is not None)


class TestFolder(TestBasic):
    def test_find_folder(self):
        mock_id, mock_name = 'test_id123', 'test_name'
        self.test_object.service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': mock_id, 'name': mock_name}]}
        id, name = self.test_object.find_folder('test_file')
        self.assertEqual(mock_id, id)

    def test_folder_create(self):
        mock_parent_id = 'parent_id123'
        mock_folder_id, mock_folder_name = 'test_id123', 'folder_test'
        self.test_object.service.files.return_value.create.return_value.execute.return_value = {'id': mock_folder_id}
        folder_id = self.test_object.create_folder(mock_parent_id, mock_folder_name)
        self.assertEqual(folder_id, mock_folder_id)


class TestUploading(TestBasic):
    @mock.patch.object(pygdrive.gdrive, 'MediaFileUpload', autospec=True)
    def test_object_upload(self, mock_media_upload):
        mock_parent_id = 'parent_id123'
        mock_file_id, mock_file_name = 'test_id123', 'file_test2.csv'
        self.test_object.service.files.return_value.create.return_value.execute.return_value = {'id': mock_file_id}
        file_id = self.test_object.upload_file(mock_parent_id, mock_file_name)
        self.assertEqual(file_id, mock_file_id)


# class TestDownloading(TestBasic):
#     def test_object_download(self):
#         mock_file_id, mock_file_name = 'test_id123', 'file_test2.csv'
#         self.test_object.service.files.return_value.get_media.return_value.execute.return_value = None
#         return_value = self.test_object.download_file(mock_file_id, mock_file_name)
#         self.assertEqual(None, return_value)


class TestFileSearching(TestBasic):
    def test_search_existing_file(self):
        mock_file_id, mock_file_name = 'test_id123', 'file_test2.csv'
        self.test_object.service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': mock_file_id, 'name': mock_file_name}]}
        id, name = self.test_object.find_file(mock_file_name)
        self.assertEqual(id, mock_file_id)

    def test_search_existing_folder(self):
        mock_folder_id, mock_folder_name = 'test_id123', 'file_test2.csv'
        self.test_object.service.files.return_value.list.return_value.execute.return_value = {
            'files': [{'id': mock_folder_id, 'name': mock_folder_name}]}
        id, name = self.test_object.find_folder(mock_folder_name)
        self.assertEqual(id, mock_folder_id)
