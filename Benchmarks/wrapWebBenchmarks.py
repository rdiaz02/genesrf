#!/usr/bin/env python

import os
import sys
import time



def launchTest(test):
    iin, t = os.popen2('fl-run-test benchmarkGeneSrF.py GeneSrF.test_' + test)
    timef = float(t.readlines()[1].strip())

def writeFile(testout, name):
    fout = open(name, mode = 'w')
    for result in testout:
        fout.write(str(result))
        fout.write('\t')
    fout.flush()
    fout.close()

TESTS = (
   'colon',
   'srbct',
   'nci',
   'prostate',
   'breast3',
   'breast2',
   'lymphoma',
   'brain',
   'adeno')

REPS = 3

alltests = TESTS * REPS

os.system("cp ../www/Examples/data.sets.tar.gz .")
os.system("tar -zxvf data.sets.tar.gz")

timings =  [-99] * len(alltests)
for i in range(len(alltests)):
    try:
        timings[i] = launchTest(alltests[i])
    except:
        None
        
writeFile(timings, 'web.bnchmk.txt')

## something screwed up above. but since it was run interactively, I copy output and then
## process.

## We then do
## grep "Ran 1 test in " out.web.txt | sed 's/Ran 1 test in //' | sed 's/s//' > web.bnchmk.txt


os.system("rm data.sets.tar.gz")
os.system("rm -r -f data.sets")




##########
