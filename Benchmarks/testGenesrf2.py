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



def common_part(self, final_output,                
                MAX_running_time = 3600,
                auto_refresh_string = auto_refresh_string):    
    server_url = self.server_url
    start_run = time.time()
    refresh_num = 0
    
    while True:
        final_body = self.getBody()
        if final_body.find(auto_refresh_string) < 0:
            break
        time.sleep(32)
        refresh_num += 1
        run_time = time.time() - start_run
        print '\n Refreshed ' + str(refresh_num) + ' times. Been running for ' + str(round(run_time/60.0, 2)) + ' minutes.\n'
        if run_time > MAX_running_time :
            self.fail('Run longer than MAX_running_time')
        self.get(server_url + self.getLastUrl(),
                 description="Get /cgi-bin/checkdone.cgi")
    expected = final_body.find(final_output) >= 0
    if not expected:
        self.fail('\n ***** (begin of) Unexpected final result!!!! *****\n' + \
                 str(final_body) + \
                 '\n ***** (end of) Unexpected final result!!!! *****\n')
    else:
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

    def test1(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/genesrfR.cgi", params=[
            ['covariate', Upload("xdata2.txt")],
            ['class', Upload("Class")],
            ['organism', 'None'],
            ['idtype', 'None']],
            description="simple test")

        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)



    def test2(self):
        server_url = self.server_url

        self.get(server_url + "/",
            description="Get /")

        self.post(server_url + "/cgi-bin/genesrfR.cgi", params=[
            ['covariate', Upload("./with.mm.names/short.covar2.txt")],
            ['class', Upload("./with.mm.names/class")],
            ['organism', 'Mm'],
            ['idtype', 'ug']],
            description="test with organism and idtype and pals")

        final_output = '<h3>Variable selection using all data </h3><h4>Variables used</h4>'
        common_part(self, final_output)



    def tearDown(self):
        """Setting up test."""
        self.logd("tearDown.\n")

if __name__ in ('main', '__main__'):
     unittest.main()
