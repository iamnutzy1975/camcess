import constants
import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def main():
    transferData = TransferData(access_token=constants.DROPBOX_TOKEN)

    file_from = 'C:\\Users\\Gord\\Desktop\\TrailCam\\perfect-bear-bait\\100_BTCF\\IMG_0010.JPG'
    file_to = '/trail-cameras/perfect/test.jpg'  # The full path to upload the file to, including the file name

    # API v2
    transferData.upload_file(file_from, file_to)

main()
