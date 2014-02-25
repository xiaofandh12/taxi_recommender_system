import json
import time
import os
import lib

proc_output_dir = "/home/donghao/ITS_project/taxi_finder/data_geojson/"
proc_input_dir = "/home/donghao/ITS_project/taxi_finder/data_by_cuid_count/"
fromdate = (2012,11,1)
todate = (2012,11,4)
tbnames = lib.dates_to_tbnames(fromdate,todate)

class Geojson:
	def cuid_start_callback(self,cuid):
		self.jdict = dict()
		self.jdict["type"] = "FeatureCollection"
		self.features = list()
		self.coordnum = 0
		self.geo = dict()
		self.geo["type"] = "LineString"
		self.coords = list()
		self.descs = list()
	def cuid_end_callback(self,cuid):
		self.jdict["features"] = self.features
		#if not os.path.exists(proc_output_dir + tbname + '/'):
		#	os.mkdir(proc_output_dir + tbname + '/')
		self.write_to_file(proc_output_dir + prefix + '_' + str(CUID_count) + '_all' + ".json")
	def line_callback(self,line):
		if line != '':
			attrs = lib.parse_line(line)
		
			taxi_status_tx = str(attrs['taxi_status'])
			time_tx = attrs['time']
			speed_tx = str(attrs['speed'])
			head_tx = str(attrs['head'])
		
			coord = [attrs['lon'],attrs['lat']]
			self.coords.append(coord)
			self.descs.append({"t":time_tx,"h":head_tx,"s":speed_tx,"taxi_status":taxi_status_tx})
			self.coordnum = self.coordnum + 1
		
		if line == '':	
			self.geo["coordinates"] = self.coords
			self.features.append({"geometry":self.geo, "properties":{"desc":self.descs}})
	
	def write_to_file(self,filename):
		with open(filename, "w") as f:
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
		#for line in open(input_dir + str(CUID_count) + '/' + str(CUID_count) + '.txt'):
		while True:
			line = inf.readline()
			geojson.line_callback(line)
			if line == '':
				break
		geojson.cuid_end_callback(CUID_count)
		print proc_output_dir + tbname + '/' + prefix + '_' + str(CUID_count) + '_all'+ '.json',' completed'
