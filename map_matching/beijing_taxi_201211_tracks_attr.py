import psycopg2
import re,lib

fromdate = (2012,11,1)
todate = (2012,11,4)
tbnames = lib.dates_to_tbnames(fromdate,todate)

class tracks_attr:
	def __init__(self):
		self.conn = psycopg2.connect(database = 'beijing_taxi_201211', user = 'postgres', password = 'zq600991')
		print 'postgres successfully connected'
	def track_get(self,track_id,track_tbname):
		track_coords = []
		track_get_sql = 'select id,cuid_count,st_astext(track_geom) as geom,track_desc,oorc from ' + track_tbname + ' where id = ' + str(track_id)
		cursor = self.conn.cursor()
		cursor.execute(track_get_sql)
		track_results = cursor.fetchone()

		track_cuid_count = track_results[1]
		track_oorc = track_results[4]
		track_coords_list = re.search('^LINESTRING\((.*)\)$',track_results[2]).group(1).split(',')
		for track_coord in track_coords_list:
			track_coord_log = float(track_coord.split(' ')[0])
			track_coord_lat = float(track_coord.split(' ')[1])
			track_coords.append([track_coord_log,track_coord_lat])

		return track_cuid_count,track_oorc,track_coords
	def track_total_length(self,track_coords):
		total_length = 0
		for i in range(1,len(track_coords)):
			length = lib.coords_2_km(track_coords[i-1],track_coords[i])	
			total_length = total_length + length
		return total_length
	def track_max_length(self,track_coords):
		max_length = 0
		for i in range(1,len(track_coords)):
			length = lib.coords_2_km(track_coords[i-1],track_coords[i])
			if length > max_length:
				max_length = length
		return max_length
	def track_total_tracks_cuid_count(self,track_cuid_count,track_tbname):
		total_tracks_cuid_count_sql = 'select count(*) from ' + track_tbname + ' where cuid_count = ' + str(track_cuid_count)
		cursor = self.conn.cursor()
		cursor.execute(total_tracks_cuid_count_sql)
		total_tracks_cuid_count = cursor.fetchone()[0]

		o_total_tracks_cuid_count_sql = 'select count(*) from ' + track_tbname + ' where cuid_count = ' + str(track_cuid_count) + ' and oorc = ' + str(1)
		cursor.execute(o_total_tracks_cuid_count_sql)
		o_total_tracks_cuid_count = cursor.fetchone()[0]

		c_total_tracks_cuid_count_sql = 'select count(*) from ' + track_tbname + ' where cuid_count = ' + str(track_cuid_count) + ' and oorc = ' + str(0)
		cursor.execute(c_total_tracks_cuid_count_sql)
		c_total_tracks_cuid_count = cursor.fetchone()[0]
		return total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count
	def create_table(self,track_attr_tbname):
		truncate_table_sql = r'truncate table ' + track_attr_tbname
		cursor = self.conn.cursor()
		cursor.execute(truncate_table_sql)
		print track_attr_tbname,'truncated'
		create_table_sql = r'create table if not exists ' + track_attr_tbname + r"""(
			track_id int not null,
			cuid_count int not null,
			track_oorc int not null,
			total_length float not null,
			max_length float not null,
			total_tracks_cuid_count int not null,
			o_total_tracks_cuid_count int not null,
			c_total_tracks_cuid_count int not null,
			primary key(track_id));"""
		cursor.execute(create_table_sql)
		self.conn.commit()
	def insert_track_attr(self,track_attr_tbname,track_id,track_cuid_count,track_oorc,total_length,max_length,total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count):
		insert_track_attr_sql = r'insert into ' + track_attr_tbname + r'(track_id,cuid_count,track_oorc,total_length,max_length,total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count) values (%s,%s,%s,%s,%s,%s,%s,%s);'
		cursor = self.conn.cursor()
		cursor.execute(insert_track_attr_sql,(track_id,track_cuid_count,track_oorc,total_length,max_length,total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count))
		self.conn.commit()
	def track_total_tracks(self,track_tbname):
		total_tracks_sql = r'select count(*) from ' + track_tbname
		cursor = self.conn.cursor()
		cursor.execute(total_tracks_sql)
		total_tracks = cursor.fetchone()[0]
		return total_tracks
tracks_attr_instance = tracks_attr()

for tbname in tbnames:
	tbname_suffix = tbname.split('_')[1]
	track_tbname = 'taxi_tracks_occupied_crusing_' + tbname_suffix
	track_attr_tbname = 'taxi_tracks_attr_' + tbname_suffix

        tracks_attr_instance.create_table(track_attr_tbname)
	
	total_tracks = tracks_attr_instance.track_total_tracks(track_tbname)
	track_cuid_count_pre = 1
	total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count = tracks_attr_instance.track_total_tracks_cuid_count(track_cuid_count_pre,track_tbname)

	for track_id in range(1,total_tracks+1):

		print tbname_suffix,track_id

		track_cuid_count,track_oorc,track_coords = tracks_attr_instance.track_get(track_id,track_tbname)

		if track_cuid_count != track_cuid_count_pre:
			track_cuid_count_pre = track_cuid_count
			total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count = tracks_attr_instance.track_total_tracks_cuid_count(track_cuid_count,track_tbname)

		total_length = tracks_attr_instance.track_total_length(track_coords)
		max_length = tracks_attr_instance.track_max_length(track_coords)
		
		tracks_attr_instance.insert_track_attr(track_attr_tbname,track_id,track_cuid_count,track_oorc,total_length,max_length,total_tracks_cuid_count,o_total_tracks_cuid_count,c_total_tracks_cuid_count)
