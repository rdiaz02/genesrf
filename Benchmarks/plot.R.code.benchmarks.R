load("one.slave.RData")
dm0 <- dm[1:5,]
dm0$walltime <- walltime[1:5]
load("dm.RData")
load("dm90.RData")
load("dm90.3.RData")
load("dm60.2.RData")

dm0$factor.num.node <- as.character(dm0$num.node)
dm$factor.num.node <- as.character(dm$num.node)
dm90$factor.num.node <- as.character(dm90$num.node)
dm90.3$factor.num.node <- '90(3)'
dm60.2$factor.num.node <- '60(2)'

dm.all <- rbind(dm0, dm, dm90, dm90.3, dm60.2)
dm.all$factor.num.node <- factor(dm.all$factor.num.node,
                                 levels = c("1", "10", "20", "60", "60(2)", "90", "90(3)", "120"))

dm.all <- dm.all[order(dm.all$factor.num.node),]


#postscript("R_timings_1.eps", width = 11, height = 8, paper = "special")
pdf("R_timings_1.pdf", width = 11, height = 8, paper = "special")

par(las = 1)
par(cex = 1.4)
par(mar = c(3.8, 5.2, .81, .81))  
par(mgp = c(4, 1, 0))
par(cex.lab = 1.4)
plot(walltime ~ as.numeric(factor.num.node), type = "b", axes = FALSE,
     data = subset(dm.all, dataset == "gl"),
     ylim = c(min(dm.all$walltime), max(dm.all$walltime)),
     col = rainbow(5)[1],
     lty = 2,
     log = "y",
     xlab = "",
     ylab = "User wall time (seconds)",
     lwd = 2)
box()
axis(2)
axis(1, at = as.numeric(dm.all$factor.num.node),
     labels = as.character(dm.all$factor.num.node))
mtext("Number of Rmpi slaves", side = 1, line = 2.5, cex = 2)
lines(walltime ~ as.numeric(factor.num.node), type = "b", lwd = 2,
      data = subset(dm.all, dataset == "vv3"),
      col = rainbow(5)[2],
      lty = 1)
lines(walltime ~ as.numeric(factor.num.node), type = "b", lwd = 2,
      data = subset(dm.all, dataset == "lymphoma"),
      col = rainbow(5)[3],
      lty = 3)
lines(walltime ~ as.numeric(factor.num.node), type = "b", lwd = 2,
      data = subset(dm.all, dataset == "brain"),
      col = rainbow(5)[4],
      lty = 4)
lines(walltime ~ as.numeric(factor.num.node), type = "b", lwd = 2,
      data = subset(dm.all, dataset == "ra"),
      col = rainbow(5)[5],
      lty = 5)

legend(x = 6, y = 60000,
       c("Leukemia", "Breast3", "Lymphoma", "Brain", "Adeno.")[c(5, 2, 4, 3, 1)],
       lty = c(2, 1, 3, 4, 5)[c(5, 2, 4, 3, 1)],
       col = rainbow(5)[c(5, 2, 4, 3, 1)],
       lwd = 2)

dev.off()



########################

## benchmarking with prostate data set

mt <- tapply(dmB$walltime, list(dmB$number.genes, dmB$number.arrays), mean)
mean.for.6033.genes <-  mt[5, -5]
mean.for.102.arrays <-  mt[-5, 5]


pdf("R_timings_2.pdf", width = 11, height = 7, paper = "special")
postscript("R_timings_2.eps", width = 11, height = 7, paper = "special")
par(mar = c(4.8, 5.8, 4.8, .81))  
par(mgp = c(3.2, 1, 0))
par(cex.main = 1.75)
par(cex.lab = 1.72)
par(cex.axis = 1.2)
par(cex.las = 1.7)
par(mfrow = c(1, 2))
par(las = 1)
plot(walltime ~ as.numeric(factor(number.arrays)), data = dmB[1:12, ],
     type = "p", xlab = "Number of arrays",
     ylab = "User wall time (seconds)", log = "y",
     axes = FALSE,
     main = "Prostate data set, 6033 genes",
     cex = 1.8)
box()
axis(2)
axis(2, at = c(180, 400, 1500))
axis(1, at = c(1, 2, 3, 4), labels = c("20", "40", "80", "100"))
lines(mean.for.6033.genes ~ c(1, 2, 3, 4), lwd = 2.2)

par(las = 1)
plot(walltime ~ as.numeric(factor(number.genes)), data = dmB[13:24, ],
     type = "p", xlab = "Number of genes",
     ylab = "User wall time (seconds)", log = "y",
     axes = FALSE,
     main = "Prostate data set, 102 samples",
     cex = 1.8)
box()
axis(2)
axis(2, at = c(250, 1800))
axis(1, at = c(1, 2, 3, 4), labels = c("1000", "2000", "4000", "6000"))
lines(mean.for.102.arrays ~ c(1, 2, 3, 4), lwd = 2.2)
dev.off()
