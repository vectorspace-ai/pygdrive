# pygdrive

pygdrive is a wrapper library of [google-api-python-clien](https://github.com/google/google-api-python-client) that simplifies uploading and downloading files. 

Project Info
------------

- Documentation: 
- GitHub: [https://github.com/vectorspace-ai/pygdrive](https://github.com/vectorspace-ai/pygdrive)

Features of pygdrive
-------------------

-  Simplifies OAuth2.0 with service_account into just few lines with flexible settings.
-  Wraps [Google Drive API](https://developers.google.com/drive/api/v3/>) into
   class which can search, upload and download files and folders.


How to install
--------------

You can install pygdrive from the current development version from GitHub, use:

```python
pip install git+https://github.com/vectorspace-ai/pygdrive.git
```

Сreating Gdrive object
---------------

Download *credentials.json* from Vectorspace AI engineers google drive shared folder. 

```python
  from pygdrive import Gdrive
  SCOPES = ['https://www.googleapis.com/auth/drive']
  CREDENTIALS_FILEPATH = 'credentials.json'
  DOWNLOAD_DIR = 'storage/data_storage/'
  UPLOAD_DIR = 'storage/data_storage/'
  gdrive_object = Gdrive(CREDENTIALS_FILEPATH, SCOPES, DOWNLOAD_DIR, UPLOAD_DIR)
  ```

File management made easy
-------------------------

Upload file to certain folder:

Make sure that folder exist and filename appears in UPLOAD_DIR

```python   
folder_id, _ = gdrive_object.find_folder('coingecko')
gdrive_object.upload_file(folder_id, 'filename.extension')
```

Create folder:

```python   
parent_id = 'PARENT ID'
folder_id = gdrive_object.create_folder(parent_id, 'folder_name')
```

Make sure that DOWNLOAD_DIR exist and filename.extension in google drive folder. 

```python
file_id, file_name = gdrive_object.find_file('filename.extension')
gdrive_object.download_file(file_id, file_name)
```
After uploading/downloading files you should expect uploaded/downloaded file.
