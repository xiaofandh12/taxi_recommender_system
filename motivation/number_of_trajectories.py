import psycopg2
import lib

fromdate = (2012,11,1)
todate = (2012,11,4)
tbnames = lib.dates_to_tbnames(fromdate,todate)

output_dir='/home/donghao/ITS_project/taxi_finder/recommender_system/motivation/number_of_trajectories/'

conn = psycopg2.connect(database = 'beijing_taxi_201211',user = 'postgres',password = 'zq600991')
cursor = conn.cursor()
for tbname in tbnames:
	datename = tbname.split('_')[1]
	output_file=open(output_dir + datename + '_number_of_trajectories.txt','w')
	cuid_counts_sql = 'select max(cuid_count) from ' + ' taxi_tracks_occupied_crusing_' + datename
	cursor.execute(cuid_counts_sql)
	cuid_counts = cursor.fetchone()[0]
	print cuid_counts
	for cuid_count in range(1,cuid_counts+1):
	#for cuid_count in range(1,10):
		sql = 'select count(*) from ' + 'taxi_tracks_occupied_crusing_' + datename + ' where cuid_count=' + str(cuid_count) + ' and oorc = 1'
		cursor.execute(sql)
		number_of_trajectories = cursor.fetchone()[0]
		print datename,cuid_count,number_of_trajectories
		if cuid_count < cuid_counts:
			output_file.write(str(number_of_trajectories) + ',')
		else:
			output_file.write(str(number_of_trajectories))
	output_file.close()
