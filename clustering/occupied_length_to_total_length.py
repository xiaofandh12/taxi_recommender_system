import psycopg2,psycopg2.extras

path_attr_conn = psycopg2.connect(database = 'beijing_taxi_201211',user = 'postgres', password = 'zq600991')
path_attr_cursor = path_attr_conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
path_attr_sql = 'select tid,length from  taxi_paths_occupied_crusing_st_20121101_attr'
path_attr_cursor.execute(path_attr_sql)
print path_attr_cursor.fetchone()

tracks_cursor = path_attr_conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
#tracks_cursor.execute('select count(*) from taxi_tracks_occupied_crusing_20121101')
#print tracks_cursor.fetchone()
occupied_length = 0
crusing_length = 0
occupied_length_1 = 0
crusing_length_1 = 0
occupied_length_9 = 0
crusing_length_9 = 0

for i in range(396415):
	path_row = path_attr_cursor.fetchone()
	tracks_sql = 'select cuid_count,oorc from taxi_tracks_occupied_crusing_20121101 where id=' + str(path_row['tid'])
	tracks_cursor.execute(tracks_sql)
	tracks_row = tracks_cursor.fetchone()

	if tracks_row['oorc'] == 1:
		occupied_length	= occupied_length + float(path_row['length'])
	else:
		crusing_length = crusing_length + float(path_row['length'])
	print path_row['tid'],occupied_length,crusing_length

	if tracks_row['cuid_count'] == 1 and tracks_row['oorc'] == 1:
		occupied_length_1 = occupied_length_1 + float(path_row['length'])
	elif tracks_row['cuid_count'] == 1 and tracks_row['oorc'] == 0:
		crusing_length_1 = crusing_length_1 + float(path_row['length'])

	if tracks_row['cuid_count'] == 9 and tracks_row['oorc'] == 1:
		occupied_length_9 = occupied_length_9 + float(path_row['length'])
	elif tracks_row['cuid_count'] == 9 and tracks_row['oorc'] == 0:
		crusing_length_9 = occupied_length_9 + float(path_row['length'])
occupied_length_crusing_length = occupied_length/(occupied_length+crusing_length)
occupied_length_crusing_length_1 = occupied_length_1/(occupied_length_1+crusing_length_1)
occupied_length_crusing_length_9 = occupied_length_9/(occupied_length_9+crusing_length_9)
print 'occupied length : crusing length',occupied_length_crusing_length
print 'occupied length 1 : crusing length 1',occupied_length_crusing_length_1
print 'occupied length 9: cursing length 9',occupied_length_crusing_length_9
