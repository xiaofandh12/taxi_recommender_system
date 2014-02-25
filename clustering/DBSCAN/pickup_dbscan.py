import numpy as np
import math

pickup_filename = 'pickup_20121101_8-0_8-30.txt'
pickup_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup_according_time/'
pickup_file = pickup_dir + pickup_filename

def loadData(fileName):
	pickups_lonlat_list = []
	f = open(fileName)
	for line in f.readlines():
		curLine = line.strip().split(',')
		pickup_lonlat_string = [curLine[3],curLine[4]]
		pickup_lonlat = map(float, pickup_lonlat_string)
		pickups_lonlat_list.append(pickup_lonlat)
	return pickups_lonlat_list

def distEclud_lonlats(A_lonlats, B_lonlats):
	dlat = 111.0 * abs(A_lonlats[1] - B_lonlats[1])
	dlon = 111.0 * abs(math.cos(math.radians((A_lonlats[1] + B_lonlats[1])/2)))*abs(A_lonlats[0]-B_lonlats[0])
	return math.sqrt(dlat**2 + dlon**2)

#calculate whether the e-neighborhood of pickup has at minpts pickups or not
def pickup_neighborhood_number(dataset, pickup, e, minpts):
	neighborhood_number = 0
	pickup_neighborhood_list = []
	pickups_index = []
	for i in range(len(dataset)):
		if distEclud_lonlats(dataset[i], pickup) <= e:
			neighborhood_number = neighborhood_number + 1
			pickup_neighborhood_list.append(dataset[i])
			pickups_index.append(i) 
	return neighborhood_number >= minpts,pickup_neighborhood_list,pickups_index

#DBSCAN begin
unvisited = 0
visited = 1
noise = -1
pickups_lonlat_list = loadData(pickup_file) #the date set for dbscan
pickups_cluster_assignment_list = [-2 for i in range(len(pickups_lonlat_list))] #-2:not assignment, -1:noise, 0 for the first cluster and so on
pickups_visited_unvisited = [unvisited for i in range(len(pickups_lonlat_list))]#0:unvisited, 1:visited
pickups_cluster_list = []
e = 1 #the radius patameter, km
minpts = 4 #the neighborhood density threshold

cluster_number = 0
#until no object is unvisited
while pickups_visited_unvisited.count(0) != 0:
	cluster = []
	noise_cluster = []
	#randomly select an unvisited object P
	for i in range(len(pickups_lonlat_list)):
		if pickups_visited_unvisited[i] == unvisited:
			pickups_visited_unvisited[i] = visited
			cur_pickup = i
			break
	
	print "the unvisited pick up point's index",cur_pickup

	has_minpts_neighborhood,pickup_neighborhood_list,pickups_index = pickup_neighborhood_number(pickups_lonlat_list, pickups_lonlat_list[cur_pickup], e, minpts)

	#if the e-neighborhood of P has at leasr minpts objects
	if has_minpts_neighborhood:
		#create a new cluster C, and add P to C
		cluster.append(pickups_lonlat_list[cur_pickup])
		pickups_cluster_assignment_list[cur_pickup] = cluster_number
		pickups_visited_unvisited[cur_pickup] = visited
		#let N be the set of objects in the e-neighborhood of P
		#for each point P' in N
		pickup_neighborhood_list_length = len(pickup_neighborhood_list)
		while pickup_neighborhood_list_length:
			#if P' is unvisited
			if pickups_visited_unvisited[pickups_index[0]] == unvisited:
				#mark P' as visited
				pickups_visited_unvisited[pickups_index[0]] = visited
				has_minpts_neighborhood1,pickup_neighborhood_list1,pickups_index1 = pickup_neighborhood_number(pickups_lonlat_list, pickup_neighborhood_list[0], e, minpts)
				#if the e-neighborhood of P' has at least minpts points, add those points to N
				if has_minpts_neighborhood1:
					pickup_neighborhood_list.extend(pickup_neighborhood_list1)
					pickups_index.extend(pickups_index1)
					pickup_neighborhood_list_length = pickup_neighborhood_list_length + len(pickup_neighborhood_list1)
			#if P' is not yet a member of any cluster, add P' to C
			if pickups_cluster_assignment_list[pickups_index[0]] == -2:
				cluster.append(pickups_lonlat_list[pickups_index[0]])
				pickups_cluster_assignment_list[pickups_index[0]] = cluster_number
			pickups_index.remove(pickups_index[0])
			pickup_neighborhood_list.remove(pickup_neighborhood_list[0])
			pickup_neighborhood_list_length = pickup_neighborhood_list_length - 1
		cluster_number = cluster_number + 1
	#else mark P as noise
	else:
		noise_cluster.append(pickups_lonlat_list[cur_pickup])
		pickups_cluster_assignment_list[cur_pickup] = noise
#DBSCAN end

#put the result into file
pickup_time = pickup_filename.split('.')[0].split('_')[1] + '_' + pickup_filename.split('.')[0].split('_')[2] + '_' + pickup_filename.split('.')[0].split('_')[3]
result_filename = 'dbscan' + '_' + pickup_time + '_' + str(e) + '_' + str(minpts) + '.txt'
result_filename_noise = 'dbscan' + '_' + pickup_time + '_' + str(e) + '_' + str(minpts) + '_noise' + '.txt'
result_dir1 = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/'
result_dir2 = '/home/donghao/ITS_project/taxi-web/data/pickup/dbscan/'
result_file1 = result_dir1 + result_filename
result_file1_noise = result_dir1 + result_filename_noise
result_file2 = result_dir2 + result_filename
result_file2_noise = result_dir2 + result_filename_noise

result_f1 = open(result_file1,'w')
result_f1_noise = open(result_file1_noise,'w')
result_f2 = open(result_file2,'w')
result_f2_noise = open(result_file2_noise,'w')
for j in range(len(set(pickups_cluster_assignment_list))):
	for i in range(len(pickups_lonlat_list)):		
		if pickups_cluster_assignment_list[i] == j:
			result_f1.write(str(j) + ',' + str(pickups_lonlat_list[i][0]) + ',' + str(pickups_lonlat_list[i][1]) + '\n')
			result_f1_noise.write(str(j) + ',' + str(pickups_lonlat_list[i][0]) + ',' + str(pickups_lonlat_list[i][1]) + '\n')
			result_f2.write(str(j) + ',' + str(pickups_lonlat_list[i][0]) + ',' + str(pickups_lonlat_list[i][1]) + '\n')
			result_f2_noise.write(str(j) + ',' + str(pickups_lonlat_list[i][0]) + ',' + str(pickups_lonlat_list[i][1]) + '\n')

for i in range(len(pickups_lonlat_list)):
	if pickups_cluster_assignment_list[i] == noise:
		result_f1_noise.write(str(noise) + ',' + str(pickups_lonlat_list[i][0]) + ',' + str(pickups_lonlat_list[i][1]) + '\n')
		result_f2_noise.write(str(noise) + ',' + str(pickups_lonlat_list[i][0]) + ',' + str(pickups_lonlat_list[i][1]) + '\n')
print 'the dbscan clustering result without noise saved in: \n',result_file1 + '\n' + result_file2
print 'the dbscan clustering result with noise saved in: \n',result_file1_noise + '\n' + result_file2_noise
