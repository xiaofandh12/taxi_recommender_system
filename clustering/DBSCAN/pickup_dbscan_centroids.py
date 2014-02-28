pickup_dbscan_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/'
pickup_dbscan_filename = 'dbscan_20121101_8-0_8-30_0.3_4_2_4.txt'
pickup_dbscan_file = pickup_dbscan_dir + pickup_dbscan_filename
pickup_dbscan_f = open(pickup_dbscan_file,'r')

max_cluster = 1
longitudes = {}
latitudes = {}
for line in pickup_dbscan_f.readlines():
	curLine = line.strip().split(',')
	if line != '':
		longitudes.setdefault(int(curLine[0]),[ ]).append(float(curLine[2]))
		latitudes.setdefault(int(curLine[0]),[ ]).append(float(curLine[3]))
		if int(curLine[0]) > max_cluster:
			max_cluster = int(curLine[0])

centroids = {}
for i in range(1,max_cluster+1):
	centroid_longitude = sum(longitudes[i])/len(longitudes[i])
	centroid_latitude = sum(latitudes[i])/len(latitudes[i])
	centroids.setdefault(i,[ ]).append(centroid_longitude)
	centroids.setdefault(i,[ ]).append(centroid_latitude)

pickup_dbscan_centroids_filename = 'centroids_20121101_8-0_8-30_0.3_4_2_4.txt'
pickup_dbscan_centroids_file = pickup_dbscan_dir + pickup_dbscan_centroids_filename
pickup_dbscan_centroids_f = open(pickup_dbscan_centroids_file,'w')
for i in range(1,max_cluster+1):
	print i,centroids[i][0],centroids[i][1]
	pickup_dbscan_centroids_f.write(str(i) + ',' + ' ' + ',' + str(centroids[i][0]) + ',' + str(centroids[i][1]) + ',' + ' ' + '\n') 	
