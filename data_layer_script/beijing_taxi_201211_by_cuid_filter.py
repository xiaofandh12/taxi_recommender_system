import lib
import os

input_dir = '/home/donghao/ITS_project/taxi_finder/data/data_by_cuid_count/'
output_dir = '/home/donghao/ITS_project/taxi_finder/data/data_by_cuid_count_filter/'
fromdate = (2012,11,1)
todate = (2012,11,4)
#tbnames = lib.dates_to_tbnames(fromdate, todate)
tbnames = ['tb_20121101','tb_20121102','tb_20121103','tb_20121104']
for tbname in tbnames:
	input_file_dir = input_dir + tbname + '/'
	output_file_dir = output_dir +tbname + '/'
	os.mkdir(output_file_dir)
	for file_number in range(1,len(os.listdir(input_file_dir))+1):
	#for file_number in range(1,2):
		input_f = open(input_file_dir + str(file_number) + '.txt','r')
		output_f = open(output_file_dir + str(file_number) + '.txt','w')
		#log_f = open(output_file_dir + str(file_number) + '_log.txt','w')
		first_line = input_f.readline()
		second_line =  input_f.readline()
		if second_line == '':
			continue
		third_line = input_f.readline()
		if third_line == '':
			continue

		first_line_attrs = lib.parse_line(first_line)
		second_line_attrs = lib.parse_line(second_line)
		third_line_attrs = lib.parse_line(third_line)

 		first_line_coord = [first_line_attrs['lon'], first_line_attrs['lat']]
		second_line_coord = [second_line_attrs['lon'],second_line_attrs['lat']]
		third_line_coord = [third_line_attrs['lon'],third_line_attrs['lat']]

		d_first_second = lib.coords_2_km(first_line_coord,second_line_coord)
		d_second_third = lib.coords_2_km(second_line_coord,third_line_coord)
		d_first_third = lib.coords_2_km(first_line_coord,third_line_coord)
		while True:
			#log_f.write(str(d_first_second) + ' ' + str(d_second_third) + ' ' + str(d_first_third) + ' ' + first_line)
			distance_separate = 0.5
			if (first_line_attrs['taxi_status'] == third_line_attrs['taxi_status']) & (first_line_attrs['taxi_status'] != second_line_attrs['taxi_status']) & (d_first_second > distance_separate) & (d_second_third > distance_separate):
			#distance_separate = 1
			#if (d_first_second > distance_separate) & (d_second_third > distance_separate) & (d_first_third < distance_separate):
			#if (d_first_third < d_first_second) & (d_first_third < d_second_third):
				output_f.write(first_line)
			
				first_line = third_line
				first_line_attrs = third_line_attrs
				first_line_coord = third_line_coord

				second_line = input_f.readline()
				if second_line == '':
					output_f.write(first_line)
					break
				second_line_attrs = lib.parse_line(second_line)
				second_line_coord = [second_line_attrs['lon'],second_line_attrs['lat']]

				third_line = input_f.readline()
				if third_line == '':
					break
				third_line_attrs = lib.parse_line(third_line)
				third_line_coord = [third_line_attrs['lon'],third_line_attrs['lat']]

				d_first_second = lib.coords_2_km(first_line_coord,second_line_coord)
				d_second_third = lib.coords_2_km(second_line_coord,third_line_coord)
				d_first_third = lib.coords_2_km(first_line_coord,third_line_coord)
			else:
				output_f.write(first_line)
				
				first_line = second_line
				first_line_attrs = second_line_attrs
				first_line_coord = second_line_coord

				second_line = third_line
				second_line_attrs = third_line_attrs
				second_line_coord = third_line_coord

				third_line = input_f.readline()
				if third_line == '':
					output_f.write(first_line)
					output_f.write(second_line)
					break
				third_line_attrs = lib.parse_line(third_line)
				third_line_coord = [third_line_attrs['lon'],third_line_attrs['lat']]

				d_first_second = lib.coords_2_km(first_line_coord,second_line_coord)
				d_second_third = lib.coords_2_km(second_line_coord,third_line_coord)
				d_first_third = lib.coords_2_km(first_line_coord,third_line_coord)
		print tbname,input_file_dir + str(file_number) + '.txt' + 'completed'
