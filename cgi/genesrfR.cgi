#!/usr/bin/python
import glob
import socket
import sys
import os
import cgi 
##import types
import time
import shutil
import dircache
##import string
import random
from stat import ST_SIZE
import cgitb
cgitb.enable() ## zz: eliminar for real work?
sys.stderr = sys.stdout

MAX_genesrf = 15 ## MAX_genesrf + 1 = Maximum number of R processes running at same time.
MAX_time = 3600 * 24 * 5 ## 5 is days until deletion of a tmp directory
R_MAX_time = 3600 * 24 ## 4 hours is max duration allowd for any process
MAX_covariate_size = 363948523L ## a 500 * 40000 array of floats
MAX_class_size = 61897L
##  f5 <- rep(paste(paste(letters, collapse = ""),
##                  paste(LETTERS, collapse="")), 1000)
## so each of 1000 labels has 48 chars.


acceptedIDTypes = ('None', 'cnio', 'affy', 'clone', 'acc', 'ensembl', 'entrez', 'ug', 'rsrna', 'rspeptide', 'hugo')
acceptedOrganisms = ('None', 'Hs', 'Mm', 'Rn')


def commonOutput():
    print "Content-type: text/html\n\n"
    print """
    <html>
    <head>
    <title>GeneSrF</title>
    </head>
    <body>
    """


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




def fileUpload(fieldName):
    """Upload and get the files and do some checking. We assume there is an existing call
    to fs = cgi.FieldStorage()"""
## we don't deal with OS specific "\n"
## because R does not have a problem (at least with Windows files)
## no problem in R either with empty carriage returns at end of file
    
    if fs.has_key(fieldName):
        fileClient = fs[fieldName].file
        if not fileClient:
            shutil.rmtree(tmpDir)
            commonOutput()
            print "<h1> GENESRF ERROR </h1>"    
            print "<p> The ", fieldName, "file you entered is not a file </p>"
            print "<p> Please fill up the required fields and try again</p>"
            print "</body></html>"
            sys.exit()
    else:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GENESRF ERROR </h1>"    
        print "<p> ", fieldName, "file required </p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
            
    # transferring files to final destination;

    fileInServer = tmpDir + "/" + fieldName
    srvfile = open(fileInServer, mode = 'w')
    fileString = fs[fieldName].value
    srvfile.write(fileString)
    srvfile.close()

    ## this is slower than reading all to memory and copying from
    ## there, but this is less taxing on memory.
    ## but with the current files, probably not worth it
    #     while 1:
    #         line = fileClient.readline()
    #         if not line: break
    #         srvfile.write(line)
    #     srvfile.close()
    
    os.chmod(fileInServer, 0666)
        
    if os.path.getsize(fileInServer) == 0:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GENESRF ERROR </h1>"
        print "<p>", fieldName, " file has size 0 </p>"
        print "<p> Please enter a file with something in it.</p>"
        print "</body></html>"
        sys.exit()



def radioUpload(fieldName, acceptedValues):
    """Upload and get the values and do some checking. For radio selections
    with text data; check those are in acceptedValues.
    We assume there is an existing call to fs = cgi.FieldStorage()"""

    if not fs.has_key(fieldName):
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GeneSrF ERROR </h1>"    
        print "<p>", fieldName, "required </p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
    if fs[fieldName].filename:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GeneSrF ERROR </h1>"    
        print "<p> ", fieldName, "should not be a file. </p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
    if type(fs[fieldName]) == type([]):
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GeneSrF ERROR </h1>"    
        print "<p>", fieldName, "should be a single value.</p>"
        print "<p> Please fill up the required fields and try again</p>"
        print "</body></html>"
        sys.exit()
    else:
        tmp = fs[fieldName].value
            
    if tmp not in acceptedValues:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GeneSrF ERROR </h1>"    
        print "<p> The", fieldName, "choosen is not valid.</p>"
        print "<p> Please fill up the required fields and try again.</p>"
        print "</body></html>"
        sys.exit()

    fileInServer = tmpDir + "/" + fieldName
    srvfile = open(fileInServer, mode = 'w')
    fileString = tmp
    srvfile.write(fileString)
    srvfile.close()
    os.chmod(fileInServer, 0666)

    return tmp


#def makePalsurl(tmp_dir):
#	f=open("idtype")
#	idtype = f.read().strip()
#	f.close()
#	f=open("organism")
#	organism = f.read().strip()
#	f.close()
#	if (idtype != "None" and organism != "None"):
#		url_org_id = "org=" + organism + "&idtype=" + idtype + "&"
#	else:
#		url_org_id = ""
#	gene_list_file = "http://pomelo2.bioinfo.cnio.es/tmp/" + tmp_dir + "/gene.list.txt"
#	data_file = "datafile=" + gene_list_file
#	Pals_main_url = "http://pals.bioinfo.cnio.es?" + url_org_id + data_file
#	return(Pals_main_url)

#########################################################
#########################################################

####          Execution starts here      ################

#########################################################
#########################################################

## Deleting tmp directories older than MAX_time
currentTime = time.time()
currentTmp = dircache.listdir("/http/genesrf2/www/tmp")
for directory in currentTmp:
    tmpS = "/http/genesrf2/www/tmp/" + directory
    if (currentTime - os.path.getmtime(tmpS)) > MAX_time:
        shutil.rmtree(tmpS)


### Creating temporal directories
newDir = str(random.randint(1, 10000)) + str(os.getpid()) + str(random.randint(1, 100000)) + str(int(currentTime)) + str(random.randint(1, 10000))
redirectLoc = "/tmp/" + newDir
tmpDir = "/http/genesrf2/www/tmp/" + newDir
os.mkdir(tmpDir)
os.chmod(tmpDir, 0700)

### Uploading files and checking not abusively large
fs = cgi.FieldStorage()


idtype = radioUpload('idtype', acceptedIDTypes)
organism = radioUpload('organism', acceptedOrganisms)

##check if file coming from preP

if(fs.getfirst("covariate2")!= None):
    prep_tmpdir = fs.getfirst("covariate2")
    ## an ugly hack, as prep not in this filesystem
    os.system('wget http://prep.bioinfo.cnio.es/tmp/' + prep_tmpdir +
              '/outdata.txt -O ' + tmpDir + '/covariate')
    ## shutil.copy("/http/prep/www/tmp/" + prep_tmpdir +"/outdata.txt",tmpDir + "/covariate")
else:
    fileUpload('covariate')
    if os.stat(tmpDir + '/covariate')[ST_SIZE] > MAX_covariate_size:
        shutil.rmtree(tmpDir)
        commonOutput()
        print "<h1> GENESRF ERROR </h1>"
        print "<p> Covariate file way too large </p>"
        print "<p> Covariate files this size not allowed.</p>"
        print "</body></html>"
        sys.exit()

fileUpload('class')
if os.stat(tmpDir + '/class')[ST_SIZE] > MAX_class_size:
    shutil.rmtree(tmpDir)
    commonOutput()
    print "<h1> GENESRF ERROR </h1>"
    print "<p> Class file way too large </p>"
    print "<p> Class files this size not allowed.</p>"
    print "</body></html>"
    sys.exit()

## Upload worked OK. We store the original names of the files in the
## browser for later report:
fileNamesBrowser = open(tmpDir + '/fileNamesBrowser', mode = 'w')
if(fs.getfirst("covariate2")== None):
    fileNamesBrowser.write(fs['covariate'].filename + '\n')
fileNamesBrowser.write(fs['class'].filename + '\n')
fileNamesBrowser.close()




## current number of processes > max number of processes?
## and yes, we do it here, not before, so that we have the most
## current info about number of process right before we launch R.

##

## Now, delete any R file left (e.g., from killing procs, etc).
RrunningFiles = dircache.listdir("/http/genesrf2/www/R.running.procs")
for Rtouchfile in RrunningFiles:
    tmpS = "/http/genesrf2/www/R.running.procs/" + Rtouchfile
    if (currentTime - os.path.getmtime(tmpS)) > R_MAX_time:
        os.remove(tmpS)

## Now, verify any processes left
numRgenesrf = len(glob.glob("/http/genesrf2/www/R.running.procs/R.*@*%*"))
if numRgenesrf > MAX_genesrf:
    shutil.rmtree(tmpDir)
    commonOutput()
    print "<h1> GeneSrF problem: The servers are too busy </h1>"
    print "<p> Because of the popularity of the application "
    print " the maximum number of simultaneous runs of genesrf has been reached.</p>"
    print "<p> Please try again later.</p>"
    print "<p> We apologize for the inconvenience.</p>"    
    print "</body></html>"
    sys.exit()
    

################        Launching R   ###############

# prepare the arrayNames file:

covarInServer = tmpDir + "/covariate"
arrayNames = tmpDir + "/arrayNames"
srvfile = open(covarInServer, mode = 'rU')
arrayfile = open(arrayNames, mode = 'w')
num_name_lines = 0
while 1:
    line = srvfile.readline()
    if not line: break
    if (line.find("#name") == 0) or (line.find("#NAME") == 0) or (line.find("#Name") == 0) \
           or (line.find('"#name"') == 0) or (line.find('"#NAME"') == 0) or (line.find('"#Name"') == 0):
        num_name_lines = num_name_lines + 1
        if num_name_lines > 1:
            commonOutput()
            print """ You have more than one line with #Name (or #NAME or #name), in the data matrix \
                   but only one is allowed."""
            sys.exit()
        arrayfile.write(line)
        arrayfile.write("\n\n")
        
    
srvfile.close()
arrayfile.close()   
os.chmod(arrayNames, 0600)


## It would be good to use spawnl or similar instead of system,
## but I have no luck with R. This, I keep using system.
## Its safety depends crucially on the newDir not being altered,
## but newDir is not passed from any other user-reachable place
## (it is created here).


## recall to include in R
    ##pid <- Sys.getpid()
    ##write.table(file = "pid.txt", pid, row.names = FALSE, col.names = FALSE)

## touch Rout, o.w. checkdone can try to open a non-existing file
touchRout = os.system("/bin/touch " + tmpDir + "/f1.Rout") 
##touchRrunning = os.system("/bin/touch /http/genesrf2/www/R.running.procs/R." + newDir)
touchRrunning = os.system("/bin/touch /http/genesrf2/www/R.running.procs/R." + newDir +
                          "@" + socket.gethostname())
shutil.copy("/http/genesrf2/cgi/f1.R", tmpDir)
## we add the 2> error.msg because o.w. if we kill R we get a server error as standard
## error is sent to the server
# Rcommand = "cd " + tmpDir + "; " + "/var/www/bin/R-local-7-LAM-MPI/bin/R CMD BATCH --no-restore --no-readline --no-save -q f1.R 2> error.msg &"
# Rrun = os.system(Rcommand)
tryrrun = os.system('/http/mpi.log/tryRrun2.py ' + tmpDir +' 10 ' + 'GeneSrF &')
createResultsFile = os.system("/bin/touch " + tmpDir + "/results.txt")



###########   Creating a results.hmtl   ###############

## Copy to tmpDir a results.html that redirects to checkdone.cgi
## If communication gets broken, there is always a results.html
## that will do the right thing.
shutil.copy("/http/genesrf2/cgi/results-pre.html", tmpDir)
os.system("/bin/sed 's/sustituyeme/" + newDir + "/g' " +
          tmpDir + "/results-pre.html > " +
          tmpDir + "/results.html; rm " +
          tmpDir +"/results-pre.html")

# os.system("cd " + tmpDir + "; /bin/sed 's/sustituyeme/" +
#           newDir + "/g' results-pre.html > results.html; rm results-pre.html")

##############    Redirect to checkdone.cgi    ##################
print "Location: "+ getQualifiedURL("/cgi-bin/checkdone.cgi") + "?newDir=" + newDir, "\n\n"


