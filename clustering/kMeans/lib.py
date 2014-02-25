#coding=utf-8
import datetime
import time
import os
import math
from numpy import *
def dates_to_tbnames(fromdate, todate):
	tbnames = []#新建一个空列表
	d = datetime.date(fromdate[0],fromdate[1],fromdate[2])#class datetime.date(year, month, day);fromdate[0]:2009,fromdate[1]:5,fromdate[2]:1;d:2009-05-01
	to_d = datetime.date(todate[0],todate[1],todate[2])
	while True:
		tbnames.append("tb_" + str(d).replace('-',''))#append为一列表方法，append方法用于在列表末尾追加新的对象；str(d)将对象d转换为字符串；replace为一字符串方法，replace方法返回某字符串的所有匹配项均被替换之后得到的字符串。
		d += datetime.date.resolution#date.resolution:The smallest possible difference between non-equal date objects,timedelta(days=1);datetime.date.resolution:datetime.timedelta(1);print datetime.date.resolution:1 day, 0:00:00;当d为2009-05-01时，执行d += datetime.date.resolution后d为2009-05-02。
		if d > to_d:
			return tuple(tbnames)#tuple函数的功能：以一个序列作为参数并把它转化为元组，如果参数就是元组，那么该参数就会被原样返回。列表与元组的主要区别在于：列表可以修改，元组则不能。

def times_to_utcs(fromdate, todate, fromtime, totime):
	utcs = []
	t = datetime.datetime(fromdate[0],fromdate[1],fromdate[2],fromtime[0],fromtime[1],fromtime[2])
	to_t = datetime.datetime(todate[0],todate[1],todate[2],totime[0],totime[1],totime[2])
	d = datetime.date(fromdate[0],fromdate[1],fromdate[2])
	to_d = datetime.date(todate[0],todate[1],todate[2])
	while True:
		utcs.append((time.mktime(t.utctimetuple()), time.mktime(to_t.utctimetuple())))   #mktime always convert local time to utc seconds
		d += datetime.date.resolution
		if d > to_d:
			return tuple(utcs)

def new_output_dir():
	output_dir = raw_input('Query results will be loaded in this new directory: ')
	if os.path.isdir(output_dir):
		print output_dir,"has exist"
		return ""
	os.mkdir(output_dir)	
	os.chdir(output_dir)
	os.mkdir('data')
	os.chdir('data')
	return os.getcwd()

def new_output_dir_as(output_dir):
	if os.path.isdir(output_dir):
		print output_dir,"has exist"
		return ""
	os.mkdir(output_dir)#output_dir存在的情况下，执行了return ""后，下面这三条语句就不会在执行了。
	os.mkdir(output_dir + 'data/')
	return output_dir + 'data/'
	
def cmp_str_by_int(str_x, str_y):
	(x_name, x_ext) = os.path.splitext(str_x)
	(y_name, y_ext) = os.path.splitext(str_y)
	return int(x_name) - int(y_name)
	
def is_record_in_area(line, min_lo, max_lo, min_la, max_la):
	s = line.split(', ')
	lo = int(s[2])
	la = int(s[3])
	return lo >= min_lo and lo <= max_lo and la >= min_la and la <= max_la

def is_coord_in_area(coord, min_lon, max_lon, min_lat, max_lat):
	lon = coord[0]
	lat = coord[1]
	return lon >= min_lon and lon <= max_lon and lat >= min_lat and lat <= max_lat

def parse_line(line):
	s = line.split(',')
	attrs = {}
	attrs['cuid'] = s[0]
	attrs['event'] = s[1]
	attrs['taxi_status'] = s[2]
	attrs['time'] = s[3]
	attrs['lon'] = float(s[4])
	attrs['lat'] = float(s[5])
	attrs['speed'] = int(s[6])
	attrs['head'] = int(s[7])
	attrs['gps_status'] = int(s[8])
	return attrs

"""
def coords_2_km(first_coord, second_coord):
	a = sin(first_coord[1]*pi/180)*sin(second_coord[1]*pi/180)
	b = cos(first_coord[1]*pi/180)*cos(second_coord[1]*pi/180)*cos((first_coord[0]-second_coord[0])*pi/180)
	return arccos(a + b)*6371.0
"""

def coords_2_km(first_coord, second_coord):
	dlat = 110.0 * abs(first_coord[1] - second_coord[1])
	dlon = 110.0 * abs(math.cos(math.radians((first_coord[1] + second_coord[1]) / 2))) * abs(first_coord[0] - second_coord[0])
	return math.sqrt(dlat**2 + dlon**2)

def parse_pickup_line(line):
	s = line.split(',')
	attrs = {}
	attrs['cuid'] = s[0]
	attrs['pickup_lon'] = float(s[1])
	attrs['pickup_lat'] = float(s[2])
	attrs['pickup_proj_lon'] = float(s[3])
	attrs['pickup_proj_lat'] = float(s[4])
	attrs['pickup_time'] = s[5]
	attrs['pickup_road'] = s[6]
	attrs['pickup_road_source'] = s[7]
	attrs['pickup_road_target'] = s[8]
	attrs['pickup_oorc'] = s[9]
	return attrs
