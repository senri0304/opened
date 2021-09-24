# List up files
files = list.files('./stereopsis_starterpack/data',full.names=T)
f = length(files)

si = gsub(".*(..)DATE.*","\\1", files)
n = length(table(si))

# Load data and store
temp = read.csv(files[1])
temp$sub = si[1]
for (i in 2:f) {
  d = read.csv(files[[i]])
  d$sub = si[i]
  temp = rbind(temp, d)
}

# Calculate and plot mean
mean = aggregate(x=temp$cdt, by=temp["disparity"], FUN=mean)
plot(x=temp$disparity, y=temp$cdt, xlim=c(0,30), ylim=c(0,30), type="p", xlab="horizontal disparity(min of arc)", ylab="mean of cdt(sec)")
par(new=T)
plot(mean, type="l", col="blue", xlim=c(0,30), ylim=c(0,30), xlab="", ylab="")
par(new=F)


pm = mean[1]
# Plot indivisual data
par(mfrow=c(2,3))
for (i in 1:n){
  camp = subset(temp, temp$sub == si[i], c("disparity", "cdt"))
  plot(camp, xlim=c(0,30), ylim=c(0,30), type="p", xlab="horizontal disparity(min of arc)", ylab="cdt(sec)")
  par(new=T)
  m = aggregate(x=camp$cdt, by=camp["disparity"], FUN=mean)
  pm = cbind(pm, m[2])
  plot(m, type="l", col="blue", xlim=c(0,30), ylim=c(0,30), xlab="", ylab="", main=si[i])
  par(new=F)
}

colnames(pm) <- c("disparity", si)


# dat = temp
# dat = subset(dat, dat["sub"]!="t")
# ano = aggregate(x=dat$cdt, by=dat[c("disparity","sub")], FUN=mean)
# library("reshape2")
# dc = dcast(ano, sub ~ disparity, mean, value.var="x")
# dc = subset(dc, select = -sub)
# d = ncol(dc)
# 
# sd = sd(dc[,1])
# for (l in 2:d) {sd = cbind(sd, sd(dc[,l]))}
# 
# cdt = aggregate(x=dat$cdt, by=dat["disparity"],FUN=mean)
# plot(cdt, xlim=c(0,55), ylim=c(0,10), type="b")
# arrows(cdt[,1], cdt$x-sd, cdt[,1], cdt$x+sd, length=0.05, angle=90, code=3)
# 
# source("anovakun_481.txt", encoding = "CP932")
# anovakun(dc,"sA", 6)