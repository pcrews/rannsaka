import os
import random
import time
import json

from locust import HttpLocust, TaskSet, task

from task_sets.baseTaskSet import baseTaskSet
import task_funcs.cinder_v1_base as cinder_base
import task_funcs.keystone_v2_base as keystone_base
import task_funcs.nova_v2_base as nova_base
import task_funcs.nova_v2_utility as nova_util


def check_volume_pool(self):
        volume_name = "%s-volume-%s" % (self.id, self.volume_count)
        self.volume_count +=1 
        response = cinder_base.list_volumes(self)
        volumes = json.loads(response.content)['volumes']
        if len(volumes) < self.min_volume_count:
            cinder_base.create_volume(self, name=volume_name)


def attach_volume(self):
        server_id = nova_base.get_server_id(self)
        volume_id = cinder_base.get_volume_id(self)
        self.output("attach_volume: %s || %s" % (server_id, volume_id))
        response = nova_base.attach_volume(self,
                                          server_id=server_id,
                                          volume_id=volume_id)

def remove_volume(self):
        server_id = nova_base.get_server_id(self)
        attachment_id = nova_base.get_attachment_id(self, server_id)
        self.output("remove_volume: %s || %s" % (server_id, attachment_id))
        response = nova_base.remove_volume(self,
                                          server_id=server_id,
                                          attachment_id=attachment_id)


class NovaCinderMix(baseTaskSet):
    """ task set designed to do insane, random, and valid things
        via the nova api

    """

    def on_start(self):
        super(NovaCinderMix, self).on_start()
        self.server_count = 0
        self.volume_count = 0
        self.min_server_count = 10 
        self.max_server_count = 20 
        self.min_volume_count = 10 
        # limit list to less core / disk-intensive flavors in general
        self.flavor_list = [42,42,84,84,451]


    tasks = {nova_util.churn_server_pool: 3,
             nova_base.list_servers: 2,
             #nova_base.list_servers_detail: 1,
             nova_util.refresh_auth_token: 1,
             nova_util.resize_server: 3,
             cinder_base.list_volumes: 3,
             #cinder_base.list_volume_detail: 3,
             check_volume_pool: 3,
             attach_volume: 3,
             #remove_volume: 1
            } 

class NovaCinderUser(HttpLocust):
    task_set = NovaCinderMix 
    min_wait=500
    max_wait=2000



