import kMeans
import lib
from datetime import datetime
import time

pickup_all_day_file_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup_all_day/'
pickup_all_day_filename = 'pickup_20121101.txt'
pickup_all_day_file = pickup_all_day_file_dir + pickup_all_day_filename


pickup_according_time_file_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup_according_time/'

def pickup_select_according_time(start_time_string,end_time_string):
	pickup_all_day_f = open(pickup_all_day_file,'r')

	start_time_datetime = datetime.strptime(start_time_string,'%Y-%m-%d %H:%M:%S')
	end_time_datetime = datetime.strptime(end_time_string,'%Y-%m-%d %H:%M:%S')
	start_time_timestamp = time.mktime(time.strptime(start_time_string,'%Y-%m-%d %H:%M:%S'))
	end_time_timestamp = time.mktime(time.strptime(end_time_string,'%Y-%m-%d %H:%M:%S'))

	pickup_according_time_f = open(pickup_according_time_file_dir + 'pickup_' + pickup_all_day_filename.split('.')[0].split('_')[1] + '_' + str(start_time_datetime.hour) + '-' + str(start_time_datetime.minute) + '_' + str(end_time_datetime.hour) + '-' + str(end_time_datetime.minute) + '.txt','w')

	pickup_number_according_time = 0
	for line in pickup_all_day_f.readlines():
		attrs = lib.parse_pickup_line(line)
		pickup_time_string = attrs['pickup_time']
		pickup_time_datetime = datetime.strptime(pickup_time_string,'%Y-%m-%d %H:%M:%S')
		pickup_time_timestamp = time.mktime(time.strptime(pickup_time_string,'%Y-%m-%d %H:%M:%S'))
		if start_time_timestamp <= pickup_time_timestamp < end_time_timestamp:
			#print line
			pickup_number_according_time = pickup_number_according_time + 1
			pickup_according_time_f.write(line)
	
	pickup_all_day_f.close()
	print 'the number of pickup point between ' + start_time_string + ' and ' + end_time_string + ' is ' + ':', pickup_number_according_time


#pickup_select_according_time('2012-11-1 19:00:00','2012-11-1 19:30:00')
time_interval_user_defined_timestamp = time.mktime(time.strptime('2012-11-1 00:30:00','%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime('2012-11-1 00:00:00','%Y-%m-%d %H:%M:%S'))
time_interval_one_day_timestamp = time.mktime(time.strptime('2012-11-2 00:00:00','%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime('2012-11-1 00:00:00','%Y-%m-%d %H:%M:%S'))
start_time = '2012-11-1 00:00:00'
for i in range(int(time_interval_one_day_timestamp/time_interval_user_defined_timestamp)):
	start_time_timestamp = time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
	end_time_timestamp = start_time_timestamp + time_interval_user_defined_timestamp
	end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_time_timestamp))
	start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time_timestamp))
	pickup_select_according_time(start_time,end_time)
	start_time = end_time
