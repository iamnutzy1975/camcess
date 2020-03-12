from loggingController import loggingController
from gmailController import gmailController
from storageController import storageController
import os
import constants as CONSTANT

logger = loggingController(filename=os.path.splitext(os.path.basename(__file__))[0]
                           ,filepath=CONSTANT.APPLICATION_LOGGING_DIR
                           ,loggingLevel=CONSTANT.APPLICATION_LOGGING_LEVEL)

storage = storageController( bucket_name=CONSTANT.GCS_BUCKET_NAME,
                            credentials_file=CONSTANT.SERVICE_ACCOUNT_CREDENTIALS_PATH)

gmail = gmailController(logger=logger, storage=storage, secretFile=CONSTANT.CLIENT_SECRET_GMAIL_CREDENTIALS_PATH
                                  , emailAddress=CONSTANT.EMAIL_ADDRESS_TO_MONITOR)

message = gmail.CreateMessageWithAttachment(sender='simulator@python.com'
                                  ,to='go06041973nut@gmail.com'
                                  ,subject='camera1'
                                  ,message_text='this is the message text'
                                  ,file_dir=CONSTANT.APPLICATION_LOGGING_DIR
                                   ,filename='IMG_0005.JPG')

gmail.SendMessage(message=message)


