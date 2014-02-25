import json

pickup_dir = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/kMeans/'
pickup_filename = 'pickup_cluster_8-0_8-30.txt'
pickup_f = open(pickup_dir + pickup_filename,'r')
cluster_number = 9

pickup_cluster_0_json_f = open(pickup_dir + pickup_filename.split('.')[0] + '_' + str(cluster_number) + '.json','w')

jdict = {}
jdict['type'] = 'MultiPoint'
coordinates = []

for line in pickup_f.readlines():
	if int(line.split(',')[0]) == cluster_number:
		print line
		coordinate = [float(line.split(',')[1]), float(line.split(',')[2])]
		coordinates.append(coordinate)

jdict['coordinates'] = coordinates
pickup_cluster_0_json_f.write(json.dumps(jdict))
pickup_cluster_0_json_f.close()



