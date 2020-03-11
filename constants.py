import os
import logging

#configure authentication
#Google APIs
#CLIENT_SECRET_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials'
# , 'analyticspros-management-kit-service.json')
CLIENT_SECRET_GMAIL_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials'
                                                    , 'client_secret_407310947692-av6hjvtb9rd60p4sa86qa1egiu75tjv7.apps.googleusercontent.com.json')
SERVICE_ACCOUNT_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials'
                                                , 'abstract-gizmo-269816-d1cb94a4eea9.json')

#Configure inbox to monitor
EMAIL_ADDRESS_TO_MONITOR = 'go06041973nut@gmail.com'  #password for account is @m@z0namazon
GMAIL_LABEL_INCOMING_ROOT = 'camcess'
GMAIL_LABEL_PROCESSED = 'attachmentsaved'
INBOX_FILTER = '{'
for location in ['camera1','dargat']:
    INBOX_FILTER += 'label:{root}/{location} '.format(root=GMAIL_LABEL_INCOMING_ROOT,location=location)
INBOX_FILTER += '}'
INBOX_PURGING_FILTER = 'label:'+GMAIL_LABEL_PROCESSED + ' AND older_than:7d'

#Application config
ATTACHMENT_REGEX_PATTERN = r"(?i)^.*\.jpe?g"       # Regex pattern for jpeg images
CAMERAS_PARENT_RX_PATTERN = r"^{root}\/.*".format(root=GMAIL_LABEL_INCOMING_ROOT)

#Configure Logging
APPLICATION_LOGGING_LEVEL = logging.INFO  #choose one of NOTSET, DEBUG, INFO, WARN, ERROR, FATAL
if os.name.upper() =='NT':
	APPLICATION_LOGGING_DIR = 'c:\\temp'
else:
	APPLICATION_LOGGING_DIR = '/home/ec2-user/logs'
SUCCESS = 'SUCCESS'
FAIL = 'FAIL'
FORMAT_TIMESTAMP_FILENAME = '%Y%m%d'

GCS_BUCKET_NAME = 'camcess-bucket'
