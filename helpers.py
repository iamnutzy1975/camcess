from GoogleAuth.BaseGoogleService import BaseGoogleService
from GoogleAuth.ServiceAccountGoogleAuth import ServiceAccountGoogleAuth
from GoogleAuth.ClientSecretGoogleAuth import ClientSecretGoogleAuth
from googleapiclient.errors import HttpError
from googleapiclient.errors import HttpError
from oauth2client import file
from oauth2client import tools
from oauth2client import client
import argparse
import constants as CONSTANT
import re
import datetime

def getGoogleService(secretFile,scope,apiName,apiVersion):
	secretFileType = 'user'
	searchSecretFile = open(secretFile, "r")
	for line in searchSecretFile.readlines():
		if '"type": "service_account"' in line: secretFileType = 'service'
		searchSecretFile.close()
	try:
		
		if secretFileType == 'service':
			auth = ServiceAccountGoogleAuth(secretFile, scope=scope)
			serviceSetup = BaseGoogleService(api_name=apiName, api_version=apiVersion, google_auth=auth)
			auth.authorize()
			return serviceSetup.getService()
		else:
			parser = argparse.ArgumentParser(
				formatter_class=argparse.RawDescriptionHelpFormatter,
				parents=[tools.argparser])
			flags = parser.parse_args([])
			flow = client.flow_from_clientsecrets(
				secretFile, scope=scope,
				message=tools.message_if_missing(secretFile,))
			storage = file.Storage(apiName + '.dat')
			credentials = storage.get()
			if credentials is None or credentials.invalid:
				tools.run_flow(flow, storage, flags)
			auth = ClientSecretGoogleAuth(secretFile,apiName + '.dat',scope=scope)
			serviceSetup = BaseGoogleService(api_name=apiName, api_version=apiVersion, google_auth=auth)
			auth.authorize()
			return serviceSetup.getService()
		
	except HttpError as err:
		raise err

def findDataSourceKey(filename):
		for key in sorted(CONSTANT.DATA_SOURCE_MAP.iterkeys()):
			result = re.match(CONSTANT.DATA_SOURCE_MAP[key][CONSTANT.ATTACHMENT_REGEX_PATTERN],filename)
			if result: return key
		return None

def cleanCSV(filename):
	cleanedFileName = filename.replace('.csv','_cleaned.csv')
	with open(filename, 'r') as originalFile:
		with open(cleanedFileName, 'w') as cleanedFile:
			originalFile.next()  # skip header line
			for line in originalFile:
				cleanedFile.write(line)
	return cleanedFileName

def bucketKeyToLocalFileName(key):
	return key.key.replace('/','-')

def localFileNameToBucketKey(filename):
	return filename.replace( '-','/')

def removeFilePathFromKey(key):
	return key.key.split('/')[-1]

def excelTimeToString(excelTime, format='%Y-%m-%d %H:%M:%S'):
		dt = datetime.datetime(1899,12,30) + datetime.timedelta(days=excelTime)
		return dt.strftime(format)

def excelTextValueToInt(excelValue):
	#return str(excelValue).split('.')[0]
	try:
		retval = ('%d'%excelValue)
	except:
		retval = ''
	return retval

def excelTextValueToFloat(excelValue):
	try:
		retval = ('%f' % excelValue)
	except:
		retval = ''
	return retval

def stringValueCleaner(value):
	return value.strip()

	
	
