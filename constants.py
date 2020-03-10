import os
import logging

#configure authentication
#Google APIs
#CLIENT_SECRET_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials'
# , 'analyticspros-management-kit-service.json')
CLIENT_SECRET_GMAIL_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials'
                                                    , 'client_secret_407310947692-av6hjvtb9rd60p4sa86qa1egiu75tjv7.apps.googleusercontent.com.json')
CLIENT_SECRET_GA_CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials'
                                                 , 'abstract-gizmo-269816-d1cb94a4eea9.json')

#Configure inbox to monitor
EMAIL_ADDRESS_TO_MONITOR = 'go06041973nut@gmail.com'  #password for account is @m@z0namazon
GMAIL_LABEL_INCOMING = 'camera1'
GMAIL_LABEL_PROCESSED = 'camera1-done'
INBOX_FILTER = 'label:'+GMAIL_LABEL_INCOMING
INBOX_PURGING_FILTER = 'label:'+GMAIL_LABEL_PROCESSED + ' AND older_than:45d'

#Application config
UPLOAD_DIR = 'uploadDirectory'
STAGING_DIR = 'stagingDirectory'
PROCESSED_DIR = 'processedDirectory'
TABLE_NAME = 'table_name'
STARTING_ROW = 'startingRow'
STARTING_SHEET = 'startingSheet'
DATA_TYPE = 'dataType'
FORMAT = 'format'
SCHEMA = 'schema'
DIMENSIONS = 'dimensions'
METRICS = 'metrics'
VIEW_ID = 'google_analytics_view_id'
SQL_INSERT_COMMAND_FILE = 'sql_insert_command_file'
SQL_DELETE_COMMAND_FILE = 'sql_delete_command_file'
ATTACHMENT_REGEX_PATTERN = 'attachmentRXPattern'
STRING = 'str'
INTEGER = 'int'
TIMESTAMP = 'ts'
MONEY = 'money'
IGNORE = 'ignore'

#Configure Logging
APPLICATION_LOGGING_LEVEL = logging.INFO  #choose one of NOTSET, DEBUG, INFO, WARN, ERROR, FATAL
if os.name.upper() =='NT':
	APPLICATION_LOGGING_DIR = 'c:\\temp'
else:
	APPLICATION_LOGGING_DIR = '/home/ec2-user/logs'
#Used when converting excel files to CSV and when copying CSV files from S3 to redshift.
FILE_DELIMITER = ';'
SUCCESS = 'SUCCESS'
FAIL = 'FAIL'
FORMAT_TIMESTAMP = '%Y-%m-%d %H:%M:%S'
FORMAT_DATEONLY_STAMP = '%Y-%m-%d'
FORMAT_TIMESTAMP_FILENAME = '%Y%m%d'
