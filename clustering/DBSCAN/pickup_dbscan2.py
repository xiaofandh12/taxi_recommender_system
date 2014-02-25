import numpy as np
import math
import random

pickup_filename = 'pickup_20121101_8-0_8-30.txt'
pickup_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/pickup_according_time/'
pickup_file = pickup_dir + pickup_filename

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
		pickups.append(pickup)
	return pickups

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

#define the descan algorithm
def dbscan_algorithm(pickups_list_for_dbscan,e,minpts):
	unvisited = 0
	visited = 1
	noise = -1
	pickups_cluster_assignment_list = [-2 for i in range(len(pickups_list_for_dbscan))] #-2:not assignment, -1:noise, 0 for the first cluster and so on
	pickups_visited_unvisited = [unvisited for i in range(len(pickups_list_for_dbscan))]#0:unvisited, 1:visited
	pickups_unvisited_index = [i for i in range(len(pickups_list_for_dbscan))]

	cluster_number = 0
	#until no object is unvisited
	while pickups_visited_unvisited.count(0) != 0:
		cluster = []
		noise_cluster = []
	
		#randomly select an unvisited object P
		if len(pickups_unvisited_index) != 0:
			random_unvisited_pickup_index = pickups_unvisited_index[random.randint(0,len(pickups_unvisited_index)-1)]
			pickups_visited_unvisited[random_unvisited_pickup_index] = visited
			pickups_unvisited_index.remove(random_unvisited_pickup_index)
			cur_pickup = random_unvisited_pickup_index
	
	
		print "the unvisited pick up point's index",cur_pickup

		has_minpts_neighborhood,pickup_neighborhood_list,pickups_index = pickup_neighborhood_number(pickups_list_for_dbscan, pickups_list_for_dbscan[cur_pickup], e, minpts)
		#if the e-neighborhood of P has at least minpts objects
		if has_minpts_neighborhood:
			#create a new cluster C, and add P to C
			cluster.append(pickups_list_for_dbscan[cur_pickup])
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
					pickups_unvisited_index.remove(pickups_index[0])
					has_minpts_neighborhood1,pickup_neighborhood_list1,pickups_index1 = pickup_neighborhood_number(pickups_list_for_dbscan, pickup_neighborhood_list[0], e, minpts)
					#if the e-neighborhood of P' has at least minpts points, add those points to N
					if has_minpts_neighborhood1:
						pickup_neighborhood_list.extend(pickup_neighborhood_list1)
						pickups_index.extend(pickups_index1)
						pickup_neighborhood_list_length = pickup_neighborhood_list_length + len(pickup_neighborhood_list1)
				#if P' is not yet a member of any cluster, add P' to C
				if pickups_cluster_assignment_list[pickups_index[0]] == -2:
					cluster.append(pickups_list_for_dbscan[pickups_index[0]])
					pickups_cluster_assignment_list[pickups_index[0]] = cluster_number
				pickups_index.remove(pickups_index[0])
				pickup_neighborhood_list.remove(pickup_neighborhood_list[0])
				pickup_neighborhood_list_length = pickup_neighborhood_list_length - 1
			cluster_number = cluster_number + 1
		#else mark P as noise
		else:
			noise_cluster.append(pickups_list_for_dbscan[cur_pickup])
			pickups_cluster_assignment_list[cur_pickup] = noise
	return pickups_cluster_assignment_list
	
pickups_list = load_data(pickup_file) #data set for dbscan
#dbscan the data of inside4huan
pickups_list_inside4huan_trackid = []
pickups_list_inside4huan = []
for i in range(len(pickups_list)):
	if 116.2670<pickups_list[i][1]<116.4865 and 39.8275<pickups_list[i][2]<39.9910:
		pickups_list_inside4huan.append([pickups_list[i][1],pickups_list[i][2]])
		pickups_list_inside4huan_trackid.append(pickups_list[i])
e_inside4huan = 0.3 #the first radius parameter, km
minpts_inside4huan = 4 #the neighborhood density threshold
pickups_cluster_assignment_list_inside4huan = dbscan_algorithm(pickups_list_inside4huan,e_inside4huan,minpts_inside4huan)

#put the result of inside4huan into file
result_dir1 = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/'
result_dir2 = '/home/donghao/ITS_project/taxi-web/data/pickup/dbscan/'
noise = -1
pickup_time = pickup_filename.split('.')[0].split('_')[1] + '_' + pickup_filename.split('.')[0].split('_')[2] + '_' + pickup_filename.split('.')[0].split('_')[3]
result_filename_inside4huan = 'dbscan' + '_' + pickup_time + '_' + str(e_inside4huan) + '_' + str(minpts_inside4huan) + '_inside4huan' + '_random.txt'
result_filename_inside4huan_noise = 'dbscan' + '_' + pickup_time + '_' + str(e_inside4huan) + '_' + str(minpts_inside4huan) + '_inside4huan' + '_noise' + '_random.txt'
result_file1_inside4huan = result_dir1 + result_filename_inside4huan
result_file1_inside4huan_noise = result_dir1 + result_filename_inside4huan_noise
result_file2_inside4huan = result_dir2 + result_filename_inside4huan
result_file2_inside4huan_noise = result_dir2 + result_filename_inside4huan_noise

result_f1_inside4huan = open(result_file1_inside4huan,'w')
result_f1_inside4huan_noise = open(result_file1_inside4huan_noise,'w')
result_f2_inside4huan = open(result_file2_inside4huan,'w')
result_f2_inside4huan_noise = open(result_file2_inside4huan_noise,'w')
for j in range(len(set(pickups_cluster_assignment_list_inside4huan))):
	for i in range(len(pickups_list_inside4huan)):		
		if pickups_cluster_assignment_list_inside4huan[i] == j:
			result_f1_inside4huan.write(str(j) + ',' + pickups_list_inside4huan_trackid[i][0] + ',' + str(pickups_list_inside4huan_trackid[i][1]) + ',' + str(pickups_list_inside4huan_trackid[i][2]) + '\n')
			result_f1_inside4huan_noise.write(str(j) + ',' + pickups_list_inside4huan_trackid[i][0] + ',' + str(pickups_list_inside4huan_trackid[i][1]) + ',' + str(pickups_list_inside4huan_trackid[i][2]) + '\n')
			result_f2_inside4huan.write(str(j) + ',' + pickups_list_inside4huan_trackid[i][0] + ',' + str(pickups_list_inside4huan_trackid[i][1]) + ',' + str(pickups_list_inside4huan_trackid[i][2]) + '\n')
			result_f2_inside4huan_noise.write(str(j) + ',' + pickups_list_inside4huan_trackid[i][0] + ',' + str(pickups_list_inside4huan_trackid[i][1]) + ',' + str(pickups_list_inside4huan_trackid[i][2]) + '\n')
for i in range(len(pickups_list_inside4huan)):
	if pickups_cluster_assignment_list_inside4huan[i] == noise:
		result_f1_inside4huan_noise.write(str(noise) + ',' + pickups_list_inside4huan_trackid[i][0] + ',' + str(pickups_list_inside4huan_trackid[i][1]) + ',' + str(pickups_list_inside4huan_trackid[i][2]) + '\n')
		result_f2_inside4huan_noise.write(str(noise) + ',' + pickups_list_inside4huan_trackid[i][0] + ',' + str(pickups_list_inside4huan_trackid[i][1]) + ',' + str(pickups_list_inside4huan_trackid[i][2]) + '\n')
print 'the dbscan clustering result of inside4huan without noise saved in: \n',result_file1_inside4huan + '\n' + result_file2_inside4huan
print 'the dbscan clustering result of inside4huan with noise saved in: \n',result_file1_inside4huan_noise + '\n' + result_file2_inside4huan_noise + '\n'

#dbscan the data of outside4huan
pickups_list_outside4huan_trackid = []
pickups_list_outside4huan = []
for i in range(len(pickups_list)):
        if (116.2670>pickups_list[i][1] or pickups_list[i][1]>116.4865) and (39.8275>pickups_list[i][2] or pickups_list[i][2]>39.9910):
                pickups_list_outside4huan.append([pickups_list[i][1],pickups_list[i][2]])
		pickups_list_outside4huan_trackid.append(pickups_list[i])
e_outside4huan = 2 #the first radius parameter, km
minpts_outside4huan = 4 #the neighborhood density threshold
pickups_cluster_assignment_list_outside4huan = dbscan_algorithm(pickups_list_outside4huan,e_outside4huan,minpts_outside4huan)

#put the result of outside4huan into file
result_filename_outside4huan = 'dbscan' + '_' + pickup_time + '_' + str(e_outside4huan) + '_' + str(minpts_outside4huan) + '_outside4huan' + '_random.txt'
result_filename_outside4huan_noise = 'dbscan' + '_' + pickup_time + '_' + str(e_outside4huan) + '_' + str(minpts_outside4huan) + '_outside4huan' + '_noise' + '_random.txt'
result_file1_outside4huan = result_dir1 + result_filename_outside4huan
result_file1_outside4huan_noise = result_dir1 + result_filename_outside4huan_noise
result_file2_outside4huan = result_dir2 + result_filename_outside4huan
result_file2_outside4huan_noise = result_dir2 + result_filename_outside4huan_noise

result_f1_outside4huan = open(result_file1_outside4huan,'w')
result_f1_outside4huan_noise = open(result_file1_outside4huan_noise,'w')
result_f2_outside4huan = open(result_file2_outside4huan,'w')
result_f2_outside4huan_noise = open(result_file2_outside4huan_noise,'w')
for j in range(len(set(pickups_cluster_assignment_list_outside4huan))):
        for i in range(len(pickups_list_outside4huan)):
                if pickups_cluster_assignment_list_outside4huan[i] == j:
                        result_f1_outside4huan.write(str(j) + ',' + pickups_list_outside4huan_trackid[i][0] + ',' + str(pickups_list_outside4huan_trackid[i][1]) + ',' + str(pickups_list_outside4huan_trackid[i][2]) + '\n')
                        result_f1_outside4huan_noise.write(str(j) + ',' + pickups_list_outside4huan_trackid[i][0] + ',' + str(pickups_list_outside4huan_trackid[i][1]) + ',' + str(pickups_list_outside4huan_trackid[i][2]) + '\n')
                        result_f2_outside4huan.write(str(j) + ',' + pickups_list_outside4huan_trackid[i][0] + ',' + str(pickups_list_outside4huan_trackid[i][1]) + ',' + str(pickups_list_outside4huan_trackid[i][2]) + '\n')
                        result_f2_outside4huan_noise.write(str(j) + ',' + pickups_list_outside4huan_trackid[i][0] + ',' + str(pickups_list_outside4huan_trackid[i][1]) + ',' + str(pickups_list_outside4huan_trackid[i][2]) + '\n')
for i in range(len(pickups_list_outside4huan)):
        if pickups_cluster_assignment_list_outside4huan[i] == noise:
                result_f1_outside4huan_noise.write(str(noise) + ',' + pickups_list_outside4huan_trackid[i][0] + ',' + str(pickups_list_outside4huan_trackid[i][1]) + ',' + str(pickups_list_outside4huan_trackid[i][2]) + '\n')
                result_f2_outside4huan_noise.write(str(noise) + ',' + pickups_list_outside4huan_trackid[i][0] + ',' + str(pickups_list_outside4huan_trackid[i][1]) + ',' + str(pickups_list_outside4huan_trackid[i][2]) + '\n')
print 'the dbscan clustering result of outside4huan without noise saved in: \n',result_file1_outside4huan + '\n' + result_file2_outside4huan
print 'the dbscan clustering result of outside4huan with noise saved in: \n',result_file1_outside4huan_noise + '\n' + result_file2_outside4huan_noise + '\n'

#put the dbscan result of inside4huan and outside4huan into one file
#cluster must have at least cluster_member_threshold pickups
result_filename = 'dbscan' + '_' + pickup_time + '_' + str(e_inside4huan) + '_' + str(minpts_outside4huan) + '_' + str(e_outside4huan) + '_' + str(minpts_outside4huan) + '_random.txt'
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
			cluster_member.append([pickups_list_inside4huan_trackid[i][0],pickups_list_inside4huan_trackid[i][1],pickups_list_inside4huan_trackid[i][2]])
	if len(cluster_member)>cluster_member_threshold:
		for k in range(len(cluster_member)):
			result_f1.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + '\n')
			result_f2.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + '\n')
		cluster_count = cluster_count + 1
for j in range(len(set(pickups_cluster_assignment_list_outside4huan))):
	cluster_member = []
	for i in range(len(pickups_list_outside4huan)):
		if pickups_cluster_assignment_list_outside4huan[i] == j:
			cluster_member.append([pickups_list_inside4huan_trackid[i][0],pickups_list_outside4huan_trackid[i][1],pickups_list_outside4huan_trackid[i][2]])
	if len(cluster_member)>cluster_member_threshold:
		for k in range(len(cluster_member)):
			result_f1.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + '\n')
			result_f2.write(str(cluster_count) + ',' + str(cluster_member[k][0]) + ',' + str(cluster_member[k][1]) + ',' + str(cluster_member[k][2]) + '\n')
		cluster_count = cluster_count + 1
print 'the dbscan clustering result of inside4huan and outside4huan(each cluster at least have ' + str(cluster_member_threshold) + ' pickups) without noise saved in: \n',result_file1 + '\n' + result_file2

