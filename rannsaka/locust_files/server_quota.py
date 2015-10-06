import os
import random
import time
import json

from locust import HttpLocust, TaskSet, task

from task_sets.baseTaskSet import baseTaskSet
import task_funcs.keystone_v2_base as keystone_base
import task_funcs.nova_v2_base as nova_base
import task_funcs.nova_v2_utility as nova_util

class NovaSnapshot(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the nova api

    """

    def on_start(self):
        super(NovaSnapshot, self).on_start()
        self.server_count = 0
        self.image_count = 0
        self.min_server_count = 10 
        self.max_server_count = 10
        # limit list to less core / disk-intensive flavors in general
        self.flavor_list = [42,42,84,84,451]


    tasks = {nova_util.churn_server_pool: 5,
             nova_base.list_servers: 4,
             nova_base.list_servers_detail: 2,
             nova_base.list_server_detail: 1,
             #nova_util.create_server_image: 1,
             #nova_base.reboot_server: 7,
             #nova_util.resize_server: 7,
             nova_util.refresh_auth_token: 1
            } 

class NovaSnapshotUser(HttpLocust):
    task_set = NovaSnapshot 
    min_wait=500
    max_wait=5000



