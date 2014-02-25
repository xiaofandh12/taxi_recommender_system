from numpy import *
from datetime import datetime

def loadDataSet(fileName,start_time_string,end_time_string):
	#'2012-11-02 12:51:12' --> '%Y-%m-%d %H:%M:%S'
	start_time_datetime = datetime.strptime(start_time_string,'%Y-%m-%d %H:%M:%S')
	end_time_datetime = datetime.strptime(end_time_string,'%Y-%m-%d %H:%M:%S')
	if start_time_datetime.date() != end_time_datetime.date():
		print start_time_string,end_time_string
		print 'start time and end time are not in the same day'
		return False
	dataMat = []
	f = open(fileName)
	for line in f.readlines():
		curLine = line.strip().split(',')
		curPickup_time_datetime = datetime.strptime(curLine[5],'%Y-%m-%d %H:%M:%S')
		#hour
		if curPickup_time_datetime.date() == start_time_datetime.date() and curPickup_time_datetime.hour >= start_time_datetime.hour and curPickup_time_datetime.hour <= end_time_datetime.hour:
		#minute
		#if curPickup_time_datetime.date() == start_time_datetime.date() and curPickup_time_datetime.hour == start_time_datetime.hour and curPickup_time_datetime.hour == end_time_datetime.hour and curPickup_time_datetime.minute >= start_time_datetime.minute and curPickup_time_datetime.minute <= end_time_datetime.minute:
			proj_lonlats_string = [curLine[3],curLine[4]]
			proj_lonlats = map(float, proj_lonlats_string)
			dataMat.append(proj_lonlats)
	return dataMat

def loadDataSetFile(fileName):
	dataMat = []
	f = open(fileName)
	for line in f.readlines():
		curLine = line.strip().split(',')
		proj_lonlats_string = [curLine[3],curLine[4]]
		proj_lonlats = map(float, proj_lonlats_string)
		dataMat.append(proj_lonlats)
	return dataMat

def distEclud_lonlats(A_lonlats, B_lonlats):
	A_lonlat = A_lonlats.tolist()[0]
	B_lonlat = B_lonlats.tolist()[0]
	dlat = 111.0 * abs(A_lonlat[1] - B_lonlat[1])
	dlon = 111.0 * abs(math.cos(math.radians((A_lonlat[1] + B_lonlat[1])/2)))*abs(A_lonlat[0]-B_lonlat[0])
	return math.sqrt(dlat**2 + dlon**2)

def randCent(dataSet, k):
	n = shape(dataSet)[1]
	centroids = mat(zeros((k, n)))
	for j in range(n):
		minJ = min(dataSet[:,j])
		rangeJ = float(max(dataSet[:,j]) - minJ)
		centroids[:, j] = minJ + rangeJ * random.rand(k, 1)
	return centroids

def kMeans(dataSet, k, distMeans=distEclud_lonlats, createCent = randCent):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m, 2)))
	centroids = createCent(dataSet, k)
	clusterChanged = True
	while clusterChanged:
		clusterChanged = False
		for i in range(m):
			minDist = inf; minIndex = -1
			for j in range(k):
				distJI = distMeans(centroids[j,:], dataSet[i,:])
				if distJI < minDist:
					minDist = distJI; minIndex = j
			if clusterAssment[i,0] != minIndex: clusterChanged = True
			clusterAssment[i,:] = minIndex,minDist**2
		print centroids
		for cent in range(k):
			ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
			centroids[cent,:] = mean(ptsInClust, axis=0)
	return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud_lonlats):
	m = shape(dataSet)[0]
	clusterAssment = mat(zeros((m,2)))
	centroid0 = mean(dataSet, axis=0).tolist()[0]
	centList = [centroid0]
	for j in range(m):
		clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
	while (len(centList) < k):
		lowestSSE = inf
		for i in range(len(centList)):
			print i
			ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
			centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
			sseSplit = sum(splitClustAss[:, 1])
			sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A!=i)[0],1])
			print 'sseSplit, and notSplit:',sseSplit,sseNotSplit
			if (sseSplit + sseNotSplit) < lowestSSE:
				bestCentToSplit = i
				bestNewCents = centroidMat
				bestClustAss = splitClustAss.copy()
				lowestSSE = sseSplit + sseNotSplit
		bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
		bestClustAss[nonzero(bestClustAss[:,1].A == 0)[0],0] = bestCentToSplit
		print 'the bestCentToSplit is: ',bestCentToSplit
		print 'the len of bestClustAss is: ', len(bestClustAss)
		centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]
		centList.append(bestNewCents[1,:].tolist()[0])
		clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] = bestClustAss
	return mat(centList), clusterAssment
			
