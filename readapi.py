import urllib2
import boto3
import datetime

def read(event, context): 
	response = urllib2.urlopen('https://oslobysykkel.no/api/v1/stations/availability')
	html = response.read()

	s3 = boto3.resource('s3')
	timestamp = datetime.datetime.now().isoformat()
	filename = timestamp+'.json'
	s3.Bucket('bysykkel-lyckander').put_object(Key=filename, Body=html)
	return "Ok"