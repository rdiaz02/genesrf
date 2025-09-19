library(Rmpi)
library(snow)

library(varSelRF)
load("all.real.data.RData")
load("gl.data.RData")

#nodes <- c(1, 10, 20, 60, 120)
nodes <- c(120, 60, 20, 10)

                                        #datanames <- c("lymphoma", "colon", "brain", "nci", "ra", "srbct",
#               "prostate", "vv", "vv3")

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



dm <- expand.grid(dataset = datanames, num.node = nodes, reps = c(1))
walltime <- rep(NA, nrow(dm))

for(i in 1:nrow(dm)) {
    cat("\n Doing i ", i, ".  dataset = ", dm[i, 1],
        " . num.node = ", dm[i, 2], "\n")
    try(stopCluster(TheCluster))
    try(rm("TheCluster"))
    try(rm(TheCluster))
    walltime[i] <- timef(dm[i, 1], dm[i, 2])
    cat("\n       This walltime was ", walltime[i], "\n")
    save.image()
}

dm$walltime <- walltime

save(file = "dm.RData", dm)
