import MySQLdb
import os
import time

txt_data_dir = "/home/donghao/ITS_project/taxi_finder/data/data_txt/"

try:
	conn = MySQLdb.connect(host="localhost",user="root",passwd="zq600991",db="beijing_taxi_201211",local_infile=1)
	cursor = conn.cursor()

	ithfile=1
	all_file = os.listdir(txt_data_dir)
	#all_file = ['20121101.txt']
	for file in all_file:
		(file_name,file_ext) = os.path.splitext(file)
		
		print "\n"
		print "processing the ",ithfile," file"
		print "processing file:",file

		txt_file_path = txt_data_dir + file
		table_name = 'tb_' + file_name		
		sql = r"CREATE TABLE IF NOT EXISTS " + table_name + r"""(
			CUID int not null,
			EVENT int not null,
			TAXI_STATUS int not null,
			TIME TIMESTAMP not null,
			LONGITUDE double not null,
			LATITUDE double not null,
			SPEED int not null,
			HEAD int not null,
			GPS_STATUS int not null);"""
		print table_name,"successfuly created."
		cursor.execute(sql)
		conn.commit()
		print txt_file_path
		sql = r"LOAD DATA LOCAL INFILE '" + txt_file_path +r"' INTO TABLE " + table_name + r" FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'"
		print time.strftime('%Y-%m-%d %H:%M:%S')
		cursor.execute(sql)
		print time.strftime('%Y-%m-%d %H:%M:%S')
		conn.commit()
		ithfile=ithfile+1
	cursor.close()
	conn.close()
			
except:
	print "something was wrong" 
