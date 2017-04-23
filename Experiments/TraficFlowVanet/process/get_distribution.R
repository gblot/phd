mydata = read.csv("data/ground_truth_traveltimes_2_NB.csv")		# load source data
sink("results/ground_truth_traveltimes_2_NB.txt")				# redirect output to a text file
print(summary(mydata$time))										# write a summary of the time column in the text file
print(length(mydata$time))	
print(var(mydata$time))	
print(sd(mydata$time))										# write the length of the vecteur (number of records in the distribution)
save(mydata, file="data/ground_truth_traveltimes_2_NB.RData")	# save the table as a R object
sink()															# redirect output by default