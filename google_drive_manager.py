from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import base64
import os
import sys


class GoogleDriveManager(object):
    """
    This class is useful to perform operations on google drive public folder 'lila_screenshots'
    """

    def __init__(self):
        """
        This will instantiate the object of this class and authenticate with google drive for
        further use.
        """
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(gauth)

    def check_filecontent_size(self, content, max_file_size_allowed=2.0):
        """
        This function checks whether the file content size is less than max_file_size_allowed
        :param content: file content (bytes)
        :param max_file_size_allowed: max allowed size in Megabytes (float)
        :return: True if size of file content in less than or equal to max_file_size_allowed
        """
        if sys.getsizeof(content) / 1000 <= max_file_size_allowed * 1000:
            return True
        else:
            return False

    def get_google_folder_id(self, folder_name):
        """
        This function returns the google folder id if it exists.
        :param folder_name: name of folder name (string)
        :return: None,None if folder doesnt exists else sharelink and folder_ id.
        """
        folder_list = self.drive.ListFile({'q': "trashed=false"}).GetList()
        folder_id = None
        folder_link = None
        for folder in folder_list:
            if folder['title'] == folder_name:
                folder_id = folder['id']
                folder_link = folder['alternateLink']
                break
        return folder_link, folder_id

    def get_google_folder_link_from_parent_folder(self, parent_folder_name, folder_name):
        """
        This function returns the google folder id and link presents in google root folder if it exists.
        :param folder_name: name of folder name (string)
        :return: None,None if folder doesnt exists else sharelink and folder_ id.
        """
        folder_link, folder_id = self.get_google_folder_id(parent_folder_name)
        if not folder_id is None:
            files_in_folder = self.drive.ListFile(
                {'q': " '" + folder_id + "' in parents and trashed=false"}).GetList()
            for folder_file in files_in_folder:
                if folder_file['title'].lower() == folder_name.lower():
                    return folder_file['alternateLink'], folder_file['id']
            print('WARNING: Google file_name doesnt exists in folder_name')
            return None, None

        return folder_link, folder_id

    def uploadFolder(self, folder_path, google_folder_name):
        """
        This function uploads folder to google drive
        :param folder_path: path of folder which needs to be uploaded (string)
        :param google_folder_name: google folder name where new folder needs to be uploaded (String)
        :return: google url link if successfully uploaded else None.
        """

        if not os.path.exists(folder_path):
            print('ERROR: folder path doesnt exists %s' % (folder_path))
            return None

        folder_link, folder_id = self.get_google_folder_id(google_folder_name)

        name_of_folder = os.path.basename(folder_path)

        new_folder_link, new_google_folder_id = self.create_new_google_folder(name_of_folder, google_folder_name)

        if new_google_folder_id is None:
            print('ERROR: while create new google folder')
            return None

        for file in os.listdir(folder_path):
            if not os.getcwd() in folder_path:
                file_path = folder_path + '/' + file
            else:
                file_path = os.getcwd() + '/' + folder_path + '/' + file
            if os.path.isfile(file_path):
                response = self.uploadFileToGoogleFolder(new_google_folder_id,
                                                         os.path.abspath(folder_path + '/' + file))
                if response is None:
                    print('WARNING:Skipping file %s got some error while uploading it to google' % (file_path))
                else:
                    print('DEBUG: Uploaded file successfully %s' % (os.path.abspath(folder_path + '/' + file)))

            elif os.path.isdir(file_path):
                return self.uploadFolder(file_path, name_of_folder)

        return new_folder_link

    def create_new_google_folder(self, folder_name, google_base_folder_name):
        """
        This function creates new google folder in google drive.
        :param folder_name: name of google folder
        :param google_base_folder_name: base folder name in google drive where new folder will be created (string)
        :return: google folder share link and folder id if successfully created else None,None.
        """

        base_folder_link, base_folder_id = self.get_google_folder_id(google_base_folder_name)

        folder_already_exists_link, folder_already_exists_id = self.get_google_folder_id(folder_name)

        if folder_already_exists_id is None:
            if not base_folder_id is None:
                folder_metadata = {
                    'title': os.path.basename(folder_name),
                    "parents": [{"id": base_folder_id, "kind": "drive#childList"}],
                    'mimeType': 'application/vnd.google-apps.folder'
                }

                folder = self.drive.CreateFile(folder_metadata)
                folder.Upload()
                return folder['alternateLink'], folder['id']
            else:
                print('ERROR: google folder path doesnt exists ' % (google_base_folder_name))
                return None, None
        else:
            return folder_already_exists_link, folder_already_exists_id

    def uploadFileToGoogleFolder(self, google_folder_id, file_path):
        """
        This function uploads file to specific google folder with google_folder_id
        :param google_folder_id: id of google folder (String)
        :param file_path: path of file which needs to be uploaded to google folder(String)
        :return: file id if successfully uploaded else None.
        """

        if not os.path.exists(file_path):
            print('ERROR: file path doesnt exists ' % (file_path))
            return None

        if not google_folder_id is None:
            file_metadata = {
                'title': os.path.basename(file_path),
                "parents": [{"id": google_folder_id, "kind": "drive#childList"}]
            }

            file = self.drive.CreateFile(file_metadata)
            file.SetContentFile(file_path)
            try:
                file.Upload()
            except Exception as e:
                print('WARNING: Problem in uploading file %s  error %s, skipping this for now.' % (file_path, e))
                return None
            return file['id']
        else:
            print('ERROR: google folder id cannot be none' % (google_folder_id))
            return None

    def get_google_file_link(self, parent_folder_name, folder_name, file_name):
        """
        This function returns google sharable link of file_name present in google folder_name
        :param parent_folder_name: google root folder name present in google drive root (str)
        :param folder_name: google folder name where file exist (str)
        :param file_name: file_name for which sharable link is required (str)
        :return: google sharable link if file found else None (str)
        """

        folder_link, folder_id = self.get_google_folder_link_from_parent_folder(parent_folder_name, folder_name)
        if not folder_link is None and not folder_id is None:
            files_in_folder = self.drive.ListFile(
                {'q': " '" + folder_id + "' in parents and trashed=false"}).GetList()
            for folder_file in files_in_folder:
                if folder_file['title'].lower() == file_name.lower():
                    return folder_file['alternateLink']
            print('WARNING: Google file_name doesnt exists in folder_name')
            return None

        else:
            print('ERROR: Google parent folder not found')
            return None

    def downloadFile(self, id, save_at_path):
        """
        This function is responsible for download file from google drive to local path
        :param id: google id of that file which you want to download
        :param save_at_path: File path to save file
        :return: Nothing
        """
        file6 = self.drive.CreateFile({'id': id})
        file6.GetContentFile(save_at_path)

    def download_google_folder_to_local_dir(self, parent_google_folder_name, google_folder_name, local_path):
        """
        This function download folder present on google to local dir
        :param parent_google_folder_name: google root folder name Where model dir is present (str)
        :param google_folder_name: model folder name in google parent google folder (str)
        :param local_path: local path where google folder will be saved (str)
        :return: True if model files are downloaded to local path else False.
        """
        if not os.path.exists(local_path + google_folder_name):
            print('DEBUG: Model folder created locally, Now downloading files')
            os.mkdir(local_path + google_folder_name)
        else:
            print('WARNING: Model folder already exists locally. Checking all the files')

        folder_link, folder_id = self.get_google_folder_link_from_parent_folder(parent_google_folder_name,
                                                                                google_folder_name)
        if not folder_link is None and not folder_id is None:
            files_in_folder = self.drive.ListFile(
                {'q': " '" + folder_id + "' in parents and trashed=false"}).GetList()
            for folder_file in files_in_folder:
                if os.path.isfile(local_path + google_folder_name + '/' + folder_file['title']):
                    print('DEBUG: Model file already exists skipping file %s' % (folder_file['title']))
                else:
                    self.downloadFile(folder_file['id'], local_path + google_folder_name + '/' + folder_file['title'])
                    print('DEBUG: Google file downloaded %s' % (google_folder_name + '/' + folder_file['title']))
            print('DEBUG: Downloaded model files from google folder %s to local path %s' % (
            google_folder_name, local_path + google_folder_name))
            return True

        else:
            print('ERROR: Google parent folder not found')
            return False

    def uploadFile(self, filename, content, folder_name='lila_screenshots',
                   temp_directory='web/images/temp-screenshots/', max_file_size_allowed=2):
        """
        The function is responsible for uploading public content to google drive folder 'lila_screenshots'
        :param filename: Name of file you want to create (String)
        :param content: Content you want to add in the file (String)
        :param folder_name:  folder on google team drive where file needs to be uploaded. (String)
        :param temp_directory: path of directory where the new file will be stored temporary, after uploading the file on
        google drive it will be deleted (String)
        :param max_file_size_allowed: max size of file allowed on google drive in Megabites(float)
        :return: If file upload is successful then shared link and image id will be returned else None, None (str, str)

        """

        lila_public_folder_link, lila_public_folder_id = self.get_google_folder_id(folder_name)

        if not lila_public_folder_id is None:
            if self.check_filecontent_size(content, max_file_size_allowed):
                try:
                    # create temp file
                    if not os.path.exists(temp_directory):
                        raise ValueError('ERROR: temp_directory path doesnt exist in function uploadFile()')

                    with open(temp_directory + filename, "wb") as fh:
                        fh.write(base64.decodebytes(content))
                    fh.close()

                    file_metadata = {'title': filename,
                                     "parents": [{"id": lila_public_folder_id, "kind": "drive#childList"}],
                                     'mimeType': 'image/jpeg', }
                    file1 = self.drive.CreateFile(
                        file_metadata)  # Create GoogleDriveFile instance with title 'Hello.txt'.
                    file1.SetContentFile(temp_directory + filename)  # Set content of the file from given string.
                    file1.Upload()

                    # Remove temp file
                    os.remove(temp_directory + filename)

                    # Insert the permissions to make file readable to everyone.
                    permission = file1.InsertPermission({
                        'type': 'anyone',
                        'value': 'anyone',
                        'role': 'reader'})
                    # Shared Link
                    return file1['alternateLink'], file1['id']
                except Exception as e:
                    print('ERROR: %s' % str(e))
                    return None, None

            else:
                print('ERROR: Size of filecontent is larger than %s' % (max_file_size_allowed))
                return None, None

        else:
            print('ERROR: Public folder not found.')
            return None, None


if __name__ == '__main__':
    google_drive_manager = GoogleDriveManager()

    # For test purpose.
    # print(google_drive_manager.uploadFolder('solution_verification_service/saved_models/03_02_AM_July_07_2019', 'online_model_training'))
    # print(google_drive_manager.get_google_file_link('online_model_training', '07_29_PM_July_11_2019', 'performance_curve_07_29_PM_July_11_2019.png'))
    google_drive_manager.download_google_folder_to_local_dir('online_trained_solution_verification_models',
                                                             '03_07_AM_July_12_2019',
                                                             './solution_verification_service/saved_models/')
