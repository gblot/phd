mydata = read.csv("data/ground_truth_traveltimes_2_NB.csv")		# load source data
mean = mean(mydata$time)
mean_alert1 = mydata$end[ mydata$time >(mean+sd(mydata$time)) ]
hist(mean_alert1,breaks=100,col = "lightblue",freq = FALSE)
den <- density(mean_alert1)
lines(den, col = "red")
#sink("results/ground_truth_traveltimes_1_NB.txt")				# redirect output to a text file
#print(summary(mydata$time))										# write a summary of the time column in the text file
#print(length(mydata$time))										# write the length of the vecteur (number of records in the distribution)
#save(mydata, file="data/ground_truth_traveltimes_1_NB.RData")	# save the table as a R object
#sink()															# redirect output by default