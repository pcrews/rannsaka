if __name__ == "__main__" and __package__ is None:
    __package__ = "task_sets.nova_basic_task_set"

import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

from baseTaskSet import baseTaskSet
import task_funcs.keystone_v2_base as keystone_base
import task_funcs.nova_v2_base as nova_base
import task_funcs.nova_v2_utility as nova_util
import task_funcs.heat_v1_base as heat_base

class HeatBasicStress(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the heat api

    """

    def on_start(self):
        super(HeatBasicStress, self).on_start()
        self.server_count = 0
        self.stack_count = 0 
        self.snapshot_count = 0

    tasks = {heat_base.list_stacks:5,
             heat_base.find_stack:5,
             heat_base.list_stack_detail:3,
             heat_base.find_stack_events:2,
             heat_base.list_stack_events:7,
             heat_base.list_snapshots:3,
             heat_base.list_snapshot_detail:7,
             heat_base.find_stack_resources:7,
             heat_base.list_stack_resources:4,
             heat_base.get_stack_template:7,
             heat_base.list_resource_types:7,
             #heat_base.suspend_stack:3,
             #heat_base.resume_stack:7,
             heat_base.create_snapshot:5,
             heat_base.delete_snapshot:2,
             heat_base.restore_snapshot:7,
             nova_util.refresh_auth_token:1
            } 
