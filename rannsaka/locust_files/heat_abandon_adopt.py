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

class HeatAbandonAdopt(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the heat api

    """

    def on_start(self):
        super(HeatAbandonAdopt, self).on_start()
        self.server_count = 0
        self.image_count = 0
        self.min_server_count = 3 
        self.max_server_count = 2
        # limit list to less core / disk-intensive flavors in general
        self.flavor_list = [42,42,84,84,451]


    tasks = {heat_util.abandon_and_adopt_stack: 10,
             heat_base.list_stack_detail:3,
             heat_base.find_stack_events:2,
             heat_base.list_stack_events:7,
             #heat_base.list_snapshots:3,
             #heat_base.list_snapshot_detail:7,
             #heat_base.find_stack_resources:7,
             heat_base.list_stack_resources:4,
             heat_base.get_stack_template:3,
             nova_util.refresh_auth_token:1
            } 

class HeatUser(HttpLocust):
    task_set = HeatAbandonAdopt  
    min_wait=500
    max_wait=5000



