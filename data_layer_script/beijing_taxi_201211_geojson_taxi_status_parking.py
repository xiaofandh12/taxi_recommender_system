import json 
import time
import os
import lib

proc_output_dir = '/home/donghao/ITS_project/taxi_finder/data_geojson_taxi_status/'
proc_input_dir = '/home/donghao/ITS_project/taxi_finder/data_by_cuid_count/'
fromdate = (2012,11,1)
todate = (2012,11,4)
tbnames = lib.dates_to_tbnames(fromdate,todate)

class Geojson:
	def cuid_start_callback(self,cuid):
		self.jdict = dict()
		self.jdict['type'] = 'FeatureCollection'
		self.features = list()
		self.coordnum = 0
		self.geo = dict()
		self.geo['type'] = 'LineString'
		self.coords = list()
		self.descs = list()
		self.taxi_status = '2'
		self.pre_taxi_status = '0'
	def cuid_end_callback(self,cuid):
		self.jdict['features'] = self.features
		self.write_to_file(proc_output_dir +'taxi_status_parking/' + prefix + '_' + str(CUID_count) + '_taxi_status_parking' + '.json')
	def line_callback(self,line):
		if line != '':
			attrs = lib.parse_line(line)
		
			taxi_status_tx = str(attrs['taxi_status'])
			time_tx = attrs['time']
			speed_tx = str(attrs['speed'])
			head_tx = str(attrs['head'])
			coord = [attrs['lon'],attrs['lat']]
			
			if self.taxi_status == attrs['taxi_status']:
				self.coords.append(coord)
				self.descs.append({'t':time_tx,'h':head_tx,'s':speed_tx,'taxi_status':taxi_status_tx})	
				self.pre_taxi_status = attrs['taxi_status']
			elif (self.taxi_status != attrs['taxi_status']) and (self.pre_taxi_status == '2'):
				self.coords.append(coord)
				self.descs.append({'t':time_tx,'h':head_tx,'s':speed_tx,'taxi_status':taxi_status_tx})
				self.geo['coordinates'] = self.coords
				self.features.append({'geometry':self.geo,'properties':{'desc':self.descs}})
				self.geo = dict()
				self.geo['type'] = 'LineString'
				self.coords = list()
				self.descs = list()
				self.pre_taxi_status = attrs['taxi_status']

		if (line == '') and (self.coords != []):
			self.geo['coordinates'] = self.coords
			self.features.append({'geometry':self.geo,'properties':{'desc':self.descs}})
		elif (line == '') and (self.coords == []):
			pass
			
	def write_to_file(self,filename):
		with open(filename,'w') as f:
			f.write(json.dumps(self.jdict))
			f.close()
geojson = Geojson()

for tbname in tbnames:
	input_dir = proc_input_dir + tbname + '/'
	prefix = tbname.split('_')[1]
	#for CUID_count in range(1,len(os.listdir(input_dir))+1):
	for CUID_count in range(1,1001):
		print tbname,CUID_count

		geojson.cuid_start_callback(CUID_count)
		inf = open(input_dir + str(CUID_count) + '.txt', 'r')
		while True:
			line = inf.readline()
			geojson.line_callback(line)
			if line == '':
				break
		geojson.cuid_end_callback(CUID_count)
		print proc_output_dir +'taxi_status_parking/' + prefix + '_' + str(CUID_count) + '_taxi_status_parking' + '.json' , 'completed'
