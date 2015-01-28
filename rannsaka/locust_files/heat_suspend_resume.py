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

class HeatSuspendResume(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the heat api

    """

    def on_start(self):
        super(HeatSuspendResume, self).on_start()


    tasks = {heat_base.suspend_stack: 3,
             heat_base.resume_stack: 7,
             heat_base.list_stack_detail:3,
             heat_base.find_stack_events:2,
             heat_base.list_stack_events:7,
             heat_base.find_stack_resources:7,
             heat_base.list_stack_resources:4,
             heat_base.get_stack_template:3,
             nova_util.refresh_auth_token:1
            } 

class HeatUser(HttpLocust):
    task_set = HeatSuspendResume  
    min_wait=500
    max_wait=5000



