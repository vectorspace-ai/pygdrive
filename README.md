# pygdrive

pygdrive is a wrapper library of [google-api-python-clien](https://github.com/google/google-api-python-client) that simplifies uploading and downloading files. 

Project Info
------------

- GitHub: [https://github.com/vectorspace-ai/pygdrive](https://github.com/vectorspace-ai/pygdrive)

Features of pygdrive
-------------------

-  Simplifies OAuth2.0 with service_account into just a few lines with flexible settings.
-  Wraps [Google Drive API](https://developers.google.com/drive/api/v3/>) into
   a class which can search, upload and download files and folders.


How to install
--------------
You can install PyDrive with regular pip command.
```python
pip install pygdrive
```
You can install pygdrive from the current development version from GitHub, use:

```python
pip install git+https://github.com/vectorspace-ai/pygdrive.git
```

Creating credentials.json file
---------------------------

Download client_secrets.json from Google API Console. 
Share your Drive account's folder to your service account.
Your service account's addresss looks like XXX@XXX.iam.gserviceaccount.com.
Then your service account can see the shared folder from your Drive account.

Сreating Gdrive object
---------------

```python
  from pygdrive import Gdrive
  SCOPES = ['https://www.googleapis.com/auth/drive']
  CREDENTIALS_FILEPATH = 'credentials.json'
  DOWNLOAD_DIR = 'download_dir/'
  UPLOAD_DIR = 'upload_dir/'
  gdrive_object = Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)
  ```

File management made easy
-------------------------

Upload file to certain folder:

Make sure that folder exists and filename appears in UPLOAD_DIR

```python   
folder_id, _ = gdrive_object.find_folder('coingecko')
gdrive_object.upload_file(folder_id, 'filename.extension')
```

Create folder:

```python   
parent_id = 'PARENT ID'
folder_id = gdrive_object.create_folder(parent_id, 'folder_name')
```

Make sure that DOWNLOAD_DIR exists and filename.extension in google drive folder. 

```python
file_id, file_name = gdrive_object.find_file('filename.extension')
gdrive_object.download_file(file_id, file_name)
```
After uploading/downloading files you should expect uploaded/downloaded file.
