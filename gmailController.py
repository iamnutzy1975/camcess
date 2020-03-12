import helpers as helpers
from apiclient import errors
import base64
import logging
import constants as CONSTANT
import datetime
import re


#For simulating emails
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import os
from apiclient import errors

from email import encoders

class gmailController(object):
    def __init__(self,logger,storage,secretFile,emailAddress):
        try:
            self.labels = []
            scope = ['https://www.googleapis.com/auth/gmail.readonly',
                        'https://www.googleapis.com/auth/userinfo.email',
                        'https://www.googleapis.com/auth/userinfo.profile',
                        'https://www.googleapis.com/auth/gmail.compose',
                        'https://www.googleapis.com/auth/gmail.send',
                        'https://www.googleapis.com/auth/gmail.modify',
                        'https://www.googleapis.com/auth/gmail.labels']
            self.logger = logger
            self.storage = storage
            self.service = helpers.getGoogleService(secretFile=secretFile, scope=scope, apiName='gmail',
                                                    apiVersion='v1')
            self.emailAddress = emailAddress
            self.gmailLabelIdProcessed = self._getGmailLabelId(CONSTANT.GMAIL_LABEL_PROCESSED)
            self.gmailLabelIdIncoming = self._getGmailLabelId(CONSTANT.GMAIL_LABEL_INCOMING_ROOT)
        except Exception as err:
            print('gmailController constructor error: {}'.format(err))


    def checkInBox(self,query):
        """Get a list of Messages from the user's mailbox.
        """
        try:
            response = self.service.users().messages().list(userId=self.emailAddress,
                                                       q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.service.users().messages().list(userId=self.emailAddress, q=query,
                                                           pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as err:
            self.logger.log('gmailController.checkInBoxAn error: {}'.format(err), level=logging.ERROR)

    def processEmailMessage(self,emailMessageId):
        try:
            message = self.service.users().messages().get(userId=self.emailAddress, id=emailMessageId).execute()

            for part in message['payload']['parts']:
                #Process jpeg images only that are 30 KB in size or higher
                self.logger.log('rocessEmailMessage checking attachment size [{s}] and name [{n}]: '
                                .format(s=part['body']['size'],n=part['filename'])
                                , level=logging.INFO)
                if re.match(CONSTANT.ATTACHMENT_REGEX_PATTERN,part['filename']) \
                        and part['body']['size'] > CONSTANT.ATTACHMENT_SIZE_MINIMUM:
                    attachment = self.service.users().messages().attachments().get(userId=self.emailAddress
                                        , messageId=emailMessageId,id=part['body']['attachmentId']).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data']
                                                         .encode('UTF-8'))

                    filename_ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")

                    camera_location_path = ''
                    for id in message['labelIds']:
                        label_name = self._getGmailLabelName(id)
                        if re.match(CONSTANT.CAMERAS_PARENT_RX_PATTERN,label_name):
                            camera_location_path = label_name
                            label_id = id
                            break   #should be only one label


                    self.storage.upload_object(object_data=file_data
                                               ,object_key_name='{path}/{fts}_{ifn}'.format(path=camera_location_path,
                                                                                            ifn=part['filename']
                                                                                            ,fts=filename_ts))
                    # new_file = open("c:\\temp\\{}.jpg".format(part['filename']), mode="wb")
                    # new_file.write(file_data)
                    # new_file.close()

                    self._getGmailLabelId(CONSTANT.GMAIL_LABEL_PROCESSED)

                    #Mark message as processed (omit for development purposes)
                    self._labelEmailMessageProcessed(emailMessageId,label_id)

            return CONSTANT.SUCCESS, datetime.datetime.fromtimestamp(int(message['internalDate'])/1000).strftime('%c')

        except errors.HttpError as err:
            self.logger.log('gmailController.processEmailMessage error: {}'.format(err),level=logging.ERROR)
            return CONSTANT.FAIL, datetime.datetime.utcnow().strftime('%c')

            self.logger.log('gmailController.checkInBoxAn error: {}'.format(err), level=logging.ERROR)


    def _labelEmailMessageProcessed(self,emailMessageId,emailLabel):
        try:
            bodyText = {'removeLabelIds': [emailLabel, self.gmailLabelIdIncoming]
                , 'addLabelIds': [self.gmailLabelIdProcessed]}

            self.service.users().messages().modify(userId=self.emailAddress,id=emailMessageId,body=bodyText).execute()
            return
        except errors.HttpError as err:
            self.logger.log('gmailController._labelEmailMessageProcessed error: {}'.format(err), level=logging.ERROR)

    def _getGmailLabelId(self,labelName):
        if len(self.labels) == 0:
            try:
                response = self.service.users().labels().list(userId=self.emailAddress).execute()
                self.labels = response['labels']

            except errors.HttpError as err:
                self.logger.log('gmailController._getGmailLabelId error: {}'.format(err), level=logging.ERROR)

       #look through collection for match
        for label in self.labels:
            if label['name'] == labelName:
                self.logger.log('found label name/id match: %s/%s' % (label['name'], label['id']),
                                level=logging.DEBUG)
                return label['id']
        self.logger.log('no label found matching name: %s' % (labelName), level=logging.ERROR)
        return None

    def _getGmailLabelName(self,labelId):
        if len(self.labels) == 0:
            try:
                response = self.service.users().labels().list(userId=self.emailAddress).execute()
                self.labels = response['labels']

            except errors.HttpError as err:
                self.logger.log('gmailController._getGmailLabelId error: {}'.format(err), level=logging.ERROR)

       #look through collection for match
        for label in self.labels:
            if label['id'] == labelId:
                self.logger.log('found label name/id match: %s/%s' % (label['name'], label['id']),
                                level=logging.DEBUG)
                return label['name']
        self.logger.log('no label found matching name: %s' % (labelId), level=logging.ERROR)
        return None

    def purgeInbox(self):
        try:
            self.logger.log(('Purging inbox, removing message matching filter: %s'%CONSTANT.INBOX_PURGING_FILTER)
                            , level=logging.INFO)
            emailMessagesForPurging = self.checkInBox(query=CONSTANT.INBOX_PURGING_FILTER)
            self.logger.log(('%s inbox has %s messages matching filter %s' % (CONSTANT.EMAIL_ADDRESS_TO_MONITOR
                             , emailMessagesForPurging.__len__(),CONSTANT.INBOX_PURGING_FILTER)), level=logging.INFO)
            # process inbox
            for message in emailMessagesForPurging:
                responseCode = self._trashMessage(message['id'])
                if responseCode:
                    self.logger.log('Successfully trashed message with ID %s' %
                                    (message['id'])
                                    , level=logging.DEBUG)
                else:
                    self.logger.log('Error trashing message with ID %s' %
                                    (message['id'])
                                    , level=logging.ERROR)
        except errors.HttpError as err:
            self.logger.log('gmailController.purgeInbox error: {}'.format(err), level=logging.ERROR)

    def _trashMessage(self,messageId):
        try:
            return self.service.users().messages().trash(userId=self.emailAddress,id=messageId).execute()
        except errors.HttpError as err:
            self.logger.log('gmailController._getGmailLabelId error: {}'.format(err), level=logging.ERROR)

    def SendMessage(self, message):
        """Send an email message.

        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.

        Returns:
          Sent Message.
        """
        try:

            mmm = (self.service.users().messages().send(userId=self.emailAddress, body=message).execute())
            print('Message Id: %s' % mmm['id'])
            return mmm
        except Exception as err:
            print('An error occurred: %s' % err)

    def CreateMessage(self,sender, to, subject, message_text):
        """Create a message for an email.

        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def CreateMessageWithAttachment(self,sender, to, subject, message_text, file_dir,filename):

        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        file_dir = file_dir
        filename = filename
        with open(os.path.join(file_dir, filename), "rb") as attachment:
            # The content type "application/octet-stream" means that a MIME attachment is a binary file
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode to base64
        encoders.encode_base64(part)

        # Add header
        part.add_header(
            "Content-Disposition",
            "attachment; filename={f}".format(f=filename)
        )

        # Add attachment to your message and convert it to string
        message.attach(part)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


