import os
import random
import time
import json

from locust import HttpLocust, TaskSet, task

from task_sets.baseTaskSet import baseTaskSet
import task_funcs.keystone_v2_base as keystone_base
import task_funcs.heat_v1_base as heat_base
import task_funcs.heat_v1_utility as heat_util
import task_funcs.nova_v2_utility as nova_util

class HeatSnapshotTest(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the heat api

    """

    def on_start(self):
        super(HeatSnapshotTest, self).on_start()
        self.server_count = 0
        self.image_count = 0
        self.stack_count = 0
        self.min_stack_count = 9 
        self.max_stack_count = 15 
        # limit list to less core / disk-intensive flavors in general
        self.flavor_list = [42,42,84,84,451]
        self.heat_templates = ['locust_files/etc/heat_1vm_template.yml',
                               'locust_files/etc/heat_2vm_template.yml']


    def create_stack_and_snapshot(self):
        response, stack_name = heat_util.create_stack(self)
        self.output("CREATED STACK: %s <<<<<<<<<" % (stack_name))

        stack_response = heat_base.find_stack(self, stack_name)
        self.output("FIND STACK DATA:")
        self.output(stack_response.content)
        stack_id = json.loads(stack_response.content)['stack']['id']
        self.output("STACK_ID: %s" % (stack_id))

        sleep_time = 120
        self.output("Sleeping %d seconds before snapshot..." % (sleep_time))
        time.sleep(sleep_time)

        response = heat_base.create_snapshot(self, stack_name, stack_id)
        self.output(response)
        self.output("#"*80)

    tasks = {#heat_util.create_stack: 7,
             #heat_util.update_stack: 4,
             create_stack_and_snapshot: 10,
             #heat_base.delete_stack: 5,
             #heat_base.list_stack_detail:3,
             #heat_base.find_stack_events:2,
             #heat_base.list_stack_events:7,
             #heat_base.list_snapshots:3,
             #heat_base.list_snapshot_detail:7,
             #heat_base.find_stack_resources:7,
             #heat_base.list_stack_resources:4,
             #heat_base.get_stack_template:3,
             nova_util.refresh_auth_token:1
            } 

class HeatUser(HttpLocust):
    task_set = HeatSnapshotTest  
    min_wait=500
    max_wait=5000



