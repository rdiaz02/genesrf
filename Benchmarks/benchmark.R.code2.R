### ojo con el num.node y el lambhost.

system("lamhalt")
system("lamboot -v lamb-host.karl02.def")


library(Rmpi)
library(snow)

library(varSelRF)
load("all.real.data.RData")


nodes <- c(60)
datanames <- c("prostate")

ngenes <- c(1000, 2000, 4000, 6000)
narrays <- c(20, 40, 80, 100)



timef <- function(ngene, narray, dataset = "prostate", num.node = 120) {
    try(stopCluster(TheCluster))
    try(rm("TheCluster"))
    basicClusterInit(num.node)
    datax <- get(paste(dataset, ".data", sep = ""))
    datay <- get(paste(dataset, ".class", sep = ""))

    arr.sample <- sample(1:nrow(datax), narray)
    gen.sample <- sample(1:ncol(datax), ngene)

    yy <- datay[arr.sample]
    xx <- datax[arr.sample, gen.sample]
    
    return(unix.time(trash <- varSelRFBoot(xx, yy,
                                           TheCluster = TheCluster))[3])
}


dm1 <- expand.grid(number.genes = 6033, number.arrays = narrays, reps = c(1, 2, 3))
dm2 <- expand.grid(number.genes = ngenes, number.arrays = 102, reps = c(1, 2, 3))
dmB <- rbind(dm1, dm2)

walltime2 <- rep(NA, nrow(dmB))

for(i in 1:nrow(dmB)) {
    cat("\n Doing i ", i, ".  ngenes = ", dmB[i, 1],
        " . narrays = ", dmB[i, 2], "\n")
    try(stopCluster(TheCluster))
    try(rm("TheCluster"))
    try(rm(TheCluster))
    walltime2[i] <- timef(dmB[i, 1], dmB[i, 2])
    cat("\n       This walltime was ", walltime2[i], "\n")
    save.image()
}

dmB$walltime <- walltime2

save(file = "dmB.RData", dmB)
