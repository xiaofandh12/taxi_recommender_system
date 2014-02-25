import graph
import db
from time import time,strftime,localtime
import lib

def track_dropoff(track_id, track_geom, track_desc, track_oorc):
	dropoff_dict = {}
	
	dropoff_dict['track_id'] = track_id
	
	track_geom_lonlats = graph.geom2lonlats(track_geom)
	track_geom_lonlats_length = len(track_geom_lonlats)
	dropoff_lonlat = track_geom_lonlats[track_geom_lonlats_length - 1]
	dropoff_dict['dropoff_lonlat'] = dropoff_lonlat

	dropoff_time = track_desc.split(',')[track_geom_lonlats_length - 1]
	dropoff_dict['dropoff_time'] = dropoff_time

	dropoff_dict['track_oorc'] = track_oorc
	return dropoff_dict

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

	dropoff_file = '/home/donghao/ITS_project/taxi_finder/data/data_dropoff/dropoff' + '_' +tbnames_suffix[i].split('_')[1]
	dropoff_f = open(dropoff_file, 'w')

	start_time = time()
	dropoff_num = 0
	while True:
		path_tid, path_way_ids = path_reader.fetch_one()
		if path_tid == None:
			break
		track_id, track_cuid_count, track_geom, track_desc, track_oorc = 		track_reader.fetch_track_by_id(path_tid)

		dropoff_dict = {}
		dropoff_dict = track_dropoff(track_id, track_geom, track_desc, track_oorc)
		if dropoff_dict['track_oorc'] == 0:
			continue
		else:
			path_way_ids_list = path_way_ids.split(',')
			path_way_ids_list_length = len(path_way_ids_list)
			path_way_id = path_way_ids_list[path_way_ids_list_length - 1]
			#path_way_ids_list = ['674',''] track_id = 16;In this situation, 	path_way_ids_list[path_way_ids_list_length-1] = ''
			if path_way_id == '':
				path_way_id = path_way_ids_list[path_way_ids_list_length - 2]
			dropoff_dict['path_way_edge'] = gw.st[int(path_way_id)]

			dropoff_proj_lonlat_dict = gw.proj_p2edge(dropoff_dict['dropoff_lonlat'], 	dropoff_dict['path_way_edge'])
			dropoff_dict['dropoff_proj_lonlat'] = dropoff_proj_lonlat_dict['proj_lonlat']
			dropoff_dict['path_way_edge'] = [path_way_id, gw.st[int(path_way_id)]]
			dropoff_f.write(str(dropoff_dict['track_id']) + ',' + str(dropoff_dict['dropoff_lonlat'][0]) + ',' + str(dropoff_dict['dropoff_lonlat'][1]) + ',' + str(dropoff_dict['dropoff_proj_lonlat'][0]) + ',' + str(dropoff_dict['dropoff_proj_lonlat'][1]) + ',' + str(dropoff_dict['dropoff_time']) + ',' + str(dropoff_dict['path_way_edge'][0]) + ',' + str(dropoff_dict['path_way_edge'][1][0]) + ',' + str(dropoff_dict['path_way_edge'][1][1]) + ',' + str(dropoff_dict['track_oorc']) + '\n')
			dropoff_num = dropoff_num + 1
			print 'path_tid:' + str(path_tid).ljust(20),'track_cuid_count:' + str(track_cuid_count).ljust(20),'dropoff_num:' + str(dropoff_num).ljust(20)

	end_time = time()

	print tbnames_suffix[i].split('_')[1],'dropoff select program start at:',strftime('%y-%m-%d %H:%M:%S',localtime(start_time))
	print tbnames_suffix[i].split('_')[1],'dropoff select program end at:',strftime('%y-%m-%d %H:%M:%S',localtime(end_time))
