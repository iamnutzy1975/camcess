from dropbox_credentials import DROPBOX_TOKEN
import dropbox
from PIL import Image
import os

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

def main(idx):
    transferData = TransferData(access_token=DROPBOX_TOKEN)

    os.chdir('C:\\Users\\Gord\\Desktop\\TrailCam\\perfect-bear-bait\\100_BTCF')
    original_filename = 'IMG_{index}.JPG'.format(index=idx)

    #compress first

    picture = Image.open(original_filename)

    # set quality= to the preferred quality.
    # I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
    os.chdir('C:\\temp')
    compressed_filename = "Compressed_{}".format(original_filename)
    picture.save(compressed_filename, "JPEG", optimize=True, quality=10)

    # API v2
    #transferData.upload_file(os.path.abspath(compressed_filename)
    #                         # The full path to upload the file to, including the file name
    #                         ,'/trail-cameras/perfect/{filename}'.format(filename=compressed_filename))

main('0309')
main('1125')
