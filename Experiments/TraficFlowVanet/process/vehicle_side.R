load("data/ground_truth_traveltimes_1_NB.RData")		# load previsously saved mydata R object
end = mydata$travel_time+mydata$departure_time			# compute the timestamp when the car reach the end of the edge
th = mean(mydata$travel_time)+sd(mydata$travel_time)	# compute AT = mean of distribution
alerts = end[ mydata$travel_time > th ]					# produce a alert Vector
print(length(alerts))									# display alert amount
hist(alerts,breaks=100,col = "lightblue")				# create histogram
den <- density(alerts)									# create density curve
lines(den, col = "red")									# display density curve