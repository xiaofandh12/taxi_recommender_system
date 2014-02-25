#coding=utf-8
import graph
import psycopg2,psycopg2.extras
import db
import lib
from time import time, localtime, strftime

def track_pickup(track_id, track_geom, track_desc, track_oorc):
        pickup_dict = {}

        pickup_dict['track_id'] = track_id

        track_geom_lonlats = graph.geom2lonlats(track_geom)
        pickup_lonlat = track_geom_lonlats[0]
        pickup_dict['pickup_lonlat'] = pickup_lonlat

        pickup_time = track_desc.split(',')[0]
        pickup_dict['pickup_time'] = pickup_time

        pickup_dict['track_oorc'] = track_oorc
        return pickup_dict

from_date = (2012,11,1)
to_date = (2012,11,30)
tbnames_suffix = lib.dates_to_tbnames(from_date, to_date)
tracks_tbname_prefix = 'taxi_tracks_occupied_crusing_'
paths_tbname_prefix = 'taxi_paths_occupied_crusing_st_'

tracks_tbname = [tracks_tbname_prefix + tbname_suffix.split('_')[1] for tbname_suffix in tbnames_suffix]
paths_tbname = [paths_tbname_prefix + tbname_suffix.split('_')[1] for tbname_suffix in tbnames_suffix]

paths_tb_length = len(paths_tbname)

for i in range(paths_tb_length): 
	gw = graph.new_gw()
	track_reader = db.TrackReader(tbname = tracks_tbname[i], limit = 10000, offset = 0)
	path_reader = db.PathReader(tbname = paths_tbname[i], gw = gw, limit = 10000, offset = 0)

	pickup_file = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup' + '_' + tbnames_suffix[i].split('_')[1] + '.txt'
	pickup_f = open(pickup_file, 'w')
	
	start_time = time()
	pickup_num = 0
	while True:
		path_tid,path_way_ids = path_reader.fetch_one()
		if path_tid == None:
			break
		track_id, track_cuid_count, track_geom, track_desc, track_oorc = track_reader.fetch_track_by_id(path_tid)
		
		pickup_dict = {}	
		pickup_dict = track_pickup(track_id, track_geom, track_desc, track_oorc)
		path_way_id = path_way_ids.split(',')[0]
		pickup_dict['path_way_edge'] =	gw.st[int(path_way_id)]
		
		if pickup_dict['track_oorc'] == 0:
			#pick_up点是occupied track的起始点，所以当track的track_oorc = 0时，就跳过
			continue
		else:
			#proj_p2edge(self, p_lonlat, edge)(graph.py中GraphWrapper类的方法)返回关于p_lonlat在edge上投影的一些信息
			pickup_proj_lonlat_dict = gw.proj_p2edge(pickup_dict['pickup_lonlat'], pickup_dict['path_way_edge'])
			pickup_dict['pickup_proj_lonlat'] = pickup_proj_lonlat_dict['proj_lonlat']
			pickup_dict['path_way_edge'] = [path_way_id, gw.st[int(path_way_id)]]
			#pickup_dict = {'pickup_lonlat':, 'pickup_proj_lonlat':, 'pickup_time':, 'track_id':, 'path_way_edge':, 'track_oorc':}
			pickup_f.write(str(pickup_dict['track_id']) + ',' + str(pickup_dict['pickup_lonlat'][0]) + ',' + str(pickup_dict['pickup_lonlat'][1]) + ',' + str(pickup_dict['pickup_proj_lonlat'][0]) + ',' + str(pickup_dict['pickup_proj_lonlat'][1]) + ',' + str(pickup_dict['pickup_time']) + ',' + str(pickup_dict['path_way_edge'][0]) + ',' + str(pickup_dict['path_way_edge'][1][0]) + ',' + str(pickup_dict['path_way_edge'][1][1]) + ',' + str(pickup_dict['track_oorc']) + '\n')
	
			pickup_num = pickup_num + 1
			print 'path_tid:' + str(path_tid).ljust(20),'track_cuid_count:' + str(track_cuid_count).ljust(20),'pickup_num:' + str(pickup_num).ljust(20)	
	end_time = time()
	print tbnames_suffix[i].split('_')[1],'dropoff select program start at:',strftime('%y-%m-%d %H:%M:%S',localtime(start_time))
	print tbnames_suffix[i].split('_')[1],'dropoff select program end at:',strftime('%y-%m-%d %H:%M:%S',localtime(end_time))
