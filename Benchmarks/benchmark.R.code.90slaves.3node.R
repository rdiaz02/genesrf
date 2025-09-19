### I forgot to run it with 90 slaves.


system("lamhalt")
system("lamboot -v lamb-host.karl02.3.def")

library(Rmpi)
library(snow)
library(varSelRF)
load("all.real.data.RData")
load("gl.data.RData")

#nodes <- c(1, 10, 20, 60, 120)
nodes <- c(90)

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



dm90.3 <- expand.grid(dataset = datanames, num.node = nodes, reps = c(1))
walltime <- rep(NA, nrow(dm90.3))

for(i in 1:nrow(dm90.3)) {
    cat("\n Doing i ", i, ".  dataset = ", dm90.3[i, 1],
        " . num.node = ", dm90.3[i, 2], "\n")
    try(stopCluster(TheCluster))
    try(rm("TheCluster"))
    try(rm(TheCluster))
    walltime[i] <- timef(dm90.3[i, 1], dm90.3[i, 2])
    cat("\n       This walltime was ", walltime[i], "\n")
    save.image()
}

dm90.3$walltime <- walltime

save(file = "dm90.3.RData", dm90.3)
