# demo: central limit theorem

library('animation')
replot <- function(x) {
  for (i in seq(from=1, to=length(x), by=10)){
    hist(dat[1:i], xlim=c(-5, 5), ylim=c(0, length(x)/10), breaks = 30, main=paste('The sampling number of', i), xlab='', )
  }
}

dat <- rnorm(10000)
saveGIF(replot(dat), movie.name="sample.gif", interval=0.04)
