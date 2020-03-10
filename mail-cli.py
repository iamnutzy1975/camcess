from loggingController import loggingController
from gmailController import gmailController
import logging
import os
import constants as CONSTANT
import glob

# setup inbox
#  For now this was done manually but can be done programmatically within constructor of gmailController
#  label messages with AW-incoming as they arrive
#  set up lable 'AW-processed' and configure in constants.py file.

# Setup up logging
logger = loggingController(filename=os.path.splitext(os.path.basename(__file__))[0]
                           ,filepath=CONSTANT.APPLICATION_LOGGING_DIR
                           ,loggingLevel=CONSTANT.APPLICATION_LOGGING_LEVEL)

# remove all previous data files
#remove all previous data files
for f in glob.glob("*.csv") or glob.glob("*.xls"):
    os.remove(f)

#  Check inbox, filter if desired using query parameter
#  filter using the gmail UI search box format
#  https://support.google.com/mail/answer/7190?hl=en
#  does not search trash, unless specified.

gmailController = gmailController(logger=logger, secretFile=CONSTANT.CLIENT_SECRET_GMAIL_CREDENTIALS_PATH
                                  , emailAddress=CONSTANT.EMAIL_ADDRESS_TO_MONITOR)
emailMessages = gmailController.checkInBox(query=CONSTANT.INBOX_FILTER)
logger.log(('%s inbox has %s messages matching filter %s'%(CONSTANT.EMAIL_ADDRESS_TO_MONITOR
        ,emailMessages.__len__(),CONSTANT.INBOX_FILTER)),level=logging.INFO)

# process inbox
for message in emailMessages:
    responseCode, messageDate = gmailController.processEmailMessage(message['id'])
    if responseCode:
      logger.log('Successfully processed message with timestamp %s' % (messageDate),level=logging.INFO)
    else:
      logger.log('Error processing message with timestamp %s' % (messageDate), level=logging.INFO)
    
# clean email account of messages older than X days
gmailController.purgeInbox()
  
