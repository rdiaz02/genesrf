### I forgot to run it with 90 slaves.

system("lamhalt")
system("lamboot -v lamb-host.karl02.2.def")

library(Rmpi)
library(snow)
library(varSelRF)
load("all.real.data.RData")
load("gl.data.RData")

#nodes <- c(1, 10, 20, 60, 120)
nodes <- c(60)

datanames <- c("gl", "lymphoma", "brain", "ra", "vv3")



timef <- function(dataset, num.node) {
    try(stopCluster(TheCluster))
    try(rm("TheCluster"))
    try(rm(TheCluster))
    basicClusterInit(num.node)
    datax <- get(paste(dataset, ".data", sep = ""))
    datay <- get(paste(dataset, ".class", sep = ""))
    return(unix.time(trash <- varSelRFBoot(datax, datay,
                                           TheCluster = TheCluster))[3])
}



dm60.2 <- expand.grid(dataset = datanames, num.node = nodes, reps = c(1))
walltime <- rep(NA, nrow(dm60.2))

for(i in 1:nrow(dm60.2)) {
    cat("\n Doing i ", i, ".  dataset = ", dm60.2[i, 1],
        " . num.node = ", dm60.2[i, 2], "\n")
    try(stopCluster(TheCluster))
    try(rm("TheCluster"))
    try(rm(TheCluster))
    walltime[i] <- timef(dm60.2[i, 1], dm60.2[i, 2])
    cat("\n       This walltime was ", walltime[i], "\n")
    save.image()
}

dm60.2$walltime <- walltime

save(file = "dm60.2.RData", dm60.2)
