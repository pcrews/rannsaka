import os
import random
import time

import json
from locust import HttpLocust, TaskSet, task

from lib.baseTaskSet import baseTaskSet

# TODO - make these config-driven
from lib.openstack.keystone import get_auth_token
from lib.openstack.nova import list_servers
from lib.openstack.nova import list_servers_detail
from lib.openstack.nova import list_server_detail
from lib.openstack.nova import create_server
from lib.openstack.nova import delete_server
from lib.openstack.nova import pause_server
from lib.openstack.nova import unpause_server
from lib.openstack.nova import suspend_server
from lib.openstack.nova import resume_server
from lib.openstack.nova import list_limits
from lib.openstack.nova import nova_get_server_id
from lib.openstack.nova import create_flavor
 

class UserBehavior(baseTaskSet):
    def on_start(self):
        super(UserBehavior, self).on_start()
        self.server_count = 0
        self.min_server_count = 7 
        self.max_server_count = 10 
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)

    @task(2)
    def nova_create_server(self):
        flavor_id = random.choice([42,84])
        response = create_server(self,
                                 flavor_id=flavor_id,
                                 name="server-%s-%s" % (self.id, self.server_count))
        server_id = json.loads(response.content)['server']['id']
        self.server_count += 1
        time.sleep(random.choice([1,1,3,3,3,5,5,5,5,5,5,10,10,10,10,25]))
        self.output("server id: %s" % server_id) 


    @task(1)
    def nova_pause_server(self):
        server_id = nova_get_server_id(self)
        pause_server(self, server_id)
        time.sleep(random.choice([1,1,1,1,3,3,3,5,10,25]))

    @task(1)
    def nova_unpause_server(self):
        server_id = nova_get_server_id(self)
        unpause_server(self, server_id)

    @task(4)
    def nova_pause_unpause_server(self):
        server_id = nova_get_server_id(self)
        pause_server(self, server_id)
        time.sleep(random.choice([1,1,3,3,5,5,5,5,10,10,10,10,25,30]))
        unpause_server(self, server_id)

    @task(4)
    def nova_suspend_resume_server(self):
        server_id = nova_get_server_id(self)
        suspend_server(self, server_id)
        time.sleep(random.choice([1,1,3,3,5,5,5,5,10,10,10,10,25,30]))
        resume_server(self, server_id)

    @task(2)
    def nova_suspend_server(self):
        server_id = nova_get_server_id(self)
        suspend_server(self, server_id)
        time.sleep(random.choice([1,1,1,1,3,3,3,5,10,25]))

    @task(1)
    def nova_resume_server(self):
        server_id = nova_get_server_id(self)
        resume_server(self, server_id)

    #@task(1)
    def nova_delete_server(self):
        server_id = nova_get_server_id(self)
        delete_server(self, server_id)

    @task(3)
    def nova_list_servers(self):
        response = list_servers(self)

    @task(3)
    def check_server_pool(self):
        response = list_servers(self)
        servers = json.loads(response.content)['servers']
        if len(servers) < self.min_server_count:
            self.nova_create_server()
        elif len(servers) == self.max_server_count:
            self.nova_delete_server()

    #@task(4)
    def nova_list_servers_detail(self):
        list_servers_detail(self)

    @task(4)
    def nova_list_limits(self):
        list_limits(self)

    @task(3)
    def keystone_auth_token(self):
        self.auth_token, self.tenant_id, self.service_catalog = get_auth_token(self)
 

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=500
    max_wait=5000
