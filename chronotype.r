#################################################################################
# This script is for finding out the chronotype from the mobile phone screen data 
# Necessary libraries:
# - ggplot2
# - tidyverse
# (c) Arsi Ikäheimonen 2020 - arsi.ikaheimonen@aalto.fi
#################################################################################

# load library
library(tidyverse)

# set path and load the data
#setwd("G:/LST/") # <- path to data
setwd("C:/Users/arsii/OneDrive/Documents/LST_project/") 
data <- read.csv("screen_data.csv",header = TRUE)
baseline <- read.csv("population_rhythm.csv",header = FALSE)

# modify baseline dataframe
names(baseline)[1] <- "events"
baseline$hours <- seq.int(nrow(baseline))

# modify screen event dataframe
data$time = (as.POSIXct(data$time, origin="1970-01-01"))
data$event <- rep(1,nrow(data))
data$wdays <- weekdays.POSIXt(data$time)
data$hours <- as.numeric(substr(data$time, 12, 13))


# dataframe for binned screen events
data_bins <- data %>% 
  group_by(wdays,hours) %>%
  summarise(sum = sum(event))

# vector for event counts
event_counts = rep(0,times=(24*7))
z = c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
i = 1 

# collect the counts from original binned data
for (d in z) {
  for (h in c(0:23)) {
    counts =  as.integer(data_bins[ which( data_bins$wdays == d & data_bins$hours == h) , ]$sum)
    if (identical(counts,integer(0))) {
      # no events here
    } else {
      event_counts[i] <- counts
    }
    i = i + 1
  }
}

# create a normalized dataframe for plotting
event_counts = event_counts / length(data$event)
hrs = seq(1:(7*24))
plotdata <- data.frame(event_counts,hrs)
plotdata <- plotdata[1:96,]
## Determine highlighted regions
v <- rep(0,96)
v[c(1:2, 6:7, 25:26, 30:31, 49:50, 54:55, 73:74, 78:79)] <- 1

## Get the start and end points for highlighted regions
inds <- diff(c(0, v))
start <- plotdata$hrs[inds == 1]
end <- plotdata$hrs[inds == -1]
if (length(start) > length(end)) end <- c(end, tail(plotdata$hrs, 1))

## highlight region data
rects <- data.frame(start=start, end=end, group=seq_along(start))

# plot screen events, regions of interest and baseline
ggplot(data=plotdata[1:(4*24),], aes(x=hrs,y=event_counts)) +
  geom_bar(stat="identity",fill="steelblue",alpha=0.7) + 
  geom_line(data=baseline[1:(4*24),], aes(x=hours,y=events),size=1) +
  geom_rect(data=rects, inherit.aes=FALSE, aes(xmin=start, xmax=end, ymin=0,
                                               ymax=(1.1*(max(max(plotdata$event_counts),max(baseline$events)))), group=group), color="transparent", fill="orange", alpha=0.15) +
  ggtitle("Screen events vs. baseline / mon-thu") +
  labs(y="Screen events / proportion", x="Hours") +
  ylim(0,1.1*(max(max(plotdata$event_counts),max(baseline$events))))

# calculate differences between the baseline morning hours and late night hours
# am mask
v_am <- rep(0,96)
v_am[c(1:2, 25:26, 49:50,  73:74)] <- 1
# pm mask
v_pm <- rep(0,96)
v_pm[c(6:7, 30:31, 54:55, 78:79)] <- 1

# mask am counts
count_am = event_counts[as.logical(v_am)]
count_pm = event_counts[as.logical(v_pm)]
# mask pm counts
base_am = baseline$events[as.logical(v_am)]
base_pm = baseline$events[as.logical(v_pm)]

# differences
diff_am = base_am - count_am
diff_pm = base_pm - count_pm

sprintf("Am differences: baseline - measured:")
sprintf("%.10f",mean(diff_am))
sprintf("Pm differences: baseline - measured:")
sprintf("%.10f",mean(diff_pm))
