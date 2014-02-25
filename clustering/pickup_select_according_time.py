import kMeans
import lib
from datetime import datetime

pickup_file_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/'
pickup_file = pickup_file_dir + 'pickup_20121101'
pickup_f = open(pickup_file,'r')

def pickup_select_according_time(start_time_string,end_time_string):
	start_time_datetime = datetime.strptime(start_time_string,'%Y-%m-%d %H:%M:%S')
	end_time_datetime = datetime.strptime(end_time_string,'%Y-%m-%d %H:%M:%S')
	pickup_f_according_time = open(pickup_file_dir + 'kMeans/' + 'pickup_' + str(start_time_datetime.hour) + '-' + str(start_time_datetime.minute) + '_' + str(end_time_datetime.hour) + '-' + str(end_time_datetime.minute) + '.txt','w')
	pickup_number_according_time = 0
	for line in pickup_f.readlines():
		attrs = lib.parse_pickup_line(line)
		pickup_time_string = attrs['pickup_time']
		pickup_time_datetime = datetime.strptime(pickup_time_string,'%Y-%m-%d %H:%M:%S')
		if pickup_time_datetime.hour >= start_time_datetime.hour and pickup_time_datetime.hour <= end_time_datetime.hour and pickup_time_datetime.minute >= start_time_datetime.minute and pickup_time_datetime.minute <= end_time_datetime.minute:
			print line
			pickup_number_according_time = pickup_number_according_time + 1
			pickup_f_according_time.write(line)
	print 'the number of pick up point between ' + start_time_string + ' and ' + end_time_string + ' is ' + ':', pickup_number_according_time

pickup_select_according_time('2013-12-1 8:00:00','2013-12-1 8:30:00')
