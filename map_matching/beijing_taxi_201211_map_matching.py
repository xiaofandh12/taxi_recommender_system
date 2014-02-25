#coding=utf-8
import sys
import datetime

import ccgraph as cg
import cctrack as ct
import ccpath as cp
import ccgeojson as cj
import ccdb as cdb

import alg_bn as abn
import alg_st as ast
import alg_iv as aiv
import alg_ut as aut
import alg_uti as auti

import networkx as nx

TRACKS_FROM_ROW = 1
TRACKS_TO_ROW = -1

#METHOD = 'bn'
METHOD = 'st'
#METHOD = 'iv'
#METHOD = 'ut'
#METHOD = 'uti'

algs = {'bn':abn, 'st':ast, 'iv':aiv, 'ut':aut, 'uti':auti}
alg = algs[METHOD]

tbname_suffixs = ['20121102','20121103','20121104']
	
def match(pwd,pawd,gw,track):
	print 'Matching...',
	path = alg.match(gw,track)
	
	if path is not None and path.is_valid():
		print 'p2db...',
		pwd.insert_update(path)
		pawd.insert_update(path, track)
			
		#print 'p2json...',
		#pt2j.write_p_geojson(path)
			
		print 'end...',
		path.summary()
		print ''
		return True
	else:
		print ''
		return False
def mm():
	for tbname_suffix in tbname_suffixs:
       		gw = cg.new_gw()
          	cdb.create_path_occupied_crusing_table(tbname_suffix,method=METHOD)#函数调用的时候，如果第一个参数使用了关键字绑定，后面的参数也必须使用关键字绑定！
        	cdb.create_path_occupied_crusing_table_attr(tbname_suffix,method=METHOD)
        	trd = cdb.new_track_reader_for_purpose(tbname_suffix,purpose='mm')
        	pwd = cdb.new_path_writer_for_method(tbname_suffix,method=METHOD)
        	pawd = cdb.new_path_attr_writer_for_method(tbname_suffix,method=METHOD)
        	#p2tj = cj.new_pt2geojson(method=METHOD)

		print ''
		start_at = datetime.datetime.now()
		print tbname_suffix + (' start at ' + str(start_at) + ' ').center(70, '-')

		print 'preparing...',
		alg.prepare(gw)
		print 'end'
		
		tracks_num = 0
		paths_failed = 0
		max_fetched = TRACKS_TO_ROW - TRACKS_FROM_ROW + 1
		
		start_match_at = datetime.datetime.now()
		print (' start matching at ' + str(start_match_at) + '').center(70, '-')

		while TRACKS_TO_ROW < 0 or trd.fetched_num < max_fetched:
			track = trd.fetch_one()

			if trd.fetched_num % 1000 == 0:
				print 'fetched', trd.fetched_num
			if track is None:
				break

			d_max = 0
        		pre_lonlat = track.rds[0]['gps_lonlat']
        		for i in range(1,len(track.rds)):
            			cur_lonlat = track.rds[i]['gps_lonlat']
          		        d = cg.lonlats2km(pre_lonlat, cur_lonlat)
           		        if d > d_max:
					d_max = d
           	       	        pre_lonlat = cur_lonlat
     			
			if d_max > 3 or track.length() >= 80:
				continue
			else:
				tracks_num += 1
			
			print 'track', str(track.tid).ljust(10),' ',
			if not match(pwd,pawd,gw,track):
				paths_failed += 1
		end_match_at = datetime.datetime.now()
		print(' end matching at ' + str(end_match_at) + ' ').center(70, '-'),'elapsed time',str(end_match_at - start_match_at)
		print 'fetched tracks: %s, paths failed: %s' % (trd.fetched_num, paths_failed)
		print ''.center(70, '-')
		
		#clear()
		end_at = datetime.datetime.now()
		print tbname_suffix + (' end at ' + str(end_at) + ' ').center(70, '-'),'elapsed time',str(end_at - start_at)

def clear():
	print 'clearing...',
	global gw,trd,pwd,pawd#,pt2j
	del gw,trd,pwd,pawd#,pt2j
	print 'end'

if __name__ == "__main__":
	mm()
#	alg.summary.printme()
