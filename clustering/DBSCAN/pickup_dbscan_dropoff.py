import time
from datetime import datetime
import os.path

def pickup_dbscan_dropoff(pickup_dbscan_dir,pickup_dbscan_filename):
	#put the relate information of dropoffs in 20121101 into a dictionary(dropoffs)
	dropoff_file_20121101 = '/home/donghao/ITS_project/taxi_finder/data/data_dropoff/dropoff_20121101'
	dropoff_f_20121101 = open(dropoff_file_20121101,'r')
	dropoffs = {}
	for line in dropoff_f_20121101.readlines():
	        curLine = line.strip().split(',')
	        dropoff_lonlat = map(float,[curLine[3],curLine[4]])
	        dropoff_lonlat.append(curLine[5])
	        dropoffs.setdefault(curLine[0],[]).append(dropoff_lonlat[0])
	        dropoffs[curLine[0]].append(dropoff_lonlat[1])
	        dropoffs[curLine[0]].append(dropoff_lonlat[2])

	#select the dropoffs corresponding to pickups(dbscan's result)
	pickup_dbscan_file = pickup_dbscan_dir + pickup_dbscan_filename
	pickup_dbscan_dropoff_file = pickup_dbscan_dir + pickup_dbscan_filename.split('.txt')[0] + '_dropoff.txt'
	
	pickup_dbscan_f = open(pickup_dbscan_file,'r')
	pickup_dbscan_dropoff_f = open(pickup_dbscan_dropoff_file,'w')
	for line in pickup_dbscan_f.readlines():
		curLine = line.strip().split(',')
		pickup_dbscan_dropoff_f.write(curLine[0] + ',' + curLine[1] + ',' + str(dropoffs[curLine[1]][0]) + ',' + str(dropoffs[curLine[1]][1]) + ',' + dropoffs[curLine[1]][2] + '\n')
	print 'pickup dbscan dropoff saved in:',pickup_dbscan_dropoff_file

pickup_dbscan_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/'	
#pickup_dbscan_filename = 'dbscan_20121101_8-0_8-30_0.3_4_2_4.txt'
#pickup_dbscan_dropoff(pickup_dbscan_dir,pickup_dbscan_filename)

time_interval_user_defined_timestamp = time.mktime(time.strptime('2012-11-1 00:30:00','%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime('2012-11-1 00:00:00','%Y-%m-%d %H:%M:%S'))
time_interval_one_day_timestamp = time.mktime(time.strptime('2012-11-2 00:00:00','%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime('2012-11-1 00:00:00','%Y-%m-%d %H:%M:%S'))
start_time_string = '2012-11-1 00:00:00'
for i in range(int(time_interval_one_day_timestamp/time_interval_user_defined_timestamp)):
	pickup_dbscan_filename_prefix = 'dbscan_20121101_'
        start_time_timestamp = time.mktime(time.strptime(start_time_string,'%Y-%m-%d %H:%M:%S'))
        end_time_timestamp = start_time_timestamp + time_interval_user_defined_timestamp
        start_time_string = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time_timestamp))
	end_time_string = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_time_timestamp))
        start_time_datetime = datetime.strptime(start_time_string,'%Y-%m-%d %H:%M:%S')
	end_time_datetime = datetime.strptime(end_time_string,'%Y-%m-%d %H:%M:%S')
	
	e_inside4huan = 0.3
	minpts_inside4huan = 4
	e_outside4huan = 2
	minpts_outside4huan = 4
	pickup_dbscan_filename = pickup_dbscan_filename_prefix + str(start_time_datetime.hour) + '-' + str(start_time_datetime.minute) + '_' + str(end_time_datetime.hour) + '-' + str(end_time_datetime.minute) + '_' + str(e_inside4huan) + '_' + str(minpts_inside4huan) + '_' + str(e_outside4huan) + '_' + str(minpts_outside4huan) + '.txt'
        pickup_dbscan_file = pickup_dbscan_dir + pickup_dbscan_filename
	if os.path.exists(pickup_dbscan_file):
		pickup_dbscan_dropoff(pickup_dbscan_dir,pickup_dbscan_filename)
	else:
		break
        start_time_string = end_time_string
