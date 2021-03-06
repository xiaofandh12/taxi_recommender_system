import kMeans
from numpy import *

pickup_file_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/kMeans/'
pickup_filename = 'pickup_8-0_8-30.txt'
datMat = mat(kMeans.loadDataSetFile(pickup_file_dir + pickup_filename))
print 'begin k-means clustering'
Centroids, clustAssing = kMeans.kMeans(datMat,20)
print 'finish k-means clustering'

datMat_list = datMat.tolist()
Centroids_list = Centroids.tolist()
clustAssing_list = clustAssing.tolist()

filename_suffix = pickup_filename.split('_')[1] + '_' + pickup_filename.split('_')[2].split('.')[0]
centroid_f = open(pickup_file_dir + 'centroids_' + filename_suffix + '.txt','w')
for centroid in Centroids_list:
	centroid_f.write(str(centroid[0]) + ',' + str(centroid[1]) + '\n')

cluster_f = open(pickup_file_dir + 'pickup_cluster_' + filename_suffix + '.txt','w')
centroids_number = len(Centroids_list)
centroid_number = 0
while centroid_number < centroids_number:
	print 'centroid_number:',centroid_number
	for i in range(len(clustAssing_list)):
		if int(clustAssing_list[i][0]) == centroid_number:
			cluster_f.write(str(centroid_number) + ',' + str(datMat_list[i][0]) + ',' + str(datMat_list[i][1]) + '\n')
	centroid_number = centroid_number + 1
