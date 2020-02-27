library(ggplot2)
# comment

setwd("C:/Users/arsii/OneDrive/Documents/LST_project/")
data <- read.csv("screen_data.csv",header = TRUE)

data$time = (as.POSIXct(data$time, origin="1970-01-01"))
data$event <- rep(1,nrow(data))
data$wdays <- weekdays.POSIXt(data$time)
attach(data)

# try to do some binning
data_bins = data.frame(data, cuts = cut(data$time, breaks="1 hours", labels=FALSE))
data_filtered = data_bins[data_bins$wdays %in% c("Monday","Tuesday","Wednesday","Thursday"),]

bins = data_filtered$cuts
mods = replicate(length(bins), 0)

t.str <- strptime(data_bins[1,]$time, "%Y-%m-%d %H:%M:%S")
offset <- as.numeric(format(t.str, "%H")) - 1

for (i in 1:length(bins)) {
  mods[i] = (bins[i] + offset) %% 24
  
}

counts = aggregate(data.frame(count = mods), list(value = mods), length)

tot = sum(counts$count)

ggplot(data=counts, aes(x=value,y=count/tot)) +
  geom_bar(stat="identity",fill="steelblue") + 
  ggtitle("Screen events / Mon-Thu normalized hourly counts") +
  labs(y="Screen events / proportion", x="Hours") 


  




