#出现bad for loop variable，解决办法：sudo dpkg-reconfigure dash 选no
#把某一天的数据存储到一个txt文件中，如使20121101.txt包含20121101这一天所有的数据
fromdir=20121101
for (( i=1; i<=30; i++ ))
do
	echo $fromdir
	workfile1=$fromdir.txt
	workfile2=$(($fromdir+1)).txt
	date1=$fromdir
	date2=$(($fromdir+1))00[0-1][0-5]

	cd /home/donghao/ITS_project/taxi_finder/data/data_original/$fromdir
	for file in `ls $pwd`#不是单引号，而是tab键上面那个符号
	do
		tar -xzvf $file
	done

	cd /home/donghao/ITS_project/taxi_finder/data/data_txt
	if [ ! -f "$workfile1" ];then
	touch /home/donghao/ITS_project/taxi_finder/data/data_txt/$workfile1
	fi
	if [ ! -f "$workfile2" ];then
	touch /home/donghao/ITS_project/taxi_finder/data/data_txt/$workfile2
	fi

	filelist=`ls /home/donghao/ITS_project/taxi_finder/data/data_original/$fromdir/*.txt`
	for file1 in $filelist
	do 
		grep -i $date1 $file1 >> /home/donghao/ITS_project/taxi_finder/data/data_txt/$workfile1
		grep -i $date2 $file1 >> /home/donghao/ITS_project/taxi_finder/data/data_txt/$workfile2
		#比如打开的20121109这个目录(fromdir=20121109)，这个目录下面的txt文件绝大部分是20121109这天的记录，另一部分有20121110这天头14分钟的记录，极小部分为其它记录（这部分可能属于错误记录）
		echo $file1
	done

	rm /home/donghao/ITS_project/taxi_finder/data/data_original/$fromdir/*.txt
	fromdir=$(($fromdir+1))
done
