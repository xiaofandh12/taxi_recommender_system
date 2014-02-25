import MySQLdb
import getpass
import os
import datetime
import time

fromdate = (2012,11,1)
todate = (2012,11,4)

def dates_to_tbnames(fromdate, todate):
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

print "mysql connected."

for tbname in tbnames:
	try:
		#sql=r"drop index iCUID on " +tbname  
		sql = r"ALTER TABLE " + tbname + " ADD INDEX iCUID (CUID)"

		print 'querying',tbname,'...',time.strftime('%Y-%m-%d %H:%M:%S')
		cursor.execute(sql)
		print 'Add index in ',tbname,' completed',time.strftime('%Y-%m-%d %H:%M:%S')
	except Exception as e:
		print e
		pass
cursor.close()
conn.close()
