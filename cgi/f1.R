## How to call Rmpi


## Define an explicit .Last, so that we know exactly what is the last
## thing in .Rout in case of normal termination. (And normal
## termination includes catching a user error!).


## Logic can lead to problems: if an unexpectec crash, .Last is not
## executed, so LAM stuff not cleaned.

require(Cairo)
version
system("hostname")

rm(list = ls())

.Last <- function() {
    RterminatedOK <- file("RterminatedOK", "w")
    cat("\nNormal termination\n", file = RterminatedOK)
    flush(RterminatedOK)
    close(RterminatedOK)    
    ## try(stopCluster(TheCluster))
    cat("\n\n Normal termination\n")
    ## try(system(paste("/http/mpi.log/killLAM.py", lamSESSION, "&")))
    try(mpi.quit(save = "no"), silent = TRUE)
}

startExecTime <- format(Sys.time())

pid <- Sys.getpid()
write.table(file = "pid.txt", pid,
            row.names = FALSE,
            col.names = FALSE)

## attach pid to name in R.running.procs
hostn <- system("hostname", intern = TRUE)
new.name1 <- unlist(strsplit(getwd(), "/"))
new.name1 <- paste(new.name1[length(new.name1)], "@", hostn, sep = "")
new.name <- paste("R.", new.name1, "%", pid, sep = "")
new.name1 <- paste("R.", new.name1, sep = "")
system(paste("mv ../../R.running.procs/", new.name1,
             " ../../R.running.procs/", new.name,
             sep = ""))



##############################################
##############################################
######                              ##########
######         Error checking       ##########
######                              ##########
##############################################
##############################################


caughtUserError <- function(message) {
    CairoPNG("fboot001.png", width = png.width, height = png.height, ps = 10)
    plot(x = c(0, 1), y = c(0, 1),
         type = "n", axes = FALSE, xlab = "", ylab = "")
    box()
    text(0.5, 0.7, "There was a PROBLEM with your data.")
    text(0.5, 0.5,
    "Please read carefully the error messages under Results,")
    
    text(0.5, 0.3, "fix the problem, and try again.")
    dev.off()
    sink(file = "results.txt")
    cat(message)
    sink()
    sink(file = "exitStatus")
    cat("Error\n\n")
    cat(message)
    sink()
    quit(save = "no", status = 11, runLast = TRUE)
}



caughtOurError <- function(message, runLast = TRUE) {
    CairoPNG("ErrorFigure.png", width = png.width, height = png.height,
             ps = 10)
    plot(x = c(0, 1), y = c(0, 1),
         type = "n", axes = FALSE, xlab = "", ylab = "")
    box()
    text(0.5, 0.7, "There was a PROBLEM with the code.")
    text(0.5, 0.5,
    "Please let us know (send us the URL),")
    
    text(0.5, 0.3, "so that we can fix it.")
    dev.off()
    sink(file = "results.txt")
    cat(message)
    sink()
    sink(file = "exitStatus")
    cat("Error\n\n")
    cat(message)
    sink()
    quit(save = "no", status = 11, runLast = runLast)
}


caughtMPIError <- function(message, runLast = FALSE) {
    ## so that tryRrun2.py tries again
    sink(file = "results.txt")
    cat(message)
    sink()
    sink(file = "exitStatus")
    cat("Error\n\n")
    cat(message)
    sink()
    quit(save = "no", status = 11, runLast = runLast)
}




#library(CGIwithR)
# library(GDD)
png.width = 550
png.height = 550
##png.res = 144
png.pointsize = 12
png.family = "Helvetica"

graphDir <- paste(getwd(), "/", sep = "")

## This is just for testing
#webPNG(file = "f1.png", width = png.width,
#       height = png.height, res = png.res,
#       pointsize = png.pointsize,
#       family = png.family); plot(rnorm(10)); dev.off()
       

##############################################
####       Constants for var sel rf #########
##############################################

numBootstrap <- 200
numRand <- 50
numTree <- 2000




##############################################
####    MPI initialization          #########
##############################################


library(varSelRF)
## library(snow)
## library(Rmpi)
## library(rsprng)
library(parallel)




## trylam <- try(
##               lamSESSION <- scan("lamSuffix", what = "character", sep = "\t", strip.white = TRUE))

## if(mpi.universe.size() < 2)
##     caughtMPIError(paste("\n Error with MPI: mpi.universe.size() < 2.",
##                          "Please let us know so we can fix the code."),
##                    runLast = FALSE)
## trycode <- (
##             basicClusterInit(mpi.universe.size()) ## use all CPUs in lam universe
##             )
## if(inherits(trycode, "try-error")) {
##   caughtOurError(paste("Could not initialize MPI, with error",
##                        trycode, ". \n Please let us know so we can fix the code."))

##   sink(file = "/http/mpi.log/GeneSrFErrorLog", append = TRUE)
##   cat("Snow failing  on node", system("hostname"),
##       "on", date(), "from dir",
##       getwd(), "\n")
##   sink()
## }


sink(file = "mpiOK")
cat("MPI started OK\n")
sink()



#################################################################
## enter info into lam suffix log table

tmpDir <- getwd()
## sed.command <- paste("sed -i 's/RprocessPid\t",
##                      lamSESSION, "\t", hostn, "/",
##                      pid, "\t",
##                      lamSESSION, "\t", hostn, "/' ",
##                      "/http/mpi.log/LAM_SUFFIX_Log",
##                      sep = "")
## ## debugging:
## sed.command

## system(sed.command)





idtype <- try(scan("idtype", what = "", n = 1))
organism <- try(scan("organism", what = "", n = 1))


##############################################
##############################################
######                              ##########
######   HTML output stuff          ##########
######    (will later move to       ##########
######       the library)           ##########
######                              ##########
##############################################
##############################################


linkGene <- function(id) {
    ## Returns a string for use in a web page with a call
    ## to IDClight.
    if ((idtype == "None") | (organism == "None"))
        return(id)
    else
        paste("<a href=\"http://idclight.bioinfo.cnio.es/IDClight.prog",
              "?idtype=", idtype, "&id=", id, "&org=",
              organism,"\" target=\"icl_window\" >",id,"</a>", sep = "")
## target=\"icl_window\"\
}
     


linkGene2 <- function(id) {
    ## Returns a string for use in a web page with a call
    ## to IDClight.
    if ((idtype == "None") | (organism == "None"))
        return(id)
    else 
        paste("http://idclight.bioinfo.cnio.es/IDClight.prog",
              "?idtype=", idtype, "&id=", id, "&org=",
              organism, sep = "")
}

library(Hmisc)

html.data.frame <- function (object, first.col = "Name",
                             file = paste(first.word(deparse(substitute(object))), 
                             "html", sep = "."), append = FALSE, link = NULL, linkCol = 1, 
                             linkType = c("href", "name"), ...) 
{
    linkType <- match.arg(linkType)
    x <- format.df(object,  numeric.dollar = FALSE, ...)
    adj <- attr(x, "col.just")
    if (any(adj == "r")) 
        for (i in seq(along = adj)[adj == "r"]) x[, i] <- paste("<div align=right>", 
            x[, i], "</div>", sep = "")
    if (length(r <- dimnames(x)[[1]])) 
        x <- cbind(first.col = r, x)
    colnames(x)[1] <- first.col
    cat("<TABLE BORDER>\n", file = file, append = append)
    cat("<tr>", paste("<td>", dimnames(x)[[2]], "</td>", sep = ""), 
        "</tr>\n", sep = "", file = file, append = file != "")
    if (length(link)) 
        x[, linkCol] <- ifelse(link == "", x[, linkCol], paste("<a ", 
            linkType, "=\"", link, "\">", x[, linkCol], "</a>", 
            sep = ""))
    for (i in 1:nrow(x)) cat("<tr>", paste("<td>", x[i, ], "</td>", 
        sep = ""), "</tr>\n", sep = "", file = file, append = file != 
        "")
    cat("</TABLE>\n", file = file, append = file != "")
    structure(list(file = file), class = "html")
}


HTML.varSelRFBoot <- function(object,
                              return.model.freqs = FALSE,
                              return.class.probs = TRUE,
                              return.var.freqs.b.models = TRUE,
                              file = file, append = FALSE,
                              ...) {
    sink(file, append)
    cat("<h3>Variable selection using all data </h3>")
    cat("<h4>Variables used</h4>")
    
    cat("<TABLE frame=\"box\">\n")
    cat("<tr><th width=200>Gene name</th></tr>\n")
    for(i in 1:length(object$all.data.vars)) {
        cat("<tr><td>", linkGene(object$all.data.vars[i]), "</td></tr>\n")
    }
    cat("</TABLE>")
    cat(paste("<p> Number of variables used: ",  length(object$all.data.vars), "</p>"))
    cat("<hr /><br><h3>Bootstrap results</h3>")
    cat(paste("<p><b>Bootstrap (.632+) estimate of prediction error</b>  (using",
              object$number.of.bootsamples, "bootstrap iterations):",
              round(object$bootstrap.pred.error, 5)))
    cat(paste("<p>Resubstitution error:                          ",
              round(object$resubstitution.error, 5),  "</p>"))
    cat(paste("<p>Leave-one-out bootstrap error:                 ",
              round(object$leave.one.out.bootstrap.error, 5), "</p>"))
    nk <- as.vector(table(object$class))
    cat(paste("<p>Error rate at random:                          ",
              round(1 - (max(nk)/sum(nk)), 5), "</p>"))
    cat("<br><p>Number of vars in bootstrapped forests:        ")
    cat("<pre>")
    print(summary(object$number.of.vars))
    cat("</pre></p>")
    cat("</p><p>Overlapp of bootstrapped forests with forest from all data</p>")
    cat("<pre>")
    print(summary(object$overlap))
    cat("</pre>")
    cat("</p><br>")
    if(return.var.freqs.b.models) {
        tttmp <- sort(table(object$all.vars.in.solutions),
                      decreasing = TRUE)/object$number.of.bootsamples
        ntttmp <- names(tttmp)
        cat("<h3>Variable freqs. in bootstrapped models</h3>")
        cat("<TABLE frame=\"box\">\n")
        cat("<tr><th width=200>Gene name</th><th>Frequency</th></tr>\n")
        for(i in 1:length(tttmp)) {
            cat("<tr><td>", linkGene(ntttmp[i]), "</td><td>",
                tttmp[i], "</td></tr>\n")
        }
        cat("</TABLE>")
    }
    in.all.data <-
        which(names(table(object$all.vars.in.solutions)) %in% object$all.data.vars)
    cat("<br><h3>Variable freqs. of variables in forest from all data, and summary</h3>")
    tttmp <- sort(table(object$all.vars.in.solutions)[in.all.data],
                  decreasing = TRUE)/object$number.of.bootsamples
    ntttmp <- names(tttmp)
    cat("<TABLE frame=\"box\">\n")
    cat("<tr><th width=200>Gene name</th><th>Frequency</th></tr>\n")
    for(i in 1:length(tttmp)) {
        cat("<tr><td>", linkGene(ntttmp[i]), "</td><td>",
            tttmp[i], "</td></tr>\n")
    }
    cat("</TABLE>")
    cat("<br>")
    cat("<pre>")
    print(summary(tttmp))
    cat("</pre>")
    if(return.model.freqs) {
        tmp.table <- sort(table(object$all.solutions),
                          decreasing = TRUE)/object$number.of.bootsamples
        n.tmp.table <- names(tmp.table)
        if(is.vector(tmp.table)) ## can fail in this case
            dim(tmp.table) <- c(length(tmp.table), 1)
        else
            dim(tmp.table) <- c(dim(tmp.table), 1)
        rownames(tmp.table) <- n.tmp.table
        colnames(tmp.table) <- "Freq."
        cat("<hr><br><h3>Model frequencies in bootstrap samples</h3>")
        cat("<p><a href=\"./model.freqs.table.html\">View</a> model frequencies table (can be large)</p>")
        html.data.frame(tmp.table, file = "model.freqs.table.html",
                        first.col = "Model")
    }
    if(return.class.probs) {
        
        cat("<hr><br><h3>Mean class membership probabilities from out of bag samples</h3>")
        sink()
        mean.class.probs <- apply(object$prob.predictions, c(1, 2),
                                  function(x) mean(x, na.rm = TRUE))
        colnames(mean.class.probs) <- levels(object$class)
        mean.class.probs <- data.frame(mean.class.probs)
        html.data.frame(round(mean.class.probs, 4), file = file, append = TRUE,
                        first.col = "Subject/array")
    } else{
        sink()
    }
}








tmp <- try(
       	   system("sed 's/\"//g' covariate > cvt; mv cvt covariate")
	   )


num.cols.covariate <- count.fields("covariate", sep = "\t",
                                   quote = "",
                                   comment.char = "#")

if(length(unique(num.cols.covariate)) > 1) {
    emessage <-
    paste("The number of columns in your covariate file\n",
          "is not the same for all rows (genes).\n",
          "We find the following number of columns\n",
          paste(num.cols.covariate, collapse = " "))
    caughtUserError(emessage)
}

tryxdata <- try(
xdata <- read.table("covariate", header = FALSE, sep = "\t",
                    strip.white = TRUE,
                    comment.char = "#",
		    quote = ""))

if(inherits(tryxdata, "try-error"))
    caughtUserError("The covariate file is not of the appropriate format\n")


geneNames <- NA
geneNames <- try(xdata[, 1])

if(any(is.na(geneNames))) {
    caughtUserError("The gene names (first column of your covariate file) contains missing values. \n That is not allowed.\n")
}



xdata <- xdata[, -1]

if(length(unique(geneNames)) < length(geneNames)) {
    dupnames <- which(duplicated(geneNames))
    emessage <- paste("Gene names are not unique.\n",
                      "Please change them so that they are unique.\n",
                      "The duplicated names are in rows", dupnames, "\n")
    caughtUserError(emessage)
}
    
rownames(xdata) <- geneNames


arrayNames <- scan("arrayNames", sep = "\t", what = "char", quote = "")



if(length(arrayNames) > 0) {
    arrayNames <- arrayNames[-1]
    if(length(unique(arrayNames)) < length(arrayNames)) {
        dupnames <- which(duplicated(arrayNames))
        emessage <- paste("Array names are not unique.\n",
                          "Please change them so that they are unique.\n",
                          "The duplicated names are ", dupnames, "\n")
        caughtUserError(emessage)
    }
    if(ncol(xdata) != length(arrayNames)) {
      emessage <- paste("We get that the number of columns in your data (", ncol(xdata), ")\n",
                        "is different from the number of column names (", length(arrayNames), ")\n",
                        "Check for things such as '#' or '#NULL!' in the middle of your data.\n")
      caughtUserError(emessage)
    }
    colnames(xdata) <- arrayNames
}

xdata <- t(xdata)

trycl <- try(
             Class <- factor(scan("class", sep = "\t", what = "char", strip.white = TRUE, nlines = 1))
             )
## to prevent problems with a space at end of classes

if(inherits(trycl, "try-error"))
    caughtUserError("The class file is not of the appropriate format\n")

if(Class[length(Class)] == "") Class <- factor(Class[-length(Class)])


tclass <- table(Class)

if(length(unique(Class)) < 2) {
    caughtUserError(paste("Your data should contain at least two classes\n",
                       "but your data have only one.\n"))
}

if(min(tclass) < 3) {
    caughtUserError(paste("At least one of your classes has less\n",
                       "than 3 cases/subjects/arrays. Although \n",
                       "the programs can deal with this, would you\n",
                       "believe it?\n"))
}


if(length(Class) != dim(xdata)[1]) {
    emessage <- paste("The class file and the covariate file\n",
                      "do not agree on the number of arrays: \n",
                      length(Class), " arrays according to the class file but \n",
                      dim(xdata)[1], " arrays according to the covariate data.\n",
                      "Please fix this problem and try again.\n")
    caughtUserError(emessage)  
}


if(!(is.numeric(xdata))) {
    caughtUserError("Your covariate file contains non-numeric data. \n That is not allowed.\n")
}
    

if(any(is.na(xdata))) {
    caughtUserError("Your covariate file contains missing values. \n That is not allowed.\n")
2}





##############################################
##############################################
######                              ##########
######         Execution            ##########
######                              ##########
##############################################
##############################################

print("First gc")
print(gc())

trycode <- try(
               rf1 <- randomForest(xdata, Class,
                                   ntree = numTree,
                                   importance = TRUE)
               )
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Could not run first random forest, with error",
                       trycode, ". \n Please let us know so we can fix the code."))

print("Second gc")
print(gc())


# basicClusterInit(mpi.universe.size()-1)



## basicClusterInit <- function (clusterNumberNodes = 1,
##                               nameCluster = "TheCluster", 
##                               typeCluster = "MPI") 
## {
##     if (!(typeCluster %in% c("MPI", "PVM"))) 
##         stop("typeCluster needs to be PVM or MPI")
##     library(snow)
##     if (typeCluster == "MPI") {
##         print("Make sure you have the Rmpi package installed and configure your cluster if needed")
##     }
##     if (typeCluster == "PVM") {
##         print("Make sure you have rpvm installed. We have only checked with Rmpi. Then do library(rpvm)")
##     }
##     if (length(find(nameCluster))) 
##         stop("\nThere is another object called ", nameCluster, 
##             ".\n", "This could mean that a cluster with that name already exists;\n", 
##             "   in this case, please use the existing cluster \n", 
##             "   ---you do not need to initialize the cluster, \n", 
##             "   just pass its name as the parameter for 'nameCluster'---\n", 
##             "   or stop that cluster and initialize a new one. \n", 
##             "It could also mean that there is\n", "   already an object with this name; either remove the object\n", 
##             "   or use another name for the cluster.\n")
    
##     assign(nameCluster, makeCluster(clusterNumberNodes, type = typeCluster), 
##         env = .GlobalEnv)
##     sprng.seed <- round(2^32 * runif(1))
##     print(paste("Using as seed for SPRNG", sprng.seed))
##     clusterSetupSPRNG(eval(parse(text = nameCluster)), seed = sprng.seed)
##     clusterEvalQ(eval(parse(text = nameCluster)), library(randomForest))
##     clusterEvalQ(eval(parse(text = nameCluster)), library(varSelRF))
## }


TheCluster <- makeForkCluster(60)
## RNGkind("L'Ecuyer-CMRG")
## It is crucial that we setup the cluseter RGstream properly
clusterSetRNGStream(TheCluster) ## , iseed = round(2^32 * runif(1)))
clusterEvalQ(TheCluster, library(varSelRF))
clusterEvalQ(TheCluster, library(randomForest))

## Maximum of 4 nodes!
## basicClusterInit(min(mpi.universe.size() - 1 , 4))


trycode <- try(
               rf.vs1 <- varSelRF(xdata, Class, fitted.rf = rf1)
               )
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Could not run varSelRF, with error",
                       trycode, ". \n Please let us know so we can fix the code."))

print("Third gc")
print(gc())
               
trycode <- try(
              rf.vs1.boot <- varSelRFBoot(xdata, Class, srf = rf.vs1,
                             TheCluster = TheCluster,
                            bootnumber = numBootstrap)
            )
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Could not run varSelRFBoot, with error",
                       trycode, ". \n Please let us know so we can fix the code."))



trycode <- try(
               rvi <- randomVarImpsRF(xdata, Class, forest = rf1,
                       numrandom = numRand,
                       TheCluster = TheCluster
                                      )
            )
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Could not run randomVarImpsRF, with error",
                       trycode, ". \n Please let us know so we can fix the code."))

stopCluster(TheCluster)


trycode <- try(
             { 
               imps <- importance(rf1, type = 1, scale = FALSE)
               imps <- as.matrix(imps[order(imps, decreasing = TRUE),])
               colnames(imps) <- "Mean Decrease in Accuracy"
             }
            )
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Problem with imps code, with error",
                       trycode, ". \n Please let us know so we can fix the code."))

               

### Now, do the plots; first PNGs for HTML output; at end are the pdfs

               
plots.oobpreds <- levels(Class)




## The folliwing 
## does not work: superimposes axis and main labels
## GDD(file = "fboot", type = "gif", width = png.width,
##         height = png.height, ps = png.pointsize)
## #        pointsize = png.pointsize,
## #        family = png.family)
## par(cex.axis = 0.75); par(cex.lab = 0.8); par(cex.main = 0.8)
## plot(rf.vs1.boot)
## dev.off()

## This next one looks very ugly 
## bitmap(file = "fboot%03d.png", width = 9,
##         height = 9, pointsize = 12)
## par(cex.axis = 0.75); par(cex.lab = 1.4); par(cex.main = 1.4)
## plot(rf.vs1.boot)
## dev.off()


## So we'll go one by one

numgddplots <- length(levels(Class))

for(ngddpl in 1:numgddplots) {
        CairoPNG(file = paste("fbootB", ngddpl, ".png", sep = ""),
                 width = png.width, height = png.height,
                 ps = png.pointsize, bg = "white")
    par(cex.axis = 0.75); par(cex.lab = 1); par(cex.main = 1)
    plot(rf.vs1.boot,
         ErrorNum = FALSE,
         class.to.plot = ngddpl)
    dev.off()
}
CairoPNG(file = paste("fbootB", numgddplots + 1, ".png", sep = ""),
         width = png.width, height = png.height, ps = png.pointsize,
         bg = "white")
par(cex.axis = 0.75); par(cex.lab = 1); par(cex.main = 1)
par(las = 2)
par(mar = c(5, 5, 4, 2) + 0.1)
par(mgp = c(4, 1, 0))
plot(rf.vs1.boot,
     ErrorNum = TRUE,
     oobProb = FALSE)
dev.off()

CairoPNG(file = "fimpspec-all.png", width = png.width,
         height = png.height, ps = png.pointsize)
par(cex.axis = 0.75); par(cex.lab = 1.2); par(cex.main = 1.2)
randomVarImpsRFplot(rvi, rf1,
                    main = "Importance Spectrum: all genes",
                    overlay = TRUE)
maxy <- max(max(rvi[[1]]), imps)
legend(x = 0.4 * dim(xdata)[2], y = 0.85 * maxy ,
       legend = c("Original data", "Permuted class labels",
       "Mean permuted class labels"),
       pch = c(21, NA, NA),
       lty = 1, lwd = 1.5,
       col = c("black", "lightblue", "red"))
dev.off()

CairoPNG(file = "fimpspec-200.png", width = png.width,
         height = png.height, ps = png.pointsize)
#       pointsize = png.pointsize,
#       family = png.family)
par(cex.axis = 0.75); par(cex.lab = 1.2); par(cex.main = 1.2)
randomVarImpsRFplot(rvi, rf1, nvars = 200,
                    main = "Importance Spectrum: first 200 genes",
                    overlay = TRUE)
dev.off()

CairoPNG(file = "fimpspec-30.png", width = png.width,
         height = png.height, ps = png.pointsize)
par(cex.axis = 0.75); par(cex.lab = 1.2); par(cex.main = 1.2)
randomVarImpsRFplot(rvi, rf1, nvars = 30,
                    main = "Importance Spectrum: first 30 genes",
                    overlay = TRUE)
dev.off()

CairoPNG(file = "fselprobplot.png", width = png.width,
         height = png.height, ps = png.pointsize)
par(cex.axis = 0.75); par(cex.lab = 1.2); par(cex.main = 1.2)
selProbPlot(rf.vs1.boot, k = c(20, 100), 
            main = "Selection Probability Plot")
dev.off()



##sink(file = "results.txt")

trycode <- try(
               HTML.varSelRFBoot(rf.vs1.boot, return.model.freqs = TRUE,
                                 file = "results.txt")
)
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Could not run summary boot, with error",
                       trycode, ". \n Please let us know so we can fix the code."))

sink(file = "results.txt", append = TRUE)
cat("<hr><br><h3>Variable (gene) importances from original data</h3>")
cat("<p><a href=\"./var.imps.table.html\">View</a> variable importances table (can be large)</p>")
sink()
nimps <- rownames(imps)
sink(file = "var.imps.table.html", append = FALSE)
cat("<TABLE frame=\"box\">\n")
cat("<tr><th width=200>Gene name</th><th>Importance</th></tr>\n")
for(i in 1:length(nimps)) {
    cat("<tr><td>", linkGene(nimps[i]), "</td><td>",
        imps[i], "</td></tr>\n")
}
cat("</TABLE>")
sink()


               

### for debugging:
save(file = "all.RData", list = ls())
     
pdf.height <- 12
pdf.width <- 12
### Now the pdfs
pdf(file = "fboot%03d.pdf", onefile = FALSE, width = pdf.width,
        height = pdf.height)
plot(rf.vs1.boot)
dev.off()

          
          
trycode <- (
            {             
              pdf(file = "fimpspec-all.pdf", onefile = FALSE, width = pdf.width,
                  height = pdf.height)
              randomVarImpsRFplot(rvi, rf1,
                                  main = "Importance Spectrum: all genes",
                                  overlay = TRUE)
              
              
              legend(x = 0.45 * dim(xdata)[2], y = 0.85 * maxy,
                     legend = c("Original data", "Permuted class labels",
                       "Mean permuted class labels"),
                     pch = c(21, NA, NA),
                     lty = 1, lwd = 1.5,
                     col = c("black", "lightblue", "red"))
              dev.off()
              
              
              pdf(file = "fimpspec-200.pdf", onefile = FALSE, width = pdf.width,
                  height = pdf.height)
              randomVarImpsRFplot(rvi, rf1, nvars = 200,
                                  main = "Importance Spectrum: first 200 genes",
                                  overlay = TRUE)
              dev.off()
              
              pdf(file = "fimpspec-30.pdf", onefile = FALSE, width = pdf.width,
                  height = pdf.height)
              randomVarImpsRFplot(rvi, rf1, nvars = 30,
                                main = "Importance Spectrum: first 30 genes",
                                  overlay = TRUE)
              dev.off()
              
              
              
              pdf(file = "fselprobplot.pdf", onefile = FALSE, width = pdf.width,
                height = pdf.height)
              selProbPlot(rf.vs1.boot, k = c(20, 100), 
                          main = "Selection Probability Plot")
              dev.off()
            }
            )
if(inherits(trycode, "try-error"))
  caughtOurError(paste("Plotting problem, with error",
                       trycode, ". \n Please let us know so we can fix the code."))


## mpi.exit()
# stopCluster(TheCluster)

## cat(paste("\n Did the call to stopCluster ", date(), " \n"),
##     file = "tmp.checks", append = TRUE)




#########  The latex stuff for report

#originalFilenames <- read.table("fileNamesBrowser")
#all.pdfs <- dir(pattern = "pdf")
#fbootpdfs <- grep("fboot", all.pdfs)

##     Ojo: recall need for escaping the "\".


##### sink(file = "results.tex")
##### cat(
#####     "
##### \documentclass[10pt]{article}
##### \usepackage{ae}
##### \usepackage{aecompl}       
##### \usepackage[latin1]{inputenc}
##### \usepackage{geometry}
##### \geometry{a4paper,tmargin=30mm,bmargin=30mm,lmargin=20mm,rmargin=20mm}
##### \usepackage{setspace}
##### \onehalfspacing
##### \usepackage{graphics}
##### \usepackage{verbatim}
##### \usepackage{amsmath}
##### \usepackage{url}
##### \usepackage [mathlines, displaymath]{lineno} 
##### \title{Automatically generated report from GeneSrF}
##### You run GeneSrF \url{http://genesrf.bioinfo.cnio.es} on ",
#####     startExecTime, 
#####     " using as covariate file \begin{verbatim}",
#####     originalFilenames[1, 1], "\end{verbatim}   and as class file
#####     \begin{verbatim}", originalFilenames[2, 1], "\end{verbatim}



##### \section{Figures}

##### \begin{figure}

##### \begin{center}

##### {\resizebox{12cm}{!}{%
##### \includegraphics{table.eps}}}
##### \end{center}
##### \caption{\Large D�az-Uriarte et al.}
##### \end{figure}





#@-node:ramon.20060206203326.1:@thin /http/genesrf2/cgi/genesrf_f1_leo.R
#@-leo
