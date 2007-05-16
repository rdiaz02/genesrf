# -*- coding: iso-8859-15 -*-
"""basic_navigation FunkLoad test

$Id: $
"""
import time
import unittest
from funkload.FunkLoadTestCase import FunkLoadTestCase
from webunit.utility import Upload


auto_refresh_string = 'This is an autorefreshing page'
MAX_running_time = 3600 * 1 

def common_part_bench(self,                 
                      auto_refresh_string = auto_refresh_string):    
    """ like above, but does not check anything. simply benchmarking"""
    server_url = self.server_url
    
    while True:
        time.sleep(10)
        final_body = self.getBody()
        if final_body.find(auto_refresh_string) < 0:
            break
        time.sleep(10)
        self.get(server_url + self.getLastUrl(),
                 description="checking if done")
    print 'OK'


    
class GeneSrF(FunkLoadTestCase):
    """XXX

    This test use a configuration file Genesrf.conf.
    """

    def setUp(self):
        """Setting up test."""
        self.logd("setUp")
        self.server_url = 'http://genesrf2.bioinfo.cnio.es'
        ##self.server_url = self.conf_get('main', 'url')

    def test1(self, dataset):
        server_url = self.server_url
        self.get(server_url + "/",
            description="Get /")
        start_time = time.time()
        self.post(server_url + "/cgi-bin/genesrfR.cgi", params=[
            ['covariate', Upload("./data.sets/" + dataset + ".data.txt")],
            ['class', Upload("./data.sets/" + dataset + ".class.txt")],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="simple test")
        common_part_bench(self)
        end_time = time.time()
        duration = end_time - start_time
        print duration

    def test_colon(self): self.test1('colon')
    def test_srbct(self): self.test1('srbct')
    def test_nci(self): self.test1('nci')
    def test_prostate(self): self.test1('prostate')
    def test_breast3(self): self.test1('breast.3.class')
    def test_breast2(self): self.test1('breast.2.class')
    def test_lymphoma(self): self.test1('lymphoma')
    def test_brain(self): self.test1('brain')
    def test_adeno(self): self.test1('adenocarcinoma')

    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
