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
	pickup_dbscan_dropoff_file = pickup_dbscan_dir + pickup_dbscan_filename.split('.')[0] + '_dropoff.txt'
	
	pickup_dbscan_f = open(pickup_dbscan_file,'r')
	pickup_dbscan_dropoff_f = open(pickup_dbscan_dropoff_file,'w')
	for line in pickup_dbscan_f.readlines():
		curLine = line.strip().split(',')
		pickup_dbscan_dropoff_f.write(curLine[0] + ',' + curLine[1] + ',' + str(dropoffs[curLine[1]][0]) + ',' + str(dropoffs[curLine[1]][1]) + ',' + dropoffs[curLine[1]][2] + '\n')

pickup_dbscan_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/'	
pickup_dbscan_filename = 'dbscan_20121101_8-0_8-30_0.3_4_2_4.txt'
pickup_dbscan_dropoff(pickup_dbscan_dir,pickup_dbscan_filename)
