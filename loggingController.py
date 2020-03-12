import logging
import glob
import json
import time
import constants as CONSTANT
import os
from apSyncFramework.BaseLogger import BaseLogger

class loggingController(BaseLogger):
    '''
    Class to handle logging for application.  Write to logfile specified during instantiation:

    filename: name of log file
    replicateAsConsoleOutput: show messages writting to log file on console as well.
    '''

    def __init__(self, filename,filepath, loggingLevel,replicateAsConsoleOutput=False):
        # check to ensure file path exists
        if os.path.exists(filepath):
            self.logFileExtension = '.log'
            self.logFileDirectory = filepath
            self.loggingLevel = loggingLevel
            self.replicateAsConsoleOutput = replicateAsConsoleOutput
            self._deleteOldLogs()
            
            filenameWithDTStamp = os.path.join(filepath,filename) + time.strftime(CONSTANT.FORMAT_TIMESTAMP_FILENAME) + self.logFileExtension
            logging.basicConfig(filename=filenameWithDTStamp, level=loggingLevel, format='%(asctime)s %(message)s')
            self.log('___________________Application Start_______________', level=loggingLevel)
        else:
            raise Exception('Logging directory (filepath parameter of [%s]) does not exist'%filepath)

    # def __del__(self):
    #     self.log('___________________Application End_________________', level=self.loggingLevel)

    def _ConsolePrint(self, logLevel, message):
        if logLevel >= self.loggingLevel:
            print('%s: %s' % (logging.getLevelName(logLevel), message))

    def log(self, message, **kwargs):
        '''
        writes message to log depends on logging library.
        :param message:  message to log to log file
        :param kwargs: level controls the log level
        :return:
        '''
        msg = message + ' - ' + json.dumps(kwargs)
        log_level = kwargs['level'] if 'level' in kwargs and not kwargs['level'] is None else logging.NOTSET
        if log_level == logging.INFO:
            logging.info(logging.getLevelName(log_level) + ': ' + msg)
            if self.replicateAsConsoleOutput: self._ConsolePrint(log_level, msg)
        elif log_level == logging.DEBUG:
            logging.debug(logging.getLevelName(log_level) + ': ' + msg)
            if self.replicateAsConsoleOutput: self._ConsolePrint(log_level, msg)
        elif log_level == logging.WARN:
            logging.warning(logging.getLevelName(log_level) + ': ' + msg)
            if self.replicateAsConsoleOutput: self._ConsolePrint(log_level, msg)
        elif log_level == logging.ERROR:
            logging.error(logging.getLevelName(log_level) + ': ' + msg)
            if self.replicateAsConsoleOutput: self._ConsolePrint(log_level, msg)
        elif log_level == logging.FATAL:
            logging.critical(logging.getLevelName(log_level) + ': ' + msg)
            if self.replicateAsConsoleOutput: self._ConsolePrint(log_level, msg)
        else:
            logging.info(logging.getLevelName(log_level) + ': ' + msg)
            if self.replicateAsConsoleOutput: self._ConsolePrint(log_level, msg)

    def _deleteOldLogs(self):
        now = time.time()
        logFiles = glob.glob(os.path.join(self.logFileDirectory,'*' + self.logFileExtension))
        for logFile in logFiles:
            # delete file older than 30 days
            if os.stat(logFile).st_ctime < now - 30 * 86400:
            #if os.stat(logFile).st_ctime < now - 30:
                if os.path.isfile(logFile):
                    os.remove(logFile)
