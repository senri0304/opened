#List up files
files = list.files('./exp04C/data',full.names=T)
#files = c(files, list.files('./exp05/data2',full.names=T))
#files = c(files, list.files('./exp05/data3',full.names=T))
f = length(files)

si = gsub(".*(.)2018.*", "\\1", files)
n = length(table(si))
usi = unique(si)

# Load data and store
temp = read.csv(files[1])
temp$si = si[1]
m = nrow(temp)
for (i in 2:f) {
  d = read.csv(files[[i]])
  d$si = si[i]
  temp = rbind(temp, d)
}
dat = temp
dat$sub = dat$si
dat$si = NULL

# Reshape data for anova
ano = aggregate(x=dat$cdt, by=dat[c("disparity","sub")], FUN=mean)
library("reshape2")
dc = dcast(ano, sub ~ disparity, fun.aggregate = mean, value.var="x")
dc = subset(dc, select = -sub)
ddd = ncol(dc)

# Calculate SD
sd = sd(dc[,1])
for (l in 2:ddd) {sd = cbind(sd, sd(dc[,l]))}

# Calculate SE
se = sd/sqrt(n)

# Anovakun
#source("anovakun_481.txt", encoding = "CP932")
#anovakun(dc,"sA", 6, peta=T)

# Plot indivisual data
par(mfrow=c(2,3))
for (k in 1:n){
  camp = subset(dat, dat$sub == usi[k], c("disparity", "cdt"))
  plot(camp, xlim=c(-50,30), ylim=c(0,30), type = "p",xlab="vertical disparity(min of arc)", ylab="cumulative disapperance times(sec)", main = toupper(usi[k]))
  par(new=T)
  plot(aggregate(x = camp$cdt, by=camp["disparity"], FUN=mean), type = "l", col="blue", xlim=c(-50,30), ylim=c(0,30), ylab="", xlab="")
  par(new=F)
}
par(mfrow=c(1,1))
# Plot cdt with error bar
cdt = aggregate(x=dat$cdt, by=dat["disparity"],FUN=mean)
plot(cdt, xlim=c(-50,30), ylim=c(0,30), type="b", xlab="vertical disparity(min of arc)", ylab="mean of cdt(sec)")
arrows(cdt$disparity, cdt$x-se, cdt$disparity, cdt$x+se, length=0.05, angle=90, code=3)

