import psycopg2
import sys
import time
import lib
import os

#proc_input_dir = '/home/donghao/ITS_project/taxi_finder/data/data_by_cuid_count/'
proc_input_dir = '/home/donghao/ITS_project/taxi_finder/data/data_by_cuid_count_filter_1/'
fromdate = (2012,11,1)
todate = (2012,11,4)
tbnames = lib.dates_to_tbnames(fromdate,todate)
#tbnames = ['tb_20121101']

class Tracks2Postgres:
	def __init__(self):
		self.conn = psycopg2.connect(database = 'beijing_taxi_201211',user = 'postgres',password = 'zq600991')
		print 'postgres successfully connected'
	def cuid_start_callback(self,cuid):
		self.cuid = cuid
		self.coords = list()
		self.descs = list()
		self.OorC = ''
		self.pre_occupied = '-1'
	def cuid_end_callback(self,cuid):
		pass
	def line_callback(self,line,postgres_tbname):
		if line != '':
			attrs = lib.parse_line(line)
		
			#taxi_status_tx = str(attrs['taxi_status'])
			time_tx = attrs['time']
			#speed_tx = str(attrs['speed'])
			#head_tx = str(attrs['head'])
			coord = [attrs['lon'],attrs['lat']]
			if (self.pre_occupied != attrs['taxi_status']) and ((self.pre_occupied == '0') or (self.pre_occupied == '1')):
				#self.coords.append(coord)
				#self.descs.append({'t':time_tx,'h':head_tx,'s':speed_tx,'taxi_status':taxi_status_tx})
				#self.descs.append({'t':time_tx})
				self.OorC = self.pre_occupied
				if len(self.coords) > 1:
					self.insert_track(postgres_tbname)
				self.coords = list()
				self.descs = list()
				self.OorC = ''
				self.pre_occupied = attrs['taxi_status']
			if (attrs['taxi_status'] == '0') or (attrs['taxi_status'] == '1'):
                                self.coords.append(coord)
                                #self.descs.append({'t':time_tx,'h':head_tx,'s':speed_tx,'taxi_status':taxi_status_tx})
				self.descs.append({'t':time_tx})
                                self.pre_occupied = attrs['taxi_status']
		if (line == '') and (len(self.coords) > 1):
			self.OorC = self.pre_occupied
			self.insert_track(postgres_tbname)
		elif (line == '') and (len(self.coords) <= 1):
			pass
	def insert_track(self,postgres_tbname):
		cursor = self.conn.cursor()
	
		coords_sql = 'LINESTRING('
		coord = self.coords[0]
		coords_sql = coords_sql + str(coord[0]) + ' ' + str(coord[1])
		for i in range(1, len(self.coords)):
			coord = self.coords[i]
			coords_sql = coords_sql + ',' + str(coord[0]) + ' ' + str(coord[1])
		coords_sql = coords_sql + ')'
		
		descs_sql = ''
		for desc in self.descs:#self.descs is a list,desc is a dictionary.
			#descs_sql = descs_sql + desc['t'] + ' ' + desc['h'] + ' ' + desc['s'] + ' ' + desc['taxi_status'] + ','
			descs_sql = descs_sql + desc['t'] + ','
		descs_sql = descs_sql + ''
		
		sql = r'insert into '+ postgres_tbname + r' (CUID_count, TRACK_GEOM, TRACK_DESC, OorC) values (%s,%s,%s,%s);'
		cursor.execute(sql, (self.cuid, coords_sql,descs_sql,self.OorC))
		self.conn.commit()
	def create_table(self,postgres_tbname):
		cursor = self.conn.cursor()
		sql_truncate_table = r"TRUNCATE TABLE " + postgres_tbname + r" RESTART IDENTITY"
		cursor.execute(sql_truncate_table)
		print postgres_tbname, 'successfully truncated.'
		sql_create_table = r"CREATE TABLE IF NOT EXISTS " + postgres_tbname + r"""(
			ID SERIAL,
			CUID_count int not null,
			TRACK_GEOM geometry not null,
			TRACK_DESC text not null,
			OorC int not null,		
			primary key(id));"""
		cursor.execute(sql_create_table)
		self.conn.commit()
		print postgres_tbname, 'successfully created.'
tracks2postgres = Tracks2Postgres()

for tbname in tbnames:
	postgres_tbname = 'taxi_tracks_occupied_crusing_' + tbname.split('_')[1]
	tracks2postgres.create_table(postgres_tbname)
	input_dir = proc_input_dir + tbname +'/'
	for CUID_count in range(1,len(os.listdir(input_dir))+1):
	#for CUID_count in range(1,2):
		print tbname,CUID_count
		
		tracks2postgres.cuid_start_callback(CUID_count)
		inf = open(input_dir + str(CUID_count) + '.txt', 'r')
		while True:
			line = inf.readline()
			tracks2postgres.line_callback(line,postgres_tbname)
			if line == '':
				break
		print input_dir + str(CUID_count) + '.txt', 'completed'
