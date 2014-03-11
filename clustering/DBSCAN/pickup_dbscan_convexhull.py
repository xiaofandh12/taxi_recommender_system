#from pyhull.convex_hull import ConvexHull
#pts = [[-0.5, -0.5], [-0.5, 0.5], [0.5, -0.5], [0.5, 0.5], [0,0]]
#hull = ConvexHull(pts)
#for s in hull.simplices:
#	print s.coords
from pyhull.convex_hull import ConvexHull
import json

def hull_to_line_coords(hull):
	#get the lines from hull and put it in the lines_coords
	lines_coords = []
	for s in hull.simplices:
	        lines_coord = []
	        lines_coord.extend(map(list,[s.coords[0],s.coords[1]]))
	        lines_coords.append(lines_coord)

	#from lines_coords get the convex hull's coord(clockwise) and put it in the line_coords
	line_coords = []
	line_coords.append(lines_coords[0][0])
	line_coords_num = len(lines_coords)
	while line_coords_num > 0:
	        for lines_coord in lines_coords:
	                if lines_coord[0][0] == line_coords[-1][0] and lines_coord[0][1] == line_coords[-1][1]:
	                        line_coords.append(lines_coord[1])
	                        line_coords_num = line_coords_num - 1
	                        break
	return line_coords
#	print line_coords

pickup_clusters_file = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/pickup_clusters/dbscan_20121101_8-0_8-30_0.3_4_2_4.txt'
pickup_clusters_f = open(pickup_clusters_file)
pickup_clusters_convexhull_file = '/home/donghao/ITS_project/taxi_finder/data/data_pickup/dbscan/pickup_clusters/pickup_clusters_convexhull.json'
pickup_clusters_convexhull_f = open(pickup_clusters_convexhull_file,'w')

pickup_cluster_convexhulls = {}
pickup_cluster_convexhulls['type'] = 'FeatureCollection'
pickup_cluster_convexhulls['features'] = []

pts = {}
max_cluster = 1
for line in pickup_clusters_f.readlines():
	curline = line.strip().split(',')
	pts.setdefault(int(curline[0]),[ ]).append(map(float,[curline[2],curline[3]]))
	if int(curline[0]) > max_cluster:
		max_cluster = int(curline[0])

for i in range(1,max_cluster+1):
	pickup_cluster_convexhull = {}
	pickup_cluster_convexhull['type'] = 'LineString'
	pickup_cluster_convexhull['coordinates'] = []
	hull = ConvexHull(pts[i])
	pickup_cluster_convexhull['coordinates'].extend(hull_to_line_coords(hull))
	pickup_cluster_convexhulls['features'].append({'geometry':pickup_cluster_convexhull})

pickup_clusters_convexhull_f.write(json.dumps(pickup_cluster_convexhulls))
