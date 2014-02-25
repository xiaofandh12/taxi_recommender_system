import MySQLdb
import os 
import datetime
import time

fromdate = (2012,11,1)
todate = (2012,11,4)
output_dir = "/home/donghao/ITS_project/taxi_finder/data/data_by_cuid_count/tb_20121101"
CUID_count = 1
CUID = 1140
f = open(output_dir + "/" + str(CUID_count) + ".txt","w")
conn = MySQLdb.connect(host="localhost",user="root",passwd="zq600991",db="beijing_taxi_201211",local_infile=1)
cursor = conn.cursor()
sql = r"SELECT * FROM " + "tb_20121101" + r" WHERE CUID = " + str(CUID) + r" ORDER BY time"
cursor.execute(sql)
results = cursor.fetchall()
for items in results:
	line = ''
	item_count = 1
	for item in items:
		if item_count == 1:
			line = line + str(CUID_count) + ','
		elif 1 < item_count <= 8:
			line = line + str(item) + ','
		else:
			line = line + str(item) + os.linesep
		item_count += 1 
	
	f.write(line)
	#		for item in items:
	#			f.write(str(item) + ', ')
	#		f.write(os.linesep)
f.close()
