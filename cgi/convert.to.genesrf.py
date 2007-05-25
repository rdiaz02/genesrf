#!/usr/bin/python

## when ready, turn adacgh2 into adacgh
## or viceversa


import sys
import os

direction = sys.argv[1]

if direction=='genesrf2':
    os.system("sed 's/genesrf.bioinfo/genesrf2.bioinfo/g' checkdone.cgi > tmp; mv tmp checkdone.cgi")
    os.system("sed 's/genesrf.bioinfo/genesrf2.bioinfo/g' genesrfR.cgi > tmp; mv tmp genesrfR.cgi")
    os.system("sed 's/genesrf.bioinfo/genesrf2.bioinfo/g' ../www/genesrf.html > tmp; mv tmp ../www/genesrf.html")
    os.system("sed 's/genesrf.bioinfo/genesrf2.bioinfo/g' results-pre.html > tmp; mv tmp results-pre.html")
    os.system("sed 's/genesrf.bioinfo/genesrf2.bioinfo/g' results-pre-ace.html > tmp; mv tmp results-pre-ace.html")    
    os.system("sed 's/\/http\/genesrf\//\/http\/genesrf2\//g' checkdone.cgi > tmp; mv tmp checkdone.cgi")
    os.system("sed 's/\/http\/genesrf\//\/http\/genesrf2\//g' genesrfR.cgi > tmp; mv tmp genesrfR.cgi")
    os.system("sed 's/\/http\/genesrf\//\/http\/genesrf2\//g' ../www/genesrf.html > tmp; mv tmp ../www/genesrf.html")
    os.system("sed 's/\/http\/genesrf\//\/http\/genesrf2\//g' results-pre.html > tmp; mv tmp results-pre.html")
    
    
if direction=='genesrf':
    os.system("sed 's/genesrf2.bioinfo/genesrf.bioinfo/g' checkdone.cgi > tmp; mv tmp checkdone.cgi")
    os.system("sed 's/genesrf2.bioinfo/genesrf.bioinfo/g' genesrfR.cgi > tmp; mv tmp genesrfR.cgi")
    os.system("sed 's/genesrf2.bioinfo/genesrf.bioinfo/g' ../www/genesrf.html > tmp; mv tmp ../www/genesrf.html")
    os.system("sed 's/genesrf2.bioinfo/genesrf.bioinfo/g' results-pre.html > tmp; mv tmp results-pre.html")
    os.system("sed 's/genesrf2.bioinfo/genesrf.bioinfo/g' results-pre-ace.html > tmp; mv tmp results-pre-ace.html")    
    os.system("sed 's/\/http\/genesrf2\//\/http\/genesrf\//g' checkdone.cgi > tmp; mv tmp checkdone.cgi")
    os.system("sed 's/\/http\/genesrf2\//\/http\/genesrf\//g' genesrfR.cgi > tmp; mv tmp genesrfR.cgi")
    os.system("sed 's/\/http\/genesrf2\//\/http\/genesrf\//g' ../www/genesrf.html > tmp; mv tmp ../www/genesrf.html")
    os.system("sed 's/\/http\/genesrf2\//\/http\/genesrf\//g' results-pre.html > tmp; mv tmp results-pre.html")

os.system('chmod u+x /http/genesrf2/cgi/*.cgi')    
os.system('chown -R www-data /http/genesrf2')
