#coding=utf-8
import time
import matplotlib.pyplot as plt

pickup_allday_file = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup_all_day/pickup_20121101.txt'

road_pickup_num = {}
for line in open(pickup_allday_file).readlines():
	curline = line.strip().split(',')
	road_id = int(curline[7])
	road_pickup_num[road_id] = road_pickup_num.setdefault(road_id,0) + 1
print '一天中每段路上pickup点的总数:'
road_num = 0
for road_pickup in sorted(road_pickup_num.items(),key=lambda d:d[1],reverse = False):
	road_num = road_num + 1
	print '共',len(road_pickup_num),'条路','第',road_num,'条路','road id:',road_pickup[0],'	pick up num:',road_pickup[1]

road_pickup_timeinterval_num = {}
time_interval_user_defined_timestamp = time.mktime(time.strptime('2012-11-1 00:10:00','%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime('2012-11-1 00:00:00','%Y-%m-%d %H:%M:%S'))
time_interval_one_day_timestamp = time.mktime(time.strptime('2012-11-2 00:00:00','%Y-%m-%d %H:%M:%S'))-time.mktime(time.strptime('2012-11-1 00:00:00','%Y-%m-%d %H:%M:%S'))
start_time = '2012-11-1 00:00:00'
for i in range(1,int(time_interval_one_day_timestamp/time_interval_user_defined_timestamp)+1):
        print i
        start_time_timestamp = time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
        end_time_timestamp = start_time_timestamp + time_interval_user_defined_timestamp
        end_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(end_time_timestamp))
        start_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start_time_timestamp))
        pickup_allday_f = open(pickup_allday_file,'r')
        for line in pickup_allday_f.readlines():
                curline = line.strip().split(',')
                cur_road_id = int(curline[7])
		road_pickup_timeinterval_num.setdefault(cur_road_id,{})
		road_pickup_timeinterval_num[cur_road_id].setdefault(i,0)
                cur_time_string = curline[5]
                cur_time_timestamp = time.mktime(time.strptime(cur_time_string,'%Y-%m-%d %H:%M:%S'))
                if start_time_timestamp <= cur_time_timestamp <= end_time_timestamp:
			road_pickup_timeinterval_num[cur_road_id][i] = road_pickup_timeinterval_num[cur_road_id][i] + 1
        pickup_allday_f.close()
        start_time = end_time

road_pickup_timeinterval_num_35663_x = road_pickup_timeinterval_num[35663].keys()
road_pickup_timeinterval_num_35663_y = road_pickup_timeinterval_num[35663].values()
road_pickup_timeinterval_num_6137_x = road_pickup_timeinterval_num[6137].keys()
road_pickup_timeinterval_num_6137_y = road_pickup_timeinterval_num[6137].values()
road_pickup_timeinterval_num_17328_x = road_pickup_timeinterval_num[17328].keys()
road_pickup_timeinterval_num_17328_y = road_pickup_timeinterval_num[17328].values()
road_pickup_timeinterval_num_25493_x = road_pickup_timeinterval_num[25493].keys()
road_pickup_timeinterval_num_25493_y = road_pickup_timeinterval_num[25493].values()
road_pickup_timeinterval_num_33310_x = road_pickup_timeinterval_num[33310].keys()
road_pickup_timeinterval_num_33310_y = road_pickup_timeinterval_num[33310].values()
road_pickup_timeinterval_num_961_x = road_pickup_timeinterval_num[961].keys()
road_pickup_timeinterval_num_961_y = road_pickup_timeinterval_num[961].values()
road_pickup_timeinterval_num_16017_x = road_pickup_timeinterval_num[16017].keys()
road_pickup_timeinterval_num_16017_y = road_pickup_timeinterval_num[16017].values()
plt.plot(road_pickup_timeinterval_num_35663_x,road_pickup_timeinterval_num_35663_y,'b-')
plt.plot(road_pickup_timeinterval_num_6137_x,road_pickup_timeinterval_num_6137_y,'g-')
plt.plot(road_pickup_timeinterval_num_17328_x,road_pickup_timeinterval_num_17328_y,'r-')
#plt.plot(road_pickup_timeinterval_num_25493_x,road_pickup_timeinterval_num_25493_y,'y-')
#plt.plot(road_pickup_timeinterval_num_33310_x,road_pickup_timeinterval_num_33310_y,'c-')
plt.plot(road_pickup_timeinterval_num_961_x,road_pickup_timeinterval_num_961_y,'y-')
plt.plot(road_pickup_timeinterval_num_16017_x,road_pickup_timeinterval_num_16017_y,'c-')

max_x = len(road_pickup_timeinterval_num[35663])
max_y = max(road_pickup_timeinterval_num[35663].values())
plt.axis([1,max_x,0,max_y])
plt.show()
