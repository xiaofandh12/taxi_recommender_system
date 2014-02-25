import psycopg2,psycopg2.extras
import graph

beijing_taxi_dbname = 'beijing_taxi_201211'
beijing_taxi_dbuser = 'postgres'
beijing_taxi_dbpassword = 'zq600991'

class DB(object):
	def __init__(self,database=beijing_taxi_dbname):
		self.database = database
		self.user = beijing_taxi_dbuser
		self.password = beijing_taxi_dbpassword
		self.open_db()
	def __del__(self):
		self.close_db()
	
	def open_db(self):
		self.conn = None
		self.cursor = None
		try:
			self.conn = psycopg2.connect(database = self.database, user = self.user, password = self.password)
			self.cursor = self.conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
			return True
		except psycopg2.DatabaseError, e:
			print e
			return False
	def close_db(self):
		if self.conn:
			self.conn.close()
			self.conn = None
			self.cursor = None

class TrackReader(DB):
	def __init__(self, tbname,limit = 10000, offset = 0):
		super(TrackReader, self).__init__()
		self.tbname = tbname
	
		self.limit = limit
		self.offset = offset
		self.queried_num = 0
		self.fetched_num = 0
	
		self.query_more()

	def query_more(self):
		sql = 'select id, cuid_count, st_astext(track_geom) as track_geom, track_desc, oorc from ' + self.tbname + ' order by id limit %s offset %s'
		self.cursor.execute(sql, (str(self.limit), str(self.offset)))
		self.offset = self.offset + self.limit
		self.queried_num = self.queried_num + self.limit
	def fetch_one(self):
		row = self.cursor.fetchone()
		if row == None:
			self.query_more()
			row = self.cursor.fetchone()
		if row == None:
			return None,None,None,None,None

		self.fetched_num = self.fetched_num + 1
		return row['id'],row['cuid_count'],row['track_geom'],row['track_desc'],row['oorc']

	def fetch_track_by_id(self, tid):
		tconn = None
		tmp_cursor = None
		try:
			tconn = psycopg2.connect(database = self.database, user = self.user, password = self.password)
			tmp_cursor = tconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
			sql = 'select id,cuid_count,st_astext(track_geom) as track_geom, track_desc, oorc from ' + self.tbname + ' where id = %s'
			tmp_cursor.execute(sql, (str(tid),))
			row = tmp_cursor.fetchone()
			if row == None:
				return None,None,None,None,None
			else:
				return row['id'],row['cuid_count'],row['track_geom'],row['track_desc'],row['oorc']
		except Exception, e:
			print e
			return None,None,None,None,None

class PathReader(DB):
	def __init__(self, tbname, gw = None, limit = 10, offset = 0):
		super(PathReader, self).__init__()
		
		self.limit = limit
		self.offset = offset
		self.queried_num = 0
		self.fetched_num = 0
	
		self.tbname = tbname
		self.gw = gw

		self.query_more()

	def query_more(self):
		sql = 'select tid,way_ids, st_astext(path_geom) as path_geom from ' + self.tbname + ' order by tid limit %s offset %s'

		self.cursor.execute(sql, (str(self.limit), str(self.offset)))
		self.offset = self.offset + self.limit
		self.queried_num = self.queried_num + self.limit

	def fetch_one(self):
		row = self.cursor.fetchone()
		if row == None:
			self.query_more()
			row = self.cursor.fetchone()
		if row == None:
			return None,None

		self.fetched_num = self.fetched_num + 1
		return row['tid'],row['way_ids']

	def fetch_path_by_tid(self, tid):
		tconn = None
		tmp_cursor = None
		try:
			tconn = psycopg2.connect(database = self.database, user = self.user, password =self.password)
			tmp_cursor = tconn.cursor(cursor_factory = psycopg2.extras.DictCursor)
			sql = 'select tid, way_ids, st_astext(path_geom) as path_geom from ' + self.tbname + ' where tid = %s'
			tmp_cursor.execute(sql, (str(tid),))
			row = tmp_cursor.fetchone()
			if row == None:
				return None,None
			else:
				return row['tid'],row['way_ids']
		except Exception, e:
			print e
			return None,None	
