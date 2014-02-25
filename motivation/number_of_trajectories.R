input_dir = '/home/donghao/ITS_project/taxi_finder/recommender_system/motivation/number_of_trajectories_occupied/20121104_number_of_trajectories.txt'
number_of_trajectories <- read.table(input_dir,header=FALSE,sep=",")
number_of_trajectories_array <- c()
i <- 1
while (i <= length(number_of_trajectories)){
	if((number_of_trajectories[1,i] <= 50) & (number_of_trajectories[1,i]>=2)){
		number_of_trajectories_array <- c(number_of_trajectories_array,number_of_trajectories[1,i]);
	}
	i <- i+1;
}
hist(number_of_trajectories_array,breaks=40,col='blue',xlab='number of occupied trajectories',ylab='number of taxis',main='')
#i <- 1
#while (i <= length(number_of_trajectories)){
#	if(number_of_trajectories[1,i] == 124){
#		index <- i;
#	}
#	i <- i+1;
#}
