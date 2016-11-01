import boto3
from boto.s3.connection import S3Connection
import json
import urllib2
import csv
import dateutil.parser
import sys
import xml.etree.ElementTree as ET
reload(sys)
sys.setdefaultencoding('utf-8')




def main():
	print "here"
	client = boto3.client('s3')
	#response = client.list_objects(Bucket='bysykkel-lyckander')
	#print response

	f = open('data-utentittel.csv', 'wt')
	csv_file = csv.writer(f)


	conn = S3Connection()
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('bysykkel-lyckander')

	stations_meta_data = readStations()

	for document in bucket.objects.all():
		name = document.key
		data_file = s3.Object('bysykkel-lyckander', name).get()['Body']
		content = json.load(data_file)
		date_time = content['updated_at']
		hour = dateutil.parser.parse(date_time).hour
		weekday = dateutil.parser.parse(date_time).weekday()

		print date_time
		print len(content['stations'])
		
		for station in content['stations']:
			id = station['id']
			availability = station['availability']
			locks = availability['locks']
			bikes = availability['bikes']
			
			if id in stations_meta_data.keys():
				station_meta_data = stations_meta_data[id]
				#title = station_meta_data['title']
				nr_of_locks = station_meta_data['nr_of_locks']
				lat = station_meta_data['lat']
				lon = station_meta_data['lon']
				masl = station_meta_data['masl']
				csv_file.writerow( (hour, weekday, id, lat, lon, masl, nr_of_locks, locks, bikes) )
			else: 
				print "wrong"

	f.close()


	
def readStations(): 
	response = urllib2.urlopen('https://oslobysykkel.no/api/v1/stations.json')
	content = json.load(response)
	stations = {}

	for station in content['stations']:
		station_meta_data = {}
		id = station['id']
		station_meta_data['title'] = station['title']
		station_meta_data['nr_of_locks'] = station['number_of_locks']
		center = station['center']
		lat = center['latitude']
		lon = center['longitude']
		station_meta_data['lat'] = lat
		station_meta_data['lon'] = lon

		station_meta_data['masl'] = readMASL(lat, lon)

		stations[id] = station_meta_data
	return stations
	
def readMASL(lat, lon):
	response = urllib2.urlopen('http://openwps.statkart.no/skwms1/wps.elevation?request=Execute&service=WPS&version=1.0.0&identifier=elevation&datainputs=[lat=' + str(lat) + ';lon=' + str(lon) + ';epsg=4326]')

	tree = ET.parse(response)
	root = tree.getroot()

	process_outputs = root.find('{http://www.opengis.net/wps/1.0.0}ProcessOutputs')
	outputs = process_outputs.findall('./{http://www.opengis.net/wps/1.0.0}Output')
	
	for output in outputs:
		value = output.find('{http://www.opengis.net/ows/1.1}Identifier').text
		if value == 'elevation':
			data = output.find('{http://www.opengis.net/wps/1.0.0}Data')
			elevation = output.findall('[@uom="m.a.s.l."]')
			meter = data.find('{http://www.opengis.net/wps/1.0.0}LiteralData').text
			print meter
			return meter

main()