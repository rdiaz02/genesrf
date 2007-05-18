library(varSelRF)
load("all.real.data.RData")


nodes <- c(1, 10, 20, 60, 120)
datanames <- c("lymphoma", "colon", "brain", "nci", "ra", "srbct",
               "prostate", "vv", "vv3")


timef <- function(dataset, num.node) {
    basicClusterInit(num.node)
    datax <- get(paste(dataset, ".data", sep = ""))
    datay <- get(paste(dataset, ".class", sep = ""))
    return(unix.time(trash <- varSelRFBoot(datax, datay,
                                           TheCluster = "TheCluster"))[3])
}

