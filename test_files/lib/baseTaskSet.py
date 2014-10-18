import os

import json
from locust import HttpLocust, TaskSet, task

class baseTaskSet(TaskSet):
    """ baseTaskSet class
        basic task set containing primary utility methods
        that will be inherited / used by sub task sets
    
    """

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.id = str(self.locust).split('at')[1].strip().replace('>','')
        self.output("Prepare to be rannsaka'd...")


    def output(self,output_data):
        print "%s: %s" % (self.id, output_data)

 
    def get_endpoint(self, endpoint_type):
        for service in self.service_catalog:
            if service['type'] == endpoint_type:
                return service['endpoints'][0]['publicURL']
        return None
