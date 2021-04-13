from google.oauth2 import service_account
from googleapiclient.discovery import build
from os.path import join
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'coinmetro-309919-3921c791278f.json'
DATASOURCE_PATH = '../storage/data_storage/'
MODELS_PATH = '../storage/model_storage/word2vec/'

class Gdrive:
    """ A class represent google drive """
    def __init__(self, credentials):
        self.service = None
        self.credentials = credentials
        self.connect()

    def connect(self):
        credentials = service_account.Credentials.from_service_account_file(
            self.credentials, scopes=SCOPES)
        self.service = build('drive', 'v3', credentials=credentials)


    def find_object(self, list_obj_name, is_folder):
        ids = []
        lst_title = []

        if is_folder:
            folder_search = "mimeType = 'application/vnd.google-apps.folder'"
        else:
            folder_search = "mimeType != 'application/vnd.google-apps.folder'"
        for obj_name in list_obj_name:

            results = self.service.files().list(fields="nextPageToken, files(id, name)", orderBy='createdTime',
                                           q=f"name contains '{obj_name}' and {folder_search}").execute()
            newest_item = results.get('files', [])['files'][-1]
            ids.append(newest_item['id'])
            lst_title.append(newest_item['name'])
        return ids


    def download_files(self, list_obj_name):
        ids, titles = self.find_object(list_obj_name, False)
        for file_id, t in zip(ids, titles):
            request = self.service.files().get_media(fileId=file_id)
            response = request.execute()
            with open(join(DATASOURCE_PATH, t), "wb") as wer:
                wer.write(response)
        return titles

    def get_parents_id(self, name):
        return self.find_object(name, True)[0]

    def create_folder(self, folder_name, folder_id):
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        file = self.service.files().create(body=file_metadata,
                                      fields='id').execute()

    def upload_file(self, folder_id, file_path):
        filename = file_path.split('/')[-1]
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path,
                                resumable=True)
        file = self.service.files().create(body=file_metadata,
                                      media_body=media,
                                      fields='id').execute()

gdrive_object = Gdrive(SERVICE_ACCOUNT_FILE)


