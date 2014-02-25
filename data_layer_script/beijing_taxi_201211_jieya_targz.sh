#把/home/donghao/ITS_project/taxi_finder/data中的*.tar.gz数据解压缩出来
cd /home/donghao/ITS_project/taxi_finder/data/data_original/20121102/
for file in `ls $pwd`
do 
tar -xzvf $file
done
