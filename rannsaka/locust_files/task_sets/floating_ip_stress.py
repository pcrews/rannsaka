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

class VipStress(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the nova api

    """

    def on_start(self):
        super(VipStress, self).on_start()

    tasks =  { nova_util.assign_and_remove_vip: 4,
               nova_base.delete_floating_ip: 3,
               nova_base.create_floating_ip: 7,
               nova_base.create_server: 5,
               nova_base.list_servers: 3,
               nova_base.list_servers_detail: 3,
               nova_util.refresh_auth_token: 1
              }
