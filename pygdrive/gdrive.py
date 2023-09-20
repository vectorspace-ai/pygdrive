from google.oauth2 import service_account
from googleapiclient.discovery import build
from os import path
from googleapiclient.http import MediaFileUpload
import json
import os


class Gdrive:
    """A class represent google drive."""

    def __init__(self, credentials_filepath=None, credentials_env_var=None, scopes=None, download_dir=None, upload_dir=None):
        """
        :str credentials_filepath: The path to the service account json file.
        :str credentials_env_var: Use an environment variable to provide service account credentials.
        :str scopes:  User-defined scopes to request during the
                authorization grant.
        :str download_path: The path to the download folder.
        :str upload_path: The path to the upload folder.
        """
        self.service = None
        self.credentials_filepath = credentials_filepath
        self.credentials_env_var = credentials_env_var
        self.scopes = scopes
        self.download_dir = download_dir
        self.upload_dir = upload_dir
        self.connect()

    def connect(self):
        """
        Creates a Credentials instance from a service account json file or an environment variable
        :return: None
        """
        if self.credentials_env_var is not None:
            service_account_info = json.loads(os.environ[self.credentials_env_var])
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=self.scopes
            )
        else:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_filepath, scopes=self.scopes
            )
        self.service = build("drive", "v3", credentials=credentials)

    def check_does_folder_exist(self, folder_name):
        """
        Checking if folder with specified name exist.
        :str folder_name: Name of the folder which should be search.
        :return: True if folder found. Otherwise False.
        """
        folder_search = "mimeType = 'application/vnd.google-apps.folder'"
        results = (
            self.service.files()
            .list(
                fields="nextPageToken, files(id, name)",
                orderBy="createdTime",
                q=f"name contains '{folder_name}' and {folder_search}",
            )
            .execute()
        )
        item = results.get("files", [])
        if item:
            return True
        return False

    def check_does_file_exist(self, file_name):
        """
        Checking if file with specified name exist.
        :str file_name: Name of the file which should be search.
        :return: True if file found. Otherwise False.
        """
        file_search = "mimeType != 'application/vnd.google-apps.folder'"
        results = (
            self.service.files()
            .list(
                fields="nextPageToken, files(id, name)",
                orderBy="createdTime",
                q=f"name = '{file_name}' and {file_search}",
            )
            .execute()
        )
        item = results.get("files", [])
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
        results = (
            self.service.files()
            .list(
                fields="nextPageToken, files(id, name)",
                orderBy="createdTime",
                q=f"name = '{folder_name}' and {folder_search}",
            )
            .execute()
        )
        item = results.get("files", [])
        return item[-1]["id"], item[-1]["name"]

    def find_file(self, file_name):
        """
        Searching for file name.
        :str file_name: Name of the file which should be search.
        :return: id, name of the founded folder.
        """
        file_search = "mimeType != 'application/vnd.google-apps.folder'"
        results = (
            self.service.files()
            .list(
                fields="nextPageToken, files(id, name)",
                orderBy="createdTime",
                q=f"name = '{file_name}' and {file_search}",
            )
            .execute()
        )
        item = results.get("files", [])
        return item[-1]["id"], item[-1]["name"]

    def get_files_in_folder(self, folder_id):
        """
        Searching for all files sorted by createdTime inside folder.
        :str folder_id: : Id of the folder.
        :return: [{"id":"str", "name":"str"}]
        """
        file_search = "mimeType != 'application/vnd.google-apps.folder'"
        results = (
            self.service.files()
            .list(
                fields="nextPageToken, files(id, name)",
                orderBy="createdTime",
                q=f"'{folder_id}' in parents and {file_search}",
            )
            .execute()
        )
        item = results.get("files", [])
        return item

    def get_dirs_in_folder(self, folder_id):
        """
        Searching for all folders sorted by createdTime inside folder.
        :str folder_id: : Id of the folder.
        :return: [{"id":"str", "name":"str"}]
        """
        file_search = "mimeType = 'application/vnd.google-apps.folder'"
        results = (
            self.service.files()
            .list(
                fields="nextPageToken, files(id, name)",
                orderBy="createdTime",
                q=f"'{folder_id}' in parents and {file_search}",
            )
            .execute()
        )
        item = results.get("files", [])
        return item

    def download_file(self, file_id, file_name, download_path=None):
        """
        Download file by file_id.
        :str file_id: Id of the file.
        :str file_name: Name of the file.
        :str download_path: The path to the download folder. If None download path will be taken from self.download_dir
        :return: None
        """
        if download_path:
            path_dir = path.join(download_path, file_name)
        else:
            path_dir = path.join(self.download_dir, file_name)
        file_body = self.service.files().get_media(fileId=file_id).execute()
        with open(path_dir, "wb") as wer:
            wer.write(file_body)

    def create_folder(self, parent_id, folder_name):
        """
         Create folder inside parent folder.
        :str parent_id: Parent folder id.
        :str folder_name: Folder name.
        :return: id of the folder
        """

        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }
        file = self.service.files().create(body=file_metadata, fields="id").execute()
        return file["id"]

    def upload_file(self, folder_id, file_name, upload_path=None):
        """
        Upload file to folder with folder_id.
        :str folder_id: Parent id.
        :str file_name: File name.
        :str upload_path: The path to the upload folder. If None upload path will be taken from self.upload_dir
        :return: id of the file
        """

        if upload_path:
            path_dir = path.join(upload_path, file_name)
        else:
            path_dir = path.join(self.upload_dir, file_name)

        file_metadata = {"name": file_name, "parents": [folder_id]}
        media = MediaFileUpload(path_dir, resumable=True)
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file["id"]

    # def delete_file(self, file_id):
    #     """
    #     delete file or folder by id
    #     :int file_id: Id of the file to be deleted
    #     :return: None
    #     """
    #     self.service.files().delete(fileId=file_id).execute()


