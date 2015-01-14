import ConfigParser
import json
import os
import random
import yaml

from locust import HttpLocust, TaskSet, task

import task_funcs.keystone_v2_base as keystone_base

class baseTaskSet(TaskSet):
    """ baseTaskSet class
        basic task set containing primary utility methods
        that will be inherited / used by sub task sets
    
    """

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.id = str(self.locust).split('object at')[1].strip().replace('>','')

        # get data from common config
        self.read_locust_config()

        # get data from tempest config
        self.keystone_user = self.get_tempest_config_value('identity','username')
        self.keystone_tenant = self.get_tempest_config_value('identity','tenant_name')
        self.keystone_pw = self.get_tempest_config_value('identity','password')
        self.keystone_uri = self.get_tempest_config_value('identity','uri')

        self.auth_token, self.tenant_id, self.service_catalog = keystone_base.get_auth_token(self)

        self.output("Prepare to be rannsaka'd...")


    def read_locust_config(self, config_file='work/locust_common.yml'):
        with open(config_file, 'r') as infile:
            data =  yaml.load(infile)
            self.config_file = data['args']['config_file']
            self.tempest_config = data['args']['tempest_config']
            self.debug = data['args']['debug']
            self.verbose = data['args']['verbose']


    def get_tempest_config_value(self, section, key_name):
        config = ConfigParser.ConfigParser()
        config.read(self.tempest_config)
        return config.get(section, key_name)


    def output(self,output_data):
        print "%s: %s" % (self.id, output_data)


    def get_endpoint(self, endpoint_type):
        for service in self.service_catalog:
            if service['type'] == endpoint_type:
                return service['endpoints'][0]['publicURL']
        return None


    def random_sleep(self, pool=None):
        if not pool:
            pool = [1,1,1,2,2,2,3,3,5,5,5,5,5,10,10,30,30,90]
        time.sleep(random.choice(pool))


    def random_hit(self, pool):
        """ Expect to get pool in the form of a list
            of N 1's and a single 2.  Return True if 2

        """
        if random.choice(pool) == 2:
            return True
        return False
        

    def one_in_five(self):
        pool = [1,1,1,1,2]
        return self.random_hit(pool)


    def one_in_ten(self):
        pool = [1,1,1,1,1,1,1,1,1,2]
        return self.random_hit(pool)
        
