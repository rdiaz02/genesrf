#!/usr/bin/python

## All this code is copyright Ramon Diaz-Uriarte. For security reasons, this is for
## now confidential. No license is granted to copy, distribute, or modify it.
## Once everything is OK, it will be distributed under the GPL.


import sys
import os
import cgi 
import types
import time
import shutil
import string
import signal
import re
import glob
import tarfile

import cgitb
##cgitb.enable() ## zz: eliminar for real work?
sys.stderr = sys.stdout ## eliminar?

R_MAX_time = 4 * 3600 ## 4 hours is max duration allowd for any process

## For redirections, from Python Cookbook

def getQualifiedURL(uri = None):
    """ Return a full URL starting with schema, servername and port.
    
    *uri* -- append this server-rooted uri (must start with a slash)
    """
    schema, stdport = ('http', '80')
    host = os.environ.get('HTTP_HOST')
    if not host:
        host = os.environ.get('SERVER_NAME')
        port = os.environ.get('SERVER_PORT', '80')
        if port != stdport: host = host + ":" + port
        
    result = "%s://%s" % (schema, host)
    if uri: result = result + uri
    
    return result

def getScriptname():
    """ Return te scriptname part of the URL."""
    return os.environ.get('SCRIPT_NAME', '')


# def getPathinfo():
#     """ Return the remaining part of the URL. """
#     pathinfo = os.environ.get('PATH_INFO', '')
#     return pathinfo

def getBaseURL():
    """ Return a fully qualified URL to this script. """
    return getQualifiedURL(getScriptname())


def commonOutput():
    print "Content-type: text/html\n\n"
    print """
    <html>
    <head>
    <title>GeneSrF results</title>
    </head>
    <body>
    """
    
## to keep executing myself:
def relaunchCGI():
    print "Content-type: text/html\n\n"
    print """
    <html>
    <head>
    """
    print '<meta http-equiv="Refresh"'
    print 'content="30; URL=' + getBaseURL() + '?newDir=' + newDir + '">'
    print '<title>GeneSrF results</title>'
    print '</head> <body>'
    print '<p> This is an autorefreshing page; your results will eventually be displayed here.\n'
    print 'If your browser does not autorefresh, the results will be kept for five days at</p>'
    print '<p><a href="' + getBaseURL() + '?newDir=' + newDir + '">', 'http://genesrf.bioinfo.cnio.es/tmp/'+ newDir + '/results.html</a>.' 
    print '</p> </body> </html>'
    

## Output-generating functions
def printErrorRun():
    Rresults = open(tmpDir + "/results.txt")
    resultsFile = Rresults.read()
    outf = open(tmpDir + "/pre-results.html", mode = "w")
    outf.write("<html><head><title>GeneSrF results </title></head><body>\n")
    outf.write("<h1> ERROR: There was a problem with the R code </h1> \n")
    outf.write("<p>  This could be a bug on our code, or a problem  ")
    outf.write("with your data (that we hadn't tought of). Below is all the output from the execution ")
    outf.write("of the run. Unless it is obvious to you that this is a fault of your data ")
    outf.write("(and that there is no way we could have avoided the crash) ")
    outf.write("please let us know so we can fix the problem. ")
    outf.write("Please sed us this URL and the output below</p>")
    ## xx: eliminar, for production, from here to xxx
###     outf.write("<p> This is the output from the R run:<p>")
###     outf.write("<pre>")
###     outf.write(cgi.escape(soFar))
###     outf.write("</pre>")
    ## xxx
    outf.write("<p> This is the results file:<p>")
    outf.write("<pre>")
    outf.write(cgi.escape(resultsFile))
    outf.write("</pre>")
    outf.write("</body></html>")
    outf.close()
    Rresults.close()
    shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")


def printOKRun():
    Rresults = open(tmpDir + "/results.txt")
    resultsFile = Rresults.read()
    outf = open(tmpDir + "/pre-results.html", mode = "w")
    outf.write("<html><head><title>GeneSrF results </title></head><body>\n")

    listPNGS = glob.glob(tmpDir + "/fboot*.png")
    listPNGS.sort()
    nf1 = len(listPNGS)
    outf.write('<h2>OOB error vs. num of genes <a href="http://genesrf.bioinfo.cnio.es/help/genesrf-help.html#f1">(help)</a></h2> \n')
    outf.write('<IMG WIDTH="500" HEIGHT="417" BORDER="0" SRC="' +
                   listPNGS[nf1 - 1].replace(tmpDir + '/', '') + '">') 
    if nf1 > 1:
        outf.write('<br /><br /><h2>OOB predictions <a href="http://genesrf.bioinfo.cnio.es/help/genesrf-help.html#f2">(help)</a></h2> \n')
        for index in range(nf1 - 1):
            tmpfile = listPNGS[index].replace(tmpDir + '/','')
            outf.write('<IMG WIDTH="500" HEIGHT="417" BORDER="0" SRC="' +
                       tmpfile + '">') 

    if os.path.exists(tmpDir + "/fimpspec-all.png"):
        outf.write('<br /><br /><h2> Importance spectrum plots <a href="http://genesrf.bioinfo.cnio.es/help/genesrf-help.html#f3">(help)</a></h2> \n')
        outf.write('<IMG WIDTH="500" HEIGHT="417" BORDER="0" SRC="fimpspec-all.png">')
    if os.path.exists(tmpDir + "/fimpspec-200.png"):
        outf.write('<IMG WIDTH="500" HEIGHT="417" BORDER="0" SRC="fimpspec-200.png">')
    if os.path.exists(tmpDir + "/fimpspec-30.png"):
        outf.write('<IMG WIDTH="500" HEIGHT="417" BORDER="0" SRC="fimpspec-30.png">')

    if os.path.exists(tmpDir + "/fselprobplot.png"):
        outf.write('<br /><br /><h2> Selection probability plot <a href="http://genesrf.bioinfo.cnio.es/help/genesrf-help.html#f4">(help)</a></h2> \n')
        outf.write('<IMG WIDTH="500" HEIGHT="417" BORDER="0" SRC="fselprobplot.png">')
    
    outf.write("<br /><br /> <hr>")
    outf.write("<pre>")
    outf.write('<br /><br /><h2> Results <a href="http://genesrf.bioinfo.cnio.es/help/genesrf-help.html#resultstext">(help)</a></h2> \n')
    outf.write(cgi.escape(resultsFile))
    outf.write("</pre>")


    ## compress all the results
    allResults = tarfile.open(tmpDir + '/all.results.tar.gz', 'w:gz')
    allResults.add(tmpDir + '/results.txt', 'results.txt')
    
    if os.path.exists(tmpDir + "/fselprobplot.png"): allResults.add(tmpDir + '/fselprobplot.png', 'SelectionProbabilityPlot.png')
    if os.path.exists(tmpDir + "/fimpspec-all.png"): allResults.add(tmpDir + '/fimpspec-all.png', 'ImportanceSpectrumAllGenes.png')
    if os.path.exists(tmpDir + "/fimpspec-200.png"): allResults.add(tmpDir + '/fimpspec-200.png', 'ImportanceSpectrum200Genes.png')
    if os.path.exists(tmpDir + "/fimpspec-30.png"): allResults.add(tmpDir + '/fimpspec-30.png', 'ImportanceSpectrum30Genes.png')
    allResults.add(listPNGS[nf1 - 1], 'OOBErrorvsNumGenes.png')
    if nf1 > 1:
        for index in range(nf1 - 1):
            allResults.add(listPNGS[index], 'OOBPredictionsFigure' + str(index + 1) + '.png')
    ## Now, the pdfs
    listPDFS = glob.glob(tmpDir + "/fboot*.pdf")
    if len(listPDFS):
        listPDFS.sort()
        allResults.add(tmpDir + '/fselprobplot.pdf', 'SelectionProbabilityPlot.pdf') 
        allResults.add(tmpDir + '/fimpspec-all.pdf', 'ImportanceSpectrumAllGenes.pdf')
        allResults.add(tmpDir + '/fimpspec-200.pdf', 'ImportanceSpectrum200Genes.pdf')
        allResults.add(tmpDir + '/fimpspec-30.pdf', 'ImportanceSpectrum30Genes.pdf')
        allResults.add(listPDFS[nf1 - 1], 'OOBErrorvsNumGenes.pdf')
        if nf1 > 1:
            for index in range(nf1 - 1):
                allResults.add(listPDFS[index], 'OOBPredictionsFigure' + str(index + 1) + '.pdf')

    allResults.close()
    outf.write('<hr> <a href="http://genesrf.bioinfo.cnio.es/tmp/' +
               newDir + '/all.results.tar.gz">Download</a> all figures and text results.')  
    outf.write("</body></html>")
    outf.close()
    Rresults.close()
    shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")


def printRKilled():
    Rresults = open(tmpDir + "/results.txt")
    resultsFile = Rresults.read()
    outf = open(tmpDir + "/pre-results.html", mode = "w")
    outf.write("<html><head><title>GeneSrF results </title></head><body>\n")
    outf.write("<h1> ERROR: R process killed </h1> \n")
    outf.write("<p>  The R process lasted longer than the maximum  allowed time, ")
    outf.write(str(R_MAX_time))
    outf.write(" seconds,  and was killed.")
###     outf.write("<p> This is the output from the R run:<p>")
###     outf.write("<pre>")
###     outf.write(cgi.escape(soFar))
###     outf.write("</pre>")
    outf.write("<p> This is the results file:<p>")
    outf.write("<pre>")
    outf.write(cgi.escape(resultsFile))
    outf.write("</pre>")
    outf.write("</body></html>")
    outf.close()
    Rresults.close()
    shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")


    
## Changing to the appropriate directory
    
form = cgi.FieldStorage()
if form.has_key('newDir'):
   value=form['newDir']
   if type(value) is types.ListType:
       commonOutput()
       print "<h1> ERROR </h1>"    
       print "<p> newDir should not be a list. </p>"
       print "<p> Anyone trying to mess with it?</p>"
       print "</body></html>"
       sys.exit()
   else:
       newDir = value.value
else:
    commonOutput()
    print "<h1> ERROR </h1>"    
    print "<p> newDir is empty. </p>"
    print "</body></html>"
    sys.exit()

if re.search(r'[^0-9]', str(newDir)):
## newDir can ONLY contain digits.
    commonOutput()
    print "<h1> ERROR </h1>"    
    print "<p> newDir does not have a valid format. </p>"
    print "<p> Anyone trying to mess with it?</p>"
    print "</body></html>"
    sys.exit()
    
redirectLoc = "/tmp/" + newDir
tmpDir = "/http/genesrf/www/tmp/" + newDir

if not os.path.isdir(tmpDir):
    commonOutput()
    print "<h1> ERROR </h1>"    
    print "<p> newDir is not a valid directory. </p>"
    print "<p> Anyone trying to mess with it?</p>"
    print "</body></html>"
    sys.exit()
    

## Were we already done in a previous execution?
## No need to reopen files or check anything else. Return url with results
## and bail out.
if os.path.exists(tmpDir + "/natural.death.pid.txt") or os.path.exists(tmpDir + "/killed.pid.txt"):
    print 'Location: http://genesrf.bioinfo.cnio.es/tmp/'+ newDir + '/results.html \n\n'
    sys.exit()

## No, we were not done. Need to examine R output
Rrout = open(tmpDir + "/f1.Rout")
soFar = Rrout.read()
Rrout.close()
finishedOK = soFar.endswith("Normal termination\n")
errorRun = soFar.endswith("Execution halted\n")

if os.path.exists(tmpDir + "/pid.txt"):
    ## do we need to kill an R process?
    if (time.time() - os.path.getmtime(tmpDir + "/pid.txt")) > R_MAX_time:
        try:
            os.kill(int(open(tmpDir + "/pid.txt", mode = "r").readline()),
                	     signal.SIGKILL)
        finally:  
            printRKilled()
            os.rename(tmpDir + '/pid.txt', tmpDir + '/killed.pid.txt')
            os.remove(tmpDir + '/f1.R')
            try:
                os.remove("/http/genesrf/www/R.running.procs/R." + newDir)
            finally:
                print 'Location: http://genesrf.bioinfo.cnio.es/tmp/'+ newDir + '/results.html \n\n'
                chkmpi = os.system('/http/mpi.log/adhocCheckRmpi.py GeneSrF&')
                sys.exit()

if errorRun > 0:
    printErrorRun()
    os.rename(tmpDir + '/pid.txt', tmpDir + '/natural.death.pid.txt')
    os.remove(tmpDir + '/f1.R')
    chkmpi = os.system('/http/mpi.log/adhocCheckRmpi.py GeneSrF&')
    try:
        os.remove("/http/genesrf/www/R.running.procs/R." + newDir)
    finally:
        print 'Location: http://genesrf.bioinfo.cnio.es/tmp/'+ newDir + '/results.html \n\n'


elif finishedOK > 0:
    printOKRun()
    os.rename(tmpDir + '/pid.txt', tmpDir + '/natural.death.pid.txt')
    os.remove(tmpDir + '/f1.R')
    chkmpi = os.system('/http/mpi.log/adhocCheckRmpi.py GeneSrF&')
    try:
        os.remove("/http/genesrf/www/R.running.procs/R." + newDir)
    finally:
        print 'Location: http://genesrf.bioinfo.cnio.es/tmp/'+ newDir + '/results.html \n\n'

    
else:
    ## we only end up here if: we were not done in a previous run AND no process was overtime 
    ## AND we did not just finish. So we must continue.
    relaunchCGI()
    



## If anything above fails, code below gives some potentially helpful output
# commonOutput()
# print "<p> getQualifiedURL ",getQualifiedURL(), "<p>"
# print "<p> getScriptname ",getScriptname(), "<p>"
# print "<p> getBaseURL ",getBaseURL(), "<p>"
# print "<p> getPathInfo ",getPathinfo(), "<p>"
# print "</body></html>"

# # # getQualifiedURL http://genesrf.bioinfo.cnio.es
# # # getScriptname /cgi-bin/checkdone.cgi
# # # getBaseURL http://genesrf.bioinfo.cnio.es/cgi-bin/checkdone.cgi
# # # getPathInfo Traceback (most recent call last): File "/http/genesrf/cgi/checkdone.cgi", line 120, in ? print "
