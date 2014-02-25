import MySQLdb
import os 
import datetime
import time

fromdate = (2012,11,1)
todate = (2012,11,4)
output_dir = "/home/donghao/ITS_project/taxi_finder/data/data_by_cuid_count/"

def dates_to_tbnames(fromdate,todate):
	tbnames = []
	d = datetime.date(fromdate[0],fromdate[1],fromdate[2])
	to_d = datetime.date(todate[0],todate[1],todate[2])
	while True:
		tbnames.append("tb_" + str(d).replace('-',''))
		d += datetime.date.resolution
		if d > to_d:
			return tuple(tbnames)
tbnames = dates_to_tbnames(fromdate,todate)
print tbnames

conn = MySQLdb.connect(host="localhost",user="root",passwd="zq600991",db="beijing_taxi_201211",local_infile=1)
cursor = conn.cursor()

print "mysql connected"

for tbname in tbnames:
	sql = r"SELECT distinct(CUID) FROM " + tbname
	cursor.execute(sql)
	results = cursor.fetchall()

	CUIDs = []
	for CUID in results:
		CUIDs.append(CUID[0])
	print CUIDs
	
	if not os.path.exists(output_dir + tbname):	
		os.mkdir(output_dir + tbname)
	
	CUID_count = 1;
	for CUID in CUIDs:
		print time.strftime('%Y-%m-%d %H:%M:%S')
		if not os.path.exists(output_dir + tbname + "/" ):
			os.mkdir(output_dir + tbname + "/")
		f = open(output_dir + tbname + "/" + str(CUID_count) + ".txt","w")
		sql = r"SELECT * FROM " + tbname + r" WHERE CUID = " + str(CUID) + r" ORDER BY time"
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
		print output_dir + tbname + "/" + str(CUID_count) + ".txt","completed"
		f.close()
		print time.strftime('%Y-%m-%d %H:%M:%S')
		print os.linesep
		CUID_count +=1;
cursor.close()
conn.close()
