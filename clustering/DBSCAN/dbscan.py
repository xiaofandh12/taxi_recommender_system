import numpy as np
import math
import random

#calculate the distance between two points
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
