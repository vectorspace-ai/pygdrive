from google.oauth2 import service_account
from googleapiclient.discovery import build
from os import path
from googleapiclient.http import MediaFileUpload

#TODO SCOPES

class Gdrive:
    """ A class represent google drive. """

    def __init__(self, credentials_filepath, scopes, download_dir, upload_dir):
        """
        :str credentials_filepath: The path to the service account json file.
        :str scopes:  User-defined scopes to request during the
                authorization grant.
        :str download_path: The path to the download folder.
        :str upload_path: The path to the upload folder.
        """
        self.service = None
        self.credentials_filepath = credentials_filepath
        self.scopes = scopes
        self.download_dir = download_dir
        self.upload_dir = upload_dir
        self.connect()

    def connect(self):
        """
        Creates a Credentials instance from a service account json file.
        :return: None
        """
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials_filepath, scopes=self.scopes)
        self.service = build('drive', 'v3', credentials=credentials)

    def check_is_folder_exist(self, folder_name):
        """
        Checking if folder with specified name exist.
        :str folder_name: Name of the folder which should be search.
        :return: True if folder found. Otherwise False.
        """
        folder_search = "mimeType = 'application/vnd.google-apps.folder'"
        results = self.service.files().list(fields="nextPageToken, files(id, name)", orderBy='createdTime',
                                            q=f"name contains '{folder_name}' and {folder_search}").execute()
        item = results.get('files', [])
        if item:
            return True
        return False

    def check_is_file_exist(self, file_name):
        """
        Checking if file with specified name exist.
        :str file_name: Name of the file which should be search.
        :return: True if file found. Otherwise False.
        """
        file_search = "mimeType != 'application/vnd.google-apps.folder'"
        results = self.service.files().list(fields="nextPageToken, files(id, name)", orderBy='createdTime',
                                            q=f"name = '{file_name}' and {file_search}").execute()
        item = results.get('files', [])
        if item:
            return True
        return False

    def find_folder(self, folder_name):
        """
        Searching for folder name.
        :str folder_name: Name of the folder which should be search.
        :return: id, name of the founded folder.
        """
        folder_search = "mimeType = 'application/vnd.google-apps.folder'"
        results = self.service.files().list(fields="nextPageToken, files(id, name)", orderBy='createdTime',
                                            q=f"name = '{folder_name}' and {folder_search}").execute()
        item = results.get('files', [])
        return item[-1]['id'], item[-1]['name']

    def find_file(self, file_name):
        """
        Searching for file name.
        :str file_name: Name of the file which should be search.
        :return: id, name of the founded folder.
        """
        file_search = "mimeType != 'application/vnd.google-apps.folder'"
        results = self.service.files().list(fields="nextPageToken, files(id, name)", orderBy='createdTime',
                                            q=f"name = '{file_name}' and {file_search}").execute()
        item = results.get('files', [])
        return item[-1]['id'], item[-1]['name']

    def find_file_in_folder(self, folder_id):
        """
        Searching for last files sorted by createdTime inside folder.
        :str folder_id: : Id of the folder.
        :return: id, name of the founded file.
        """
        file_search = "mimeType != 'application/vnd.google-apps.folder'"
        results = self.service.files().list(fields="nextPageToken, files(id, name)", orderBy='createdTime',
                                            q=f"{folder_id} in parents and {file_search}").execute()
        item = results.get('files', [])
        return item[-1]['id'], item[-1]['name']

    def download_file(self, file_id, file_name):
        """
        Download file by file_id.
        :str file_id: Id of the file.
        :str file_name: Name of the file.
        :return: None
        """
        request = self.service.files().get_media(fileId=file_id)
        response = request.execute()
        with open(path.join(self.download_dir, file_name), "wb") as wer:
            wer.write(response)

    def create_folder(self, folder_id, folder_name):
        """
         Create folder inside parent folder.
        :str folder_id: Parent folder id.
        :str folder_name: Folder name.
        :return: None
        """
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        file = self.service.files().create(body=file_metadata,
                                           fields='id').execute()

    def upload_file(self, folder_id, file_name):
        """
        Upload file to folder with folder_id.
        :str folder_id: Parent id.
        :str file_name: File name.
        :return: None
        """

        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(path.join(self.upload_dir, file_name),
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                           media_body=media,
                                           fields='id').execute()


