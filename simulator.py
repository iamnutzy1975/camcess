from loggingController import loggingController
from gmailController import gmailController
from storageController import storageController
import constants as CONSTANT
import random
import os
from PIL import Image
import piexif
import datetime
import pytz

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--location', help='name of the location of the camera')
parser.add_argument('--dir', help='file directory where the attachment is located')
parser.add_argument('--file', help='filename of the attachment')

args = parser.parse_args()

logger = loggingController(filename=os.path.splitext(os.path.basename(__file__))[0]
                           ,filepath=CONSTANT.APPLICATION_LOGGING_DIR
                           ,loggingLevel=CONSTANT.APPLICATION_LOGGING_LEVEL)

storage = storageController( bucket_name=CONSTANT.GCS_BUCKET_NAME,
                            credentials_file=CONSTANT.SERVICE_ACCOUNT_CREDENTIALS_PATH)

gmail = gmailController(logger=logger, storage=storage, secretFile=CONSTANT.CLIENT_SECRET_GMAIL_CREDENTIALS_PATH
                                  , emailAddress=CONSTANT.EMAIL_ADDRESS_TO_MONITOR)

file = os.path.join(args.dir, args.file)
img = Image.open(file)

exif_dict = {}
exif_dict["0th"] = {}
exif_dict["Exif"] = {}

# We now have a useful Exif dict, time to adjust the values
# now = datetime.datetime.utcnow()
now = datetime.datetime.now(pytz.timezone("Canada/Mountain"))

d = now.strftime("%Y:%m:%d %H:%M:%S")
exif_dict["Exif"][36868] = d.encode("utf-8")
exif_dict["Exif"][36867] = d.encode("utf-8")
exif_dict["0th"][306] = d.encode("utf-8")

# Convert into bytes and dump into file
exif_bytes = piexif.dump(exif_dict)
piexif.insert(exif_bytes, file)

message = gmail.CreateMessageWithAttachment(sender='simulator@python.com'
                                  ,to='go06041973nut@gmail.com'
                                  ,subject='testing location {}'.format(args.location)
                                  ,message_text='message text from the location {}'.format(args.location)
                                  ,file_dir=args.dir
                                   ,filename=args.file)

gmail.SendMessage(message=message)


