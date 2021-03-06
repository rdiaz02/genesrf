#!/usr/bin/python


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
cgitb.enable() ## zz: eliminar for real work?
sys.stderr = sys.stdout ## eliminar?

## For redirections, from Python Cookbook
sys.path.append("/asterias-web-apps/web-apps-common")
from web_apps_config import *


# def extract_for_PaLS_from_geneSrF(file_in1 = '/results.html',
#                                   file_in2 = '/model.freqs.table.html',
#                                   file_out = '/Selected.genes.txt',
#                                   file_out1 ='/Selected.and.bootstrap.selected.txt'):
#     string1_all_data = '<h3>Variable selection using all data </h3><h4>Variables used</h4><TABLE frame="box">\n'
#     string_r_remove_all_data = '</a> </td></tr>'
#     string_l_remove_all_data =  'target="icl_window" >'
#     string_end_all = '</TABLE><p> Number of variables used:'
#     f1 = open(file_in1, mode = 'r').readlines()
#     f2 = open(file_out, mode = 'w')
#     f3 = open(file_out1, mode = 'w')

#     # A check
#     if f1[9] != string1_all_data:
#         raise SystemError

#     def find_num_used(x):
#         for i in range(9, len(f1)):
#             tmpl = f1[i]
#             if tmpl.startswith(string_end_all):
#                 nvars = tmpl.split()[5]
#                 return int(nvars)
#                 break

#     nvars = find_num_used(f1)
#     lines_vars = range(11, 11 + nvars)

#     f2.write("#AllData\n")
#     f3.write("#AllData\n")

#     for ll in lines_vars:
#         tmp = f1[ll]
#         posl = tmp.rfind(string_l_remove_all_data) + 21
#         posr = tmp.rfind(string_r_remove_all_data)
#         f2.write(tmp[posl:posr] +  '\n')
#         f3.write(tmp[posl:posr] +  '\n')

#     f2.flush()
#     f2.close()

#     f1b = open(file_in2, mode = 'r').readlines()
#     f1b = f1b[2:-1]
#     cvnum = 1

#     for ll in f1b:
#         f3.write("#CV.run." + str(cvnum) + "\n")
#         outst = ll.replace('+', ' ').replace('<tr><td>', ' ').\
#                 replace('</td><td><div align=right>',' ').\
#                 replace('</div></td></tr>',' ').split()[:-1]
#         for outg in outst:
#             f3.write(outg + '\n')
#         cvnum += 1

#     f3.flush()
#     f3.close()


# def clean_for_PaLS(file_in, file_out):
#     """ Make sure no file has two consecutive lines that start with '#',
#     so there are not lists without genes."""
#     f1 = open(file_in, mode = 'r').readlines()
#     f2 = open(file_out, mode = 'w')
#     maxi = len(f1) - 1
#     i = 0
#     if len(f1) == 0:
#         f2.close()
#     else:
#         tmp1 = f1[i]
#         tmp2 = ' '
#         while True:
#             if i == maxi:
#                 break
#             tmp2 = f1[i + 1]
#             if not tmp1.startswith('#'):
#                 f2.write(tmp1)
#             elif not tmp2.startswith('#'):
#                 f2.write(tmp1)
#             tmp1 = tmp2
#             i += 1
#     ### make sure last one is written if not a "#"
#         if not tmp2.startswith('#'):
#             f2.write(tmp2)
#         f2.close()


# def printPalsURL(newDir,
#                  tmpDir,
#                  application_url = "http://genesrf.iib.uam.es",
#                  f1 = "Selected.genes.txt",
#                  f2 = "Selected.and.bootstrap.selected.txt",
#                  s1 = "genes selected in main run (this rarely makes any sense!)",
#                  s2 = "genes selected in main run and in bootstrap runs"):
#     """ Based on Pomelo II's Send_to_Pals.cgi."""
#     f=open(tmpDir + "/idtype")
#     idtype = f.read().strip()
#     f.close()
#     f=open(tmpDir + "/organism")
#     organism = f.read().strip()
#     f.close()
#     if (idtype != "None" and organism != "None"):
#         url_org_id = "org=" + organism + "&idtype=" + idtype + "&"
#     else:
#         url_org_id = ""
#     gl_base = application_url + '/tmp/' + newDir + '/'
#     gl1 = gl_base + f1
#     gl2 = gl_base + f2

#     ## Fixme: I am taking this out of here,
#     ## because I need to read the veryu results.html file
#     ## and varSelRF always gives at least two genes.
#     ## clean_for_PaLS(tmpDir + '/' + f1, tmpDir + '/' + f1)
#     ## clean_for_PaLS(tmpDir + '/' + f2, tmpDir + '/' + f2)
    
#     outstr0 = '<br /> <hr> ' + \
#               '<h3> Send results to <a href = "http://pals.iib.uam.es">' + \
#               '<IMG BORDER="0" SRC="../../palsfavicon40.png" align="middle"></a></h3>'
#     outstr = outstr0 + \
#              '<p> Send set of <a href="http://pals.iib.uam.es?' + \
#              url_org_id + 'datafile=' + gl1 + \
#              '">' + s1 + ' to PaLS</a></p>' + \
#              '<p> Send set of <a href="http://pals.iib.uam.es?' + \
#              url_org_id + 'datafile=' + gl2 + \
#              '">' + s2 + ' to PaLS</a></p>' 
#     return(outstr)




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
    print 'content="10; URL=' + getBaseURL() + '?newDir=' + newDir + '">'
    print '<title>GeneSrF results</title>'
    print '</head> <body>'
    print '<p> This is an autorefreshing page; your results will eventually be displayed here.\n'
    print 'If your browser does not autorefresh, the results will be kept for five days at</p>'
    print '<p><a href="' + getBaseURL() + '?newDir=' + newDir + '">', 'http://genesrf.iib.uam.es/tmp/'+ newDir + '/results.html</a>.' 
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
    outf.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">')
    outf.write('\n<html><head>')
    outf.write('\n <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-15">')
##    outf.write('\n <SCRIPT type="text/javascript" SRC="../../aqtree3clickable.js"></SCRIPT> ')
##    outf.write('\n <LINK REL="stylesheet" HREF="../../aqtree3clickable.css"> ')
    outf.write('\n <LINK REL="stylesheet" HREF="../../style1.css"> ')

    outf.write("<html><head><title>GeneSrF results </title></head><body>\n")

    if os.path.exists(tmpDir + "/ErrorFigure.png"):
        outf.write('<IMG BORDER="0" SRC="ErrorFigure.png">')
        outf.write("<br /><br /> <hr>")
        outf.write("<pre>")
        outf.write('<br /><br /><h2> Results <a href="http://adacgh.iib.uam.es/help/adacgh-help.html#outputText">(help)</a></h2> \n')
        outf.write("<br /><br /> <hr>")
        outf.write(cgi.escape(resultsFile))
        outf.write("</pre>")
        outf.write("</body></html>")
        outf.flush()
        outf.close()
        Rresults.close()
        shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")

    else:
        listPNGS = glob.glob(tmpDir + "/fboot*.png")
        listPNGS.sort()
        nf1 = len(listPNGS)
        outf.write('<h2>OOB error vs. num of genes <a href="http://genesrf.iib.uam.es/help/genesrf-help.html#f1">(help)</a></h2> \n')
        outf.write('<IMG BORDER="0" SRC="' +
                       listPNGS[nf1 - 1].replace(tmpDir + '/', '') + '">') 
        if nf1 > 1:
            outf.write('<br /><br /><h2>OOB predictions <a href="http://genesrf.iib.uam.es/help/genesrf-help.html#f2">(help)</a></h2> \n')
            for index in range(nf1 - 1):
                tmpfile = listPNGS[index].replace(tmpDir + '/','')
                outf.write('<IMG BORDER="0" SRC="' +
                           tmpfile + '">') 

        if os.path.exists(tmpDir + "/fimpspec-all.png"):
            outf.write('<br /><br /><h2> Importance spectrum plots <a href="http://genesrf.iib.uam.es/help/genesrf-help.html#f3">(help)</a></h2> \n')
            outf.write('<IMG BORDER="0" SRC="fimpspec-all.png">')
        if os.path.exists(tmpDir + "/fimpspec-200.png"):
            outf.write('<IMG BORDER="0" SRC="fimpspec-200.png">')
        if os.path.exists(tmpDir + "/fimpspec-30.png"):
            outf.write('<IMG BORDER="0" SRC="fimpspec-30.png">')

        if os.path.exists(tmpDir + "/fselprobplot.png"):
            outf.write('<br /><br /><h2> Selection probability plot <a href="http://genesrf.iib.uam.es/help/genesrf-help.html#f4">(help)</a></h2> \n')
            outf.write('<IMG BORDER="0" SRC="fselprobplot.png">')

        outf.write("<br /><br /> <hr>")
    #    outf.write("<pre>")
        outf.write('<br /><br /><h2> Results <a href="http://genesrf.iib.uam.es/help/genesrf-help.html#resultstext">(help)</a></h2> \n')
        outf.write(resultsFile)
    #    outf.write("</pre>")
        ## compress all the results
        allResults = tarfile.open(tmpDir + '/all.results.tar.gz', 'w:gz')
        os.system('cd ' + tmpDir +'; cp results.txt rr.html; w3m -dump rr.html > results.TXT; rm rr.html')
        allResults.add(tmpDir + '/results.TXT', 'results.txt')
        
	if os.path.exists(tmpDir + "/all.RData"): allResults.add(tmpDir + '/all.RData', 'all_R_objects.RData')
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
        allResults.add(tmpDir + '/pre-results.html', 'results.html')                    
        allResults.close()
        outf.write('<hr> <a href="http://genesrf.iib.uam.es/tmp/' +
                   newDir + '/all.results.tar.gz">Download</a> all figures and text results.')  

        # outf.write(printPalsURL(newDir, tmpDir))
        outf.write("</body></html>")
        outf.flush()
        outf.close()
        Rresults.close()
        shutil.copyfile(tmpDir + "/pre-results.html", tmpDir + "/results.html")
        # try:
        #     extract_for_PaLS_from_geneSrF(file_in1 = tmpDir + '/results.html',
        #                                   file_in2 = tmpDir + '/model.freqs.table.html',
        #                                   file_out = tmpDir + '/Selected.genes.txt',
        #                                   file_out1 = tmpDir + '/Selected.and.bootstrap.selected.txt')
        # except:
        #     None

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
tmpDir = "/asterias-web-apps/genesrf/www/tmp/" + newDir

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
    print 'Location: http://genesrf.iib.uam.es/tmp/'+ newDir + '/results.html \n\n'
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
        lamenv = open(tmpDir + "/lamSuffix", mode = "r").readline()
        try:
            os.system('export LAM_MPI_SESSION_SUFFIX=' + lamenv +
                      '; lamhalt -H; lamwipe -H; touch ' +
                      tmpDir + '/lamKilledFromPython')
        except:
            None
#             os.kill(int(open(tmpDir + "/pid.txt", mode = "r").readline()),
#                 	     signal.SIGKILL)

        printRKilled()
        os.rename(tmpDir + '/pid.txt', tmpDir + '/killed.pid.txt')
##        os.remove(tmpDir + '/f1.R')
        try:
            os.system("rm /asterias-web-apps/genesrf/www/R.running.procs/R." + newDir + "*")
        except:
            None
        print 'Location: http://genesrf.iib.uam.es/tmp/'+ newDir + '/results.html \n\n'
##                chkmpi = os.system('/asterias-web-apps/mpi.log/adhocCheckRmpi.py GeneSrF&')
        sys.exit()

if errorRun > 0:
    printErrorRun()
    os.rename(tmpDir + '/pid.txt', tmpDir + '/natural.death.pid.txt')
##    os.remove(tmpDir + '/f1.R')
##    chkmpi = os.system('/asterias-web-apps/mpi.log/adhocCheckRmpi.py GeneSrF&')
    # try:
    #     lamenv = open(tmpDir + "/lamSuffix", mode = "r").readline()
    # except:
    #     None
    # try:
    #     os.system('export LAM_MPI_SESSION_SUFFIX=' + lamenv +
    #               '; lamhalt -H; lamwipe -H; touch ' +
    #               tmpDir + '/lamKilledFromPython')
    # except:
    #     None
    try:
        os.system("rm /asterias-web-apps/genesrf/www/R.running.procs/R." + newDir + "*")
    except:
        None
    print 'Location: http://genesrf.iib.uam.es/tmp/'+ newDir + '/results.html \n\n'


elif finishedOK > 0:
    ##zz: killing lam seems not to be working from here...
    # try:
    #     lamenv = open(tmpDir + "/lamSuffix", mode = "r").readline()
    # except:
    #     None
    # try:
    #     lamkill = os.system('export LAM_MPI_SESSION_SUFFIX=' + lamenv +
    #                         '; lamhalt -H; lamwipe -H; touch ' +
    #                         tmpDir + '/lamKilledFromPython')
    # except:
    #     None
    printOKRun()
    os.rename(tmpDir + '/pid.txt', tmpDir + '/natural.death.pid.txt')
#    os.remove(tmpDir + '/f1.R')
    ##    chkmpi = os.system('/asterias-web-apps/mpi.log/adhocCheckRmpi.py GeneSrF&')
    try:
        os.system("rm /asterias-web-apps/genesrf/www/R.running.procs/R." + newDir  + "*")
    except:
        None
    print 'Location: http://genesrf.iib.uam.es/tmp/'+ newDir + '/results.html \n\n'

    
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

# # # getQualifiedURL http://genesrf.iib.uam.es
# # # getScriptname /cgi-bin/checkdone.cgi
# # # getBaseURL http://genesrf.iib.uam.es/cgi-bin/checkdone.cgi
# # # getPathInfo Traceback (most recent call last): File "/asterias-web-apps/genesrf/cgi/checkdone.cgi", line 120, in ? print "
