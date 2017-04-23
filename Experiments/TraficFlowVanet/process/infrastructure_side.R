mydata = read.csv("data/ground_truth_traveltimes_1_NB.csv")		# load source data
sink("results/ground_truth_traveltimes_1_NB.txt")				# redirect output to a text file
print(summary(mydata$travel_time))								# write a summary of the time column in the text file
print(length(mydata$travel_time))	
print(var(mydata$travel_time))	
print(sd(mydata$travel_time))									# write the length of the vecteur (number of records in the distribution)
save(mydata, file="data/ground_truth_traveltimes_1_NB.RData")	# save the table as a R object
sink()															# redirect output by default