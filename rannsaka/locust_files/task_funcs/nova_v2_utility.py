import os
import random
import time
import json

from locust import HttpLocust, TaskSet, task

import keystone_v2_base as keystone_base
import nova_v2_base as nova_base

""" These are more complex 'tasks' built, upon the base api tasks.
    They are intended to be a write-once, re-use-many resource and
    to provide the building blocks for task-sets / test runs.

"""

def churn_server_pool(self):
    """ This function is intended to do what it says - keep a create
        and delete cycle of servers going.
        It is also intended as a chaos generator during nova tests
        servers can be expected to randomly be deleted during operations

    """
 
    response = nova_base.list_servers(self)
    servers = json.loads(response.content)['servers']
    if len(servers) < self.min_server_count:
        if self.flavor_list:
            flavor_id = random.choice(self.flavor_list)
        else:
            # randomly grab one
            flavor_id = nova_base.get_flavor_id(self)
        nova_base.create_server(self,
                               flavor_id = flavor_id,
                               name="server-%s-%s" % (self.id, self.server_count))
        self.server_count += 1
    elif len(servers) >= self.max_server_count:
        server_id = nova_base.get_server_id(self)
        nova_base.delete_server(self, server_id)


def resize_server(self):
    # TODO: allow options on server_id values vs. just random
    server_id = nova_base.get_server_id(self)
    # TODO: allow options on flavor_id vs. just random
    # limit new flavors to a smaller set of smaller flavors
    # this is to increase the success rate and to prevent the system getting
    # 'stuck' in a boring test state due to lack of test cores
    flavor_id = random.choice([42,84,451,9998,9998,9998,9999,9999,9999])
    #flavor_id = nova_base.get_flavor_id(self)
    self.output("Resize server | %s | %s " % (server_id, flavor_id))
    if server_id:
        nova_base.resize_server(self, server_id, flavor_id)
        time.sleep(random.choice([5,9,9,9,9,10,10,10,10,25]))
        if self.one_in_five():
            nova_base.revert_resize_server(self, server_id)
        else:
            nova_base.confirm_resize_server(self,server_id)
    else:
        pass


def refresh_auth_token(self):
    self.auth_token, self.tenant_id, self.service_catalog = keystone_base.get_auth_token(self)


def assign_and_remove_vip(self):
    """ pick a server and a vip and assign and remove it """
    server_id = nova_base.get_server_id(self)
    floating_ip = nova_base.get_floating_ip(self)
    nova_base.assign_floating_ip(self,
                                server_id=server_id,
                                floating_ip=floating_ip)
    time.sleep(random.choice([1,1,1,1,1,3,5,10]))
    nova_base.remove_floating_ip(self,
                                server_id = server_id,
                                floating_ip = floating_ip)


def create_server_image(self):
    server_id = nova_base.get_server_id(self)
    image_name = "image-%s-%s-%s" % (self.id, server_id, self.image_count)
    result = nova_base.create_server_image(self, server_id=server_id, name=image_name)
    self.image_count += 1

