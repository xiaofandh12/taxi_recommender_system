import MySQLdb
import getpass
import os
import datetime

fromdate = (2012,11,1)
todate = (2012,11,4)

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
	
	f=open("/home/donghao/ITS_project/taxi_finder/data_cuid/"+tbname+".txt","w")
	
	CUIDs=[]
	for CUID in results:
		CUIDs.append(CUID[0])
		f.write(str(CUID[0]))
		f.write(os.linesep)
		print CUID[0]
	f.close()
	print CUIDs
		
cursor.close()
conn.close()
