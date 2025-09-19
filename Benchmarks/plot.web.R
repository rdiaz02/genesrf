timings <- scan("web.bnchmk.txt")
## we forgot to run Leukemia first time, we enter the three values here
timings <- c(timings, 221.606, 220.339, 220.343)
data.sets <- c('Colon',
               'Srbct',
               'NCI',
               'Prostate',
               'Breast3',
               'Breast2',
               'Lymph.',
               'Brain',
               'Adeno.')
data.sets <- factor(c(rep(data.sets, 3), rep("Leuk.", 3)))

postscript("web_timings.eps", width = 11, height = 8, paper = "special")
pdf("web_timings.pdf", width = 11, height = 8, paper = "special")
par(las = 1)
par(cex = 1.3)
par(cex.lab = 1.4)
## stripchart(timings ~ data.sets, vertical = TRUE, pch = 21,
##            col = rainbow(9), xlab = "",
##            ylab = "User wall time (seconds)")

plot(timings ~ as.numeric(factor(data.sets)), pch = 21,
     bg = rainbow(9), xlab = "",
     ylab = "User wall time (seconds)", axes = FALSE,
     cex = 1.8)
axis(2)
box()
axis(1, at = 1:10, labels = levels(data.sets))

mtext("(76x9868)", side = 1, at = 1, line = 2, cex = 1.2)
mtext("(42x6000)", side = 1, at = 2, line = 2, cex = 1.2)
mtext("(78x4869)", side = 1, at = 3, line = 2, cex = 1.2)
mtext("(96x4869)", side = 1, at = 4, line = 2, cex = 1.2)
mtext("(62x2000)", side = 1, at = 5, line = 2, cex = 1.2)
mtext("(38x3051)", side = 1, at = 6, line = 2, cex = 1.2)
mtext("(62x4026)", side = 1, at = 7, line = 2, cex = 1.2)
mtext("(61x5244)", side = 1, at = 8, line = 2, cex = 1.2)
mtext("(102x6033)", side = 1, at = 9, line = 2, cex = 1.2)
mtext("(63x2308)", side = 1, at = 10, line = 2, cex = 1.2)
dev.off()

