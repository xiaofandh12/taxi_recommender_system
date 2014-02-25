import sys
import math
import re
import psycopg2 
import psycopg2.extras 
import networkx 
import rtree
#from ccdef import *

try:
    INF = float('inf')
except:
    INF = 1e7

ways_dbname = 'beijing_mm_po'
ways_dbuser = 'postgres'
ways_dbpassword = 'zq600991'

gw = None

def new_gw():
    	global gw
    	if gw is not None:
        	return gw
    
   	print 'loading...',
    	gw = GraphWrapper()
    	print 'end'

    	print 'creating graph...',
    	result = gw.create_graph()
    	print 'end'

    	return gw

class GraphWrapper:
	def __init__(self):
		self.G = None
		self.__ways_num = None
		self.__oneway_ways_num = None
		self.conn = None
		self.cursor = None
		self.rtree = None
		self.st = None
	def create_graph(self):
		self.G = networkx.DiGraph()
		self.st = {}
		
		self.__ways_num = 0
		self.__oneway_ways_num = 0

		if not self.open_db():
			return False
		sql = '''select id,
                	 osm_id, osm_source_id, osm_target_id,
                	 clazz, flags,
                	 source, target,
                	 km, kmh,
                	 reverse_cost,
                	 x1, y1, x2, y2,
                	 st_astext(geom_way) as geom from ways'''
       		self.cursor.execute(sql)
        
       		while True:
			row = self.cursor.fetchone()
			if row == None:
                		break
		
			way_id = int(row['id'])
			s = int(row['source'])
			t = int(row['target'])
			length = float(row['km'])
			speed = float(row['kmh'])
			is_oneway = int(row['reverse_cost']) > 100000
			s_lonlat = (float(row['x1']),float(row['y1']))
			t_lonlat = (float(row['x2']),float(row['y2']))
			lonlats = geom2lonlats(row['geom'])

			self.__ways_num = self.__ways_num + 1
    
			self.G.add_edge(
						s,
                		t,
                		way_id = way_id,
                		weight = 1,
               			time = length / speed,
                		length = length,
                		speed = speed,
                		s_lonlat = s_lonlat,
                		t_lonlat = t_lonlat,
                		lonlats = lonlats)

                	if not is_oneway:
                		self.G.add_edge(
                    			t,
                    			s,
                    			way_id = way_id,
                    			weight = 1,
                    			time = length / speed,
                    			length = length,
                    			speed = speed,
                    			s_lonlat = t_lonlat,
                    			t_lonlat = s_lonlat,
                    			lonlats = lonlats[::-1])
			else:
                		self.__oneway_ways_num = self.__oneway_ways_num + 1

            		self.G.add_node(s, pos = s_lonlat)
            		self.G.add_node(t, pos = t_lonlat)
        
            		self.st[way_id] = (s, t)

        	self.close_db()
        	self.nodes_pos = networkx.get_node_attributes(self.G, 'pos')
        	return True

	def proj_p2edge(self, p_lonlat, edge):
        	s = edge[0]
       		t = edge[1]
        	lonlats = self.G[s][t]['lonlats']
        	d_min = INF
        	for i in range(0, len(lonlats)-1):
            		s_lonlat = lonlats[i]
            		t_lonlat = lonlats[i+1]
            		d = d_p2seg(p_lonlat, s_lonlat, t_lonlat)
            		if d < d_min:
                		d_min = d
                		i_d_min = i

        	s_lonlat = lonlats[i_d_min]
        	t_lonlat = lonlats[i_d_min + 1]

        	tt = proj_p2seg(p_lonlat, s_lonlat, t_lonlat)

        	if tt <= 0:
            		l_s = 0
        	elif tt >= 1:
            		l_s = lonlats2km(s_lonlat, t_lonlat)
        	else:
            		l_s = lonlats2km(s_lonlat, t_lonlat) * tt
    
        	for i in range(0, i_d_min):
            		l_s = l_s + lonlats2km(lonlats[i], lonlats[i+1])
        
        	l_t = self.G[s][t]['length'] - l_s

        	proj_lonlat = ((1-tt) * s_lonlat[0] + tt * t_lonlat[0], (1-tt) * s_lonlat[1] + tt * t_lonlat[1])
        	return {'d_proj':d_min, 'l_s':l_s, 'l_t':l_t, 'proj_lonlat':proj_lonlat, 's':s, 't':t}
                             
	def open_db(self):
		self.conn = None
		self.cursor = None
		try:
			self.conn = psycopg2.connect(database = ways_dbname, user = ways_dbuser, password = ways_dbpassword)
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

def d_p2seg(p_lonlat, s_lonlat, t_lonlat):
	p_xy = lonlat2xykm(p_lonlat)
    	s_xy = lonlat2xykm(s_lonlat)
    	t_xy = lonlat2xykm(t_lonlat)
    	ps = d_p2p(p_xy, s_xy)
    	pt = d_p2p(p_xy, t_xy)
    	st = d_p2p(s_xy, t_xy)
    	if ps < 0.000001 or pt < 0.000001:
        	return 0.0
    	if st < 0.000001:
        	return (ps + pt) / 2
    	if ps**2 >= pt**2 + st**2:
        	return pt
    	if pt**2 >= ps**2 + st**2:
        	return ps
    	l = (ps + pt + st) / 2
    	try:
        	a = math.sqrt(l * (l - ps) * (l - pt) * (l - st))
    	except:
        	return 0
    	return 2 * a / st

def lonlat2xykm(lonlat):
    	return (110.0 * abs(math.cos(math.radians(lonlat[1]))) * lonlat[0], 111.0 * lonlat[1])

def d_p2p(s_xy, t_xy):
    	return math.sqrt((s_xy[0] - t_xy[0])**2 + (s_xy[1] - t_xy[1])**2)

def proj_p2seg(p_lonlat, s_lonlat, t_lonlat):
    	p_xy = lonlat2xykm(p_lonlat)
    	s_xy = lonlat2xykm(s_lonlat)
    	t_xy = lonlat2xykm(t_lonlat)
    	st_xy = (t_xy[0] - s_xy[0], t_xy[1] - s_xy[1])
    	t = ((p_xy[0]-s_xy[0])*st_xy[0] + (p_xy[1]-s_xy[1])*st_xy[1])/(st_xy[0]**2+st_xy[1]**2)
    	return t

def lonlats2km(s_lonlat, t_lonlat):
    	dlat = 111.0 * abs(s_lonlat[1] - t_lonlat[1])
    	dlon = 111.0 * abs(math.cos(math.radians((s_lonlat[1] + t_lonlat[1])/2)))*abs(s_lonlat[0]-t_lonlat[0])
    	return math.sqrt(dlat**2 + dlon**2)

def geom2lonlats(geom):
	try:
		str_lonlats = re.search('^LINESTRING\((.*)\)$', geom).group(1).split(',')
		lonlats = []
		for s in str_lonlats:
			if s == '':
				continue
			lon = float(s.split(' ')[0])
			lat = float(s.split(' ')[1])
			lonlats.append((lon, lat))
		return tuple(lonlats)
	except Exception, e:
		print e
		return None
