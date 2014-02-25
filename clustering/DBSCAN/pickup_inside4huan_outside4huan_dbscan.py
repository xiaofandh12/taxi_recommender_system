import dbscan

#pickups format:[[pickup's track_id, pickup's longitude, pickup's latitude, pickup's time], ... , [...]]
def load_data(fileName):
	pickups = []
	f = open(fileName)
	for line in f.readlines():
		curLine = line.strip().split(',')
		pickup = [curLine[0]]
		pickup_lonlat_string = [curLine[3],curLine[4]]
		pickup_lonlat = map(float, pickup_lonlat_string)
		pickup.append(pickup_lonlat[0])

		pickup.append(pickup_lonlat[1])
		pickup.append(curLine[5])
		pickups.append(pickup)
	return pickups

#use dbscan to cluster the pickups both inside3huan and outside4huan,but with different parameters
def pickup_inside4huan_outside4huan_dbscan(pickup_file,e_inside4huan,minpts_inside4huan,e_outside4huan,minpts_outside4huan):
	pickups_list = dbscan.load_data(pickup_file)

	#dbscan the pickups which is inside4huan
	pickups_list_inside4huan_trackid = []
	pickups_list_inside4huan = []
	for i in range(len(pickups_list)):
	        if 116.2670<pickups_list[i][1]<116.4865 and 39.8275<pickups_list[i][2]<39.9910:
        	        pickups_list_inside4huan.append([pickups_list[i][1],pickups_list[i][2]])
                	pickups_list_inside4huan_trackid.append(pickups_list[i])
	pickups_cluster_assignment_list_inside4huan = dbscan.dbscan_algorithm(pickups_list_inside4huan,e_inside4huan,minpts_inside4huan)

	#dbscan the pickups which is outside4huan
	pickups_list_outside4huan_trackid = []
	pickups_list_outside4huan = []
	for i in range(len(pickups_list)):
        	if (116.2670>pickups_list[i][1] or pickups_list[i][1]>116.4865) and (39.8275>pickups_list[i][2] or pickups_list[i][2]>39.9910):
        	        pickups_list_outside4huan.append([pickups_list[i][1],pickups_list[i][2]])
        	        pickups_list_outside4huan_trackid.append(pickups_list[i])
	pickups_cluster_assignment_list_outside4huan = dbscan.dbscan_algorithm(pickups_list_outside4huan,e_outside4huan,minpts_outside4huan)

	#put the cluster(the cluster at least have cluster_member_threshold pickup points) into the result file
	result_dir1 = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/'
	result_dir2 = '/home/donghao/ITS_project/taxi-web/data/pickup/dbscan/'
	pickup_time = pickup_filename.split('.')[0].split('_')[1] + '_' + pickup_filename.split('.')[0].split('_')[2] + '_' + pickup_filename.split('.')[0].split('_')[3]
	result_filename = 'dbscan' + '_' + pickup_time + '_' + str(e_inside4huan) + '_' + str(minpts_outside4huan) + '_' + str(e_outside4huan) + '_' + str(minpts_outside4huan) + '.txt'
	result_file1 = result_dir1 + result_filename
	result_file2 = result_dir2 + result_filename
	result_f1 = open(result_file1,'w')
	result_f2 = open(result_file2,'w')

	cluster_member_threshold = 10
	cluster_count = 1
	for j in range(len(set(pickups_cluster_assignment_list_inside4huan))):
	        cluster_member = []
	        for i in range(len(pickups_list_inside4huan)):
	                if pickups_cluster_assignment_list_inside4huan[i] == j:
	                        cluster_member.append(pickups_list_inside4huan_trackid[i])
	        if len(cluster_member)>cluster_member_threshold:
	                for k in range(len(cluster_member)):
	                        result_f1.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + ',' + cluster_member[k][3] + '\n')
	                        result_f2.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + ',' + cluster_member[k][3] + '\n')
	                cluster_count = cluster_count + 1
	for j in range(len(set(pickups_cluster_assignment_list_outside4huan))):
	        cluster_member = []
	        for i in range(len(pickups_list_outside4huan)):
	                if pickups_cluster_assignment_list_outside4huan[i] == j:
	                        cluster_member.append(pickups_list_outside4huan_trackid[i])
	        if len(cluster_member)>cluster_member_threshold:
	                for k in range(len(cluster_member)):
	                        result_f1.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + ',' + cluster_member[k][3] + '\n')
	                        result_f2.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + ',' + cluster_member[k][3] + '\n')
	                cluster_count = cluster_count + 1
	print 'the dbscan clustering result of inside4huan and outside4huan(each cluster at least have ' + str(cluster_member_threshold) + ' pickups) without noise saved in: \n',result_file1 + '\n' + result_file2



 
pickup_filename = 'pickup_20121101_8-0_8-30.txt'
pickup_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup_according_time/'

pickup_file = pickup_dir + pickup_filename
e_inside4huan = 0.3
minpts_inside4huan = 4
e_outside4huan = 2
minpts_outside4huan = 4

pickup_inside4huan_outside4huan_dbscan(pickup_file,e_inside4huan,minpts_inside4huan,e_outside4huan,minpts_outside4huan)